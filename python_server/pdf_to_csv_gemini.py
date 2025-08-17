#!/usr/bin/env python3
"""
PDF画像をGemini APIでCSVナレッジファイルに変換
各ページの画像をGeminiに送信してタイトルと内容を抽出し、CSVファイルを生成
"""

import os
import sys
import asyncio
import csv
from pathlib import Path
import argparse
import logging
from typing import List, Dict
import google.generativeai as genai
from PIL import Image
import time

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFToCSVConverter:
    def __init__(self, api_key: str):
        """Gemini APIクライアントを初期化"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.retry_model = genai.GenerativeModel('gemini-1.5-flash')  # リトライ用高速モデル
        logger.info("Gemini API初期化完了")
    
    def extract_slide_info(self, image_path: str, slide_number: int) -> Dict[str, str]:
        """
        画像からスライド情報を抽出
        
        Args:
            image_path: 画像ファイルのパス
            slide_number: スライド番号
            
        Returns:
            スライド情報の辞書
        """
        try:
            # 画像を読み込み
            image = Image.open(image_path)
            
            # ナレッジベース用に最適化されたプロンプト
            prompt = """
このスライド画像を分析して、AIチャットボットのナレッジベースとして使用するデータを抽出してください。

【重要】ナレッジベースの目的：
- ユーザーからの質問に適切に回答するための知識データとして使用
- 検索可能で、理解しやすい形式での情報整理が必要

抽出してください：
1. title: スライドのメインタイトルまたは主要テーマ（30文字以内、検索しやすいキーワードを含む）
2. text: スライドの全内容を体系的に説明
   - 重要なポイント、数値、事実を漏らさず記載
   - 図表やグラフの内容も文章で説明
   - 箇条書きの項目も文章として統合
   - ユーザーが質問しそうな観点から記述

以下のJSON形式で回答してください：
{
  "title": "検索しやすいタイトル",
  "text": "ナレッジベースとして有用な詳細説明（150文字以上、具体的な情報を含む）"
}

注意：
- textは必ず150文字以上で記述
- 専門用語は説明を併記
- 数値やデータは正確に記載
- JSONのみを返してください
"""
            
            # Gemini APIを呼び出し
            logger.info(f"スライド {slide_number} を分析中...")
            response = self.model.generate_content([prompt, image])
            
            # レスポンスからJSONを抽出
            response_text = response.text.strip()
            
            # JSONブロックを抽出（```json で囲まれている場合に対応）
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_text = response_text[start:end].strip()
            elif response_text.startswith("{") and response_text.endswith("}"):
                json_text = response_text
            else:
                # JSONブロックが見つからない場合のフォールバック
                logger.warning(f"スライド {slide_number}: JSON形式でない応答を受信")
                return {
                    "title": f"スライド {slide_number}",
                    "text": response_text[:500]  # 最初の500文字を使用
                }
            
            # JSONをパース
            import json
            slide_data = json.loads(json_text)
            
            # 品質チェック
            quality_result = self.check_quality(slide_data, slide_number)
            
            if not quality_result["is_good"]:
                logger.warning(f"スライド {slide_number} 品質不足: {quality_result['issues']}")
                # 品質改善を試行
                improved_data = self.improve_quality(image, slide_data, slide_number)
                if improved_data:
                    slide_data = improved_data
            
            logger.info(f"スライド {slide_number} 分析完了: {slide_data.get('title', 'タイトルなし')}")
            return slide_data
            
        except Exception as e:
            logger.error(f"スライド {slide_number} の分析エラー: {e}")
            # エラー時のフォールバック
            return {
                "title": f"スライド {slide_number}",
                "text": f"スライド {slide_number} の内容（分析エラーのため詳細不明）"
            }
    
    def check_quality(self, slide_data: Dict[str, str], slide_number: int) -> Dict[str, any]:
        """
        抽出されたデータの品質をチェック
        
        Returns:
            品質チェック結果の辞書
        """
        issues = []
        
        # タイトルチェック
        title = slide_data.get("title", "")
        if len(title) < 5:
            issues.append("タイトルが短すぎます（5文字未満）")
        elif len(title) > 50:
            issues.append("タイトルが長すぎます（50文字超）")
        
        # テキストチェック
        text = slide_data.get("text", "")
        if len(text) < 100:
            issues.append(f"説明文が短すぎます（{len(text)}文字、最低100文字）")
        elif "スライド" in text and "内容" in text and len(text) < 150:
            issues.append("説明文が汎用的すぎます")
        
        # 具体性チェック
        if not any(keyword in text for keyword in ["について", "である", "です", "ます", "した", "する"]):
            issues.append("説明文に具体的な記述が不足")
        
        return {
            "is_good": len(issues) == 0,
            "issues": issues
        }
    
    def improve_quality(self, image, original_data: Dict[str, str], slide_number: int) -> Dict[str, str]:
        """
        品質の低いデータを改善
        """
        try:
            improvement_prompt = f"""
前回の分析結果が不十分でした：
- タイトル: "{original_data.get('title', '')}"
- 説明: "{original_data.get('text', '')}"

このスライド画像をより詳細に分析し直してください。
特に以下の点を改善してください：

1. タイトル: より具体的で検索しやすいキーワードを含める（5-30文字）
2. 説明文: 最低150文字以上で、以下を含める：
   - スライドの具体的な内容
   - 数値やデータがあれば正確に記載
   - 図表の説明
   - 重要なポイントの詳細

JSON形式で回答：
{{
  "title": "改善されたタイトル",
  "text": "詳細で具体的な説明（150文字以上）"
}}
"""
            
            logger.info(f"スライド {slide_number} 品質改善を実行中...")
            response = self.retry_model.generate_content([improvement_prompt, image])
            
            response_text = response.text.strip()
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_text = response_text[start:end].strip()
            else:
                json_text = response_text
            
            import json
            improved_data = json.loads(json_text)
            
            # 改善後の品質チェック
            quality_result = self.check_quality(improved_data, slide_number)
            if quality_result["is_good"]:
                logger.info(f"スライド {slide_number} 品質改善成功")
                return improved_data
            else:
                logger.warning(f"スライド {slide_number} 品質改善失敗")
                return None
                
        except Exception as e:
            logger.error(f"スライド {slide_number} 品質改善エラー: {e}")
            return None
    
    def process_all_slides(self, slides_dir: str, output_csv: str) -> None:
        """
        全スライド画像を処理してCSVファイルを生成
        
        Args:
            slides_dir: スライド画像があるディレクトリ
            output_csv: 出力CSVファイルのパス
        """
        slides_path = Path(slides_dir)
        
        # slide_*.png ファイルを取得（番号順にソート）
        slide_files = sorted(
            slides_path.glob("slide_*.png"),
            key=lambda x: int(x.stem.replace("slide_", ""))
        )
        
        if not slide_files:
            raise FileNotFoundError(f"スライド画像が見つかりません: {slides_path}/slide_*.png")
        
        logger.info(f"{len(slide_files)} 枚のスライドを処理開始")
        
        csv_data = []
        
        for i, slide_file in enumerate(slide_files, 1):
            try:
                # APIレート制限対策で少し待機
                if i > 1:
                    time.sleep(2)  # 2秒待機
                
                # スライド情報を抽出
                slide_info = self.extract_slide_info(str(slide_file), i)
                
                # CSVデータに追加
                csv_data.append({
                    "title": slide_info.get("title", f"スライド {i}"),
                    "text": slide_info.get("text", ""),
                    "filename": f"slide_{i}.png"
                })
                
                logger.info(f"進捗: {i}/{len(slide_files)} 完了")
                
            except Exception as e:
                logger.error(f"スライド {i} の処理エラー: {e}")
                # エラー時もCSVに追加（空の内容で）
                csv_data.append({
                    "title": f"スライド {i}",
                    "text": "",
                    "filename": f"slide_{i}.png"
                })
        
        # CSVファイルに書き込み
        self.write_csv(csv_data, output_csv)
        logger.info(f"CSV生成完了: {output_csv}")
    
    def write_csv(self, data: List[Dict], output_path: str) -> None:
        """CSVファイルを書き込み"""
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'text', 'filename']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in data:
                writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="PDF画像をGemini APIでCSVナレッジファイルに変換")
    parser.add_argument("--slides-dir", default="../aituber_3d/Assets/Resources/Slides", 
                       help="スライド画像ディレクトリ (デフォルト: ../aituber_3d/Assets/Resources/Slides)")
    parser.add_argument("--output", default="faiss_knowledge/auto_generated_2025.csv", 
                       help="出力CSVファイル (デフォルト: faiss_knowledge/auto_generated_2025.csv)")
    parser.add_argument("--api-key", help="Gemini APIキー（設定されていない場合は環境変数から取得）")
    
    args = parser.parse_args()
    
    # APIキーの取得
    api_key = args.api_key
    if not api_key:
        # 環境変数または設定ファイルから取得
        try:
            from src.config import settings
            api_key = settings.GOOGLE_API_KEY
        except ImportError:
            api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        logger.error("Gemini APIキーが設定されていません")
        logger.error("--api-key オプションまたは環境変数GOOGLE_API_KEYを設定してください")
        sys.exit(1)
    
    try:
        # 変換処理を実行
        converter = PDFToCSVConverter(api_key)
        converter.process_all_slides(args.slides_dir, args.output)
        
        print(f"\n✅ CSV生成完了!")
        print(f"📁 出力ファイル: {args.output}")
        print(f"\n次のステップ:")
        print("1. 生成されたCSVファイルを確認")
        print("2. FAISSナレッジDBを再構築")
        
    except Exception as e:
        logger.error(f"処理エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()