#!/usr/bin/env python3
"""
PDF画像変換スクリプト
PDFファイルをページごとに画像（PNG）に変換し、Unityプロジェクトの適切なフォルダに保存します。
ポータブル対応：プロジェクト内のPopplerバイナリを使用します。
"""

import os
import sys
from pathlib import Path
import argparse
from pdf2image import convert_from_path
import logging

# ポータブルPoppler設定
def setup_portable_poppler():
    """プロジェクト内のPopplerバイナリを設定"""
    current_dir = Path(__file__).parent
    poppler_path = current_dir.parent / "tools" / "poppler" / "Library" / "bin"
    
    if poppler_path.exists():
        logger.info(f"ポータブルPoppler使用: {poppler_path}")
        return str(poppler_path)
    else:
        logger.warning(f"ポータブルPopplerが見つかりません: {poppler_path}")
        logger.info("システムPATHのPopplerを使用します")
        return None

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_output_directory(output_dir: str) -> Path:
    """出力ディレクトリを作成・設定"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"出力ディレクトリ: {output_path}")
    return output_path

def convert_pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 200) -> list:
    """
    PDFファイルを画像に変換
    
    Args:
        pdf_path: PDFファイルのパス
        output_dir: 出力ディレクトリ
        dpi: 画像の解像度
        
    Returns:
        変換された画像ファイルのパスリスト
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
    
    output_path = setup_output_directory(output_dir)
    
    # ポータブルPopplerのパスを取得
    poppler_path = setup_portable_poppler()
    
    logger.info(f"PDF変換開始: {pdf_file.name}")
    
    try:
        # PDFを画像に変換（ポータブルPoppler対応）
        if poppler_path:
            images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
        else:
            images = convert_from_path(pdf_path, dpi=dpi)
        image_paths = []
        
        for i, image in enumerate(images, 1):
            # ファイル名を slide_{i}.png 形式で保存
            image_filename = f"slide_{i}.png"
            image_path = output_path / image_filename
            
            # PNG形式で保存
            image.save(image_path, "PNG")
            image_paths.append(str(image_path))
            
            logger.info(f"ページ {i} を保存: {image_filename}")
        
        logger.info(f"変換完了: {len(images)} ページを処理しました")
        return image_paths
        
    except Exception as e:
        logger.error(f"PDF変換エラー: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="PDFファイルをページごとに画像に変換")
    parser.add_argument("pdf_path", help="変換するPDFファイルのパス")
    parser.add_argument("-o", "--output", default="../aituber_3d/Assets/Resources/Slides", 
                       help="出力ディレクトリ (デフォルト: ../aituber_3d/Assets/Resources/Slides)")
    parser.add_argument("--dpi", type=int, default=200, help="画像の解像度 (デフォルト: 200)")
    
    args = parser.parse_args()
    
    try:
        image_paths = convert_pdf_to_images(args.pdf_path, args.output, args.dpi)
        
        print(f"\n✅ 変換完了!")
        print(f"📁 出力先: {args.output}")
        print(f"📄 変換ページ数: {len(image_paths)}")
        print(f"\n次の手順:")
        print("1. Unityで Assets > Set Texture Type to Sprite を実行")
        print("2. マルチモーダルLLMでPDFからCSVを生成")
        print("3. FAISSナレッジDBを再構築")
        
    except Exception as e:
        logger.error(f"処理エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()