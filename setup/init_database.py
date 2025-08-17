#!/usr/bin/env python3
"""
Nitto AI Avatar System - Database Initialization Script
データベースの初期セットアップを行います
"""

import os
import sys
import asyncio
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "python_server"))

async def init_database():
    """データベースを初期化する"""
    try:
        # 設定ファイルの確認
        env_file = project_root / "python_server" / ".env"
        if not env_file.exists():
            print("❌ エラー: .env ファイルが見つかりません")
            print("📝 python_server/.env.template をコピーして .env を作成してください")
            return False
        
        # 設定の読み込み
        from src.config import settings
        
        print("🗄️ データベース初期化を開始...")
        print(f"📍 データベースタイプ: {settings.DATABASE_TYPE}")
        
        if settings.DATABASE_TYPE == "sqlite":
            # SQLiteデータベース作成
            from src.databases.engine import get_database_engine
            
            engine = get_database_engine()
            
            # テーブル作成のためのインポート
            from sqlalchemy import text
            
            # 基本的なテーブル構造を作成
            async with engine.begin() as conn:
                # シンプルなログテーブルを作成
                await conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS interaction_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        slide_info TEXT,
                        processing_time REAL
                    )
                """))
                
                print("✅ SQLiteデータベースを初期化しました")
            
            await engine.dispose()
            
        elif settings.DATABASE_TYPE == "postgresql":
            print("📝 PostgreSQL使用時は、事前にデータベースサーバーの準備が必要です")
            print("🔧 Alembicマイグレーションを実行してください：")
            print("   cd python_server && alembic upgrade head")
        
        print("🎉 データベース初期化が完了しました")
        return True
        
    except Exception as e:
        print(f"❌ データベース初期化エラー: {e}")
        return False

async def verify_database():
    """データベースの動作確認"""
    try:
        print("🔍 データベース接続テスト...")
        
        from src.databases.engine import get_database_engine
        engine = get_database_engine()
        
        async with engine.connect() as conn:
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1"))
            if result.fetchone():
                print("✅ データベース接続: OK")
            
        await engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ データベース接続エラー: {e}")
        return False

async def main():
    """メイン実行関数"""
    print("=" * 50)
    print("🎮 Nitto AI Avatar System")
    print("📊 Database Initialization")
    print("=" * 50)
    
    # 作業ディレクトリを設定
    os.chdir(project_root / "python_server")
    
    # データベース初期化
    if await init_database():
        # 接続テスト
        await verify_database()
        print("\n🎉 データベースのセットアップが完了しました")
        print("🚀 次のコマンドでAPIサーバーを起動できます：")
        print("   python -m uvicorn src.web.api:app --host 0.0.0.0 --port 7200")
    else:
        print("\n❌ データベースのセットアップに失敗しました")
        print("📝 .env ファイルの設定を確認してください")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())