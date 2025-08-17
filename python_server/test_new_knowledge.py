#!/usr/bin/env python3
"""
新しいナレッジベースの動作テスト
"""

import requests
import json

def test_api_with_nitto_questions():
    """Nittoに関する質問でAPIをテスト"""
    
    # APIエンドポイント
    url = "http://127.0.0.1:7200/reply"
    
    # テスト質問（2025_all.pdfに含まれていそうな内容）
    test_questions = [
        "Nittoグループの経営理念について教えて",
        "Creating Wondersとは何ですか？",
        "ESG経営について説明してください",
        "2025年度の業績について",
        "サステナビリティ重要課題について"
    ]
    
    print("新しいナレッジベースのテスト開始\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"【テスト {i}】質問: {question}")
        
        try:
            # APIにPOSTリクエスト送信
            response = requests.post(url, data={"inputtext": question}, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response_text", "応答なし")
                image_filename = result.get("image_filename", "不明")
                
                print(f"OK 応答: {response_text[:150]}...")
                print(f"画像: {image_filename}")
                print(f"応答文字数: {len(response_text)}")
                
                # 新しいナレッジが使われているかチェック
                if any(keyword in response_text for keyword in ["Nitto", "Creating", "2025"]):
                    print("新しいナレッジが使用されている可能性があります")
                else:
                    print("古いナレッジが使用されている可能性があります")
                    
            else:
                print(f"エラー: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"接続エラー: {e}")
            
        print("-" * 60)
        print()

if __name__ == "__main__":
    print("API動作確認ツール")
    print("前提条件: APIサーバーがポート7200で起動していること")
    print()
    
    # APIサーバーの状態確認
    try:
        response = requests.get("http://127.0.0.1:7200", timeout=5)
        print("APIサーバー接続OK")
    except:
        print("APIサーバーに接続できません")
        print("先にサーバーを起動してください:")
        print('python -m uvicorn src.web.api:app --host 0.0.0.0 --port 7200')
        exit(1)
    
    test_api_with_nitto_questions()
    print("テスト完了!")