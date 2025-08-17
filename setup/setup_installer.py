#!/usr/bin/env python3
"""
Nitto AI Avatar System - 自動セットアップインストーラー
Python依存関係とシステム要件の自動インストール
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🤖 Nitto AI Avatar System - セットアップインストーラー")
    print("=" * 60)
    print()

def check_python_version():
    """Python バージョンチェック"""
    print("📋 Python バージョン確認中...")
    if sys.version_info < (3, 12):
        print("❌ Error: Python 3.12以上が必要です")
        print(f"   現在のバージョン: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} - OK")
    return True

def install_requirements():
    """Python 依存関係のインストール"""
    print("\n📦 Python依存関係をインストール中...")
    
    requirements = [
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "google-generativeai>=0.7.0",
        "azure-cognitiveservices-speech>=1.34.0",
        "faiss-cpu>=1.7.4",
        "rank-bm25>=0.2.2",
        "structlog>=23.2.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.0",
        "pandas>=2.1.0",
        "psycopg>=3.1.0",
        "psycopg-binary>=3.1.0",
        "alembic>=1.13.0",
        "elevenlabs>=1.0.0",
        "janome>=0.5.0",
        "jaconv>=0.3.4",
        "click>=8.1.0"
    ]
    
    for requirement in requirements:
        print(f"   Installing {requirement}...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", requirement, "--user"
            ], check=True, capture_output=True)
            print(f"   ✅ {requirement}")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {requirement}")
            print(f"      Error: {e}")
            return False
    
    print("✅ すべての依存関係のインストールが完了しました")
    return True

def setup_database():
    """データベースの初期設定"""
    print("\n🗄️ データベース設定中...")
    
    # プロジェクトルートのパスを取得
    setup_dir = Path(__file__).parent
    project_root = setup_dir.parent
    python_server_dir = project_root / "python_server"
    
    if not python_server_dir.exists():
        print("❌ python_server ディレクトリが見つかりません")
        return False
    
    os.chdir(python_server_dir)
    
    try:
        # Alembic マイグレーション実行
        print("   Alembic マイグレーション実行中...")
        subprocess.run([
            sys.executable, "-m", "alembic", "upgrade", "head"
        ], check=True, capture_output=True)
        print("   ✅ データベースマイグレーション完了")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ データベース設定に失敗: {e}")
        return False

def check_env_file():
    """環境設定ファイルの確認"""
    print("\n🔑 環境設定ファイル確認中...")
    
    setup_dir = Path(__file__).parent
    project_root = setup_dir.parent
    env_file = project_root / "python_server" / ".env"
    env_template = project_root / "python_server" / ".env.template"
    
    if not env_file.exists():
        if env_template.exists():
            print("   .env ファイルが見つかりません")
            print(f"   📝 {env_template} を {env_file} にコピーして")
            print("      APIキーを設定してください")
            return False
        else:
            print("❌ .env.template ファイルが見つかりません")
            return False
    
    print("✅ .env ファイルが存在します")
    return True

def check_unity_installation():
    """Unity インストール確認"""
    print("\n🎮 Unity インストール確認中...")
    
    # Windowsの場合
    if platform.system() == "Windows":
        unity_paths = [
            "C:\\Program Files\\Unity\\Hub\\Editor\\*\\Editor\\Unity.exe",
            "C:\\Program Files\\Unity\\Editor\\Unity.exe"
        ]
        
        for path in unity_paths:
            if "*" in path:
                # ワイルドカード展開
                import glob
                matches = glob.glob(path)
                if matches:
                    print("✅ Unity エディター検出: 利用可能")
                    return True
            else:
                if os.path.exists(path):
                    print("✅ Unity エディター検出: 利用可能")
                    return True
    
    print("⚠️  Unity エディターが検出されませんでした")
    print("   Unity 2022.3 LTS 以上をインストールしてください")
    print("   https://unity.com/download")
    return False

def print_setup_completion():
    """セットアップ完了メッセージ"""
    print("\n" + "=" * 60)
    print("🎉 セットアップ完了！")
    print("=" * 60)
    print()
    print("📋 次の手順:")
    print()
    print("1. APIキー設定:")
    print("   python_server/.env ファイルを編集")
    print("   - GOOGLE_API_KEY (Google Gemini)")
    print("   - AZURE_SPEECH_KEY (Azure Speech Services)")
    print()
    print("2. サーバー起動:")
    print("   cd python_server")
    print("   python -m uvicorn src.web.api:app --host 0.0.0.0 --port 7200")
    print()
    print("3. Unity起動:")
    print("   unity_avatar/aituber_3d/ プロジェクトを Unity で開く")
    print()
    print("4. 対話テスト:")
    print("   - Playボタンを押す")
    print("   - 「Nittoの事業内容は？」などの質問を入力")
    print()
    print("🔧 トラブルシューティング:")
    print("   docs/troubleshooting.md を参照")
    print()

def main():
    """メイン実行関数"""
    print_header()
    
    # システムチェック
    checks = [
        ("Python バージョン", check_python_version),
        ("Python 依存関係", install_requirements),
        ("データベース設定", setup_database),
        ("環境設定ファイル", check_env_file),
        ("Unity インストール", check_unity_installation)
    ]
    
    failed_checks = []
    
    for check_name, check_func in checks:
        try:
            if not check_func():
                failed_checks.append(check_name)
        except Exception as e:
            print(f"❌ {check_name} でエラーが発生: {e}")
            failed_checks.append(check_name)
    
    if failed_checks:
        print(f"\n⚠️  以下の項目で問題が発生しました:")
        for failed in failed_checks:
            print(f"   - {failed}")
        print("\n詳細は上記のエラーメッセージを確認してください")
        return 1
    
    print_setup_completion()
    return 0

if __name__ == "__main__":
    sys.exit(main())