#!/usr/bin/env python3
"""
FAISS データベース再構築スクリプト
"""
import os
import pandas as pd
from langchain.schema.document import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import settings
import google.generativeai as genai

# Google AI API設定
genai.configure(api_key=settings.GOOGLE_API_KEY)
os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

def rebuild_qa_database():
    """QAデータベースを再構築"""
    print("QAデータベースを再構築中...")
    
    # Nitto企業用のQAデータを作成
    sample_qa_data = [
        {"question": "Nittoの経営理念について教えて", "answer": "NittoのMissionは「新しい発想でお客様の価値創造に貢献します」、Visionは「Creating Wonders」です。"},
        {"question": "Nittoの技術について", "answer": "粘接着、多孔、剥離などのコア技術を活かした製品開発を行っています。"},
        {"question": "Innovation for Customersとは", "answer": "お客様の価値創造に貢献する製品・システム・アイデアの提供を目指すNittoのスローガンです。"},
        {"question": "Nittoの事業領域について", "answer": "電子部品、自動車、医療、インダストリアルテープなど幅広い分野で事業を展開しています。"},
        {"question": "データサイエンスグループについて", "answer": "Nitto研究開発本部の一部門として、AI・データ分析技術を活用した価値創造に取り組んでいます。"}
    ]
    
    documents = []
    for i, qa in enumerate(sample_qa_data):
        content = f"Q: {qa['question']}\nA: {qa['answer']}"
        
        doc = Document(
            page_content=content,
            metadata={"source": f"qa_{i}", "row": i, "question": qa['question']}
        )
        documents.append(doc)
    
    # 埋め込みモデル作成
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    # FAISSデータベース作成
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # 保存
    vectorstore.save_local("faiss_qa")
    print(f"QAデータベース再構築完了: {len(documents)}件のドキュメント")
    
    return vectorstore

def rebuild_knowledge_database():
    """知識データベースを再構築"""
    print("知識データベースを再構築中...")
    
    # CSVファイルを読み込み（新しい2025ナレッジデータ）
    knowledge_csv_path = "faiss_knowledge/2025_all_knowledge.csv"
    df = pd.read_csv(knowledge_csv_path, encoding='utf-8-sig')
    
    documents = []
    for i, row in df.iterrows():
        title = row.get('title', f'Document {i}')
        text = row.get('text', '')
        filename = row.get('filename', f'doc_{i}.png')
        
        page_content = f"Title: {title}\n{text}"
        metadata = {
            "row": i,
            "image": filename,
            "title": title
        }
        
        doc = Document(
            page_content=page_content,
            metadata=metadata
        )
        documents.append(doc)
    
    # 埋め込みモデル作成
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    # FAISSデータベース作成
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # 保存
    vectorstore.save_local("faiss_knowledge")
    print(f"知識データベース再構築完了: {len(documents)}件のドキュメント")
    
    return vectorstore

def test_databases():
    """データベースをテスト"""
    print("\n=== データベーステスト ===")
    
    try:
        # QAデータベーステスト
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        qa_db = FAISS.load_local("faiss_qa", embeddings, allow_dangerous_deserialization=True)
        qa_results = qa_db.similarity_search("Nitto技術", k=2)
        print(f"QAテスト成功: {len(qa_results)}件の結果")
        
        # 知識データベーステスト
        knowledge_db = FAISS.load_local("faiss_knowledge", embeddings, allow_dangerous_deserialization=True)
        knowledge_results = knowledge_db.similarity_search("AI技術", k=2)
        print(f"知識DBテスト成功: {len(knowledge_results)}件の結果")
        
        return True
    except Exception as e:
        print(f"テストエラー: {e}")
        return False

if __name__ == "__main__":
    # カレントディレクトリを確認
    print(f"カレントディレクトリ: {os.getcwd()}")
    
    # QAデータベース再構築
    rebuild_qa_database()
    
    # 知識データベース再構築
    rebuild_knowledge_database()
    
    # テスト実行
    if test_databases():
        print("\n✅ FAISS データベース再構築完了！")
    else:
        print("\n❌ テストに失敗しました")