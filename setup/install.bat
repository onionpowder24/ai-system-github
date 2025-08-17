@echo off
echo ======================================================
echo 🤖 Nitto AI Avatar System - Windows インストーラー
echo ======================================================
echo.

REM Python バージョンチェック
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python がインストールされていません
    echo    Python 3.12+ をインストールしてください
    echo    https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python が見つかりました
python --version

REM 依存関係インストール
echo.
echo 📦 Python 依存関係をインストール中...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --user

if errorlevel 1 (
    echo ❌ 依存関係のインストールに失敗しました
    echo    詳細は上記のエラーメッセージを確認してください
    pause
    exit /b 1
)

echo ✅ 依存関係のインストールが完了しました

REM 環境設定ファイル確認
echo.
echo 🔑 環境設定ファイル確認中...
if not exist "..\python_server\.env" (
    if exist "..\python_server\.env.template" (
        echo    .env ファイルをコピーしています...
        copy "..\python_server\.env.template" "..\python_server\.env"
        echo ⚠️  APIキーを設定してください:
        echo    ..\python_server\.env
    ) else (
        echo ❌ .env.template ファイルが見つかりません
    )
) else (
    echo ✅ .env ファイルが存在します
)

REM データベース設定
echo.
echo 🗄️ データベース設定中...
cd ..\python_server
python -m alembic upgrade head
if errorlevel 1 (
    echo ❌ データベース設定に失敗しました
    pause
    exit /b 1
)
echo ✅ データベース設定が完了しました

cd ..\setup

echo.
echo ======================================================
echo 🎉 インストール完了！
echo ======================================================
echo.
echo 📋 次の手順:
echo.
echo 1. APIキー設定:
echo    ..\python_server\.env ファイルを編集してください
echo    - GOOGLE_API_KEY (Google Gemini API)
echo    - AZURE_SPEECH_KEY (Azure Speech Services)
echo.
echo 2. サーバー起動:
echo    cd ..\python_server
echo    python -m uvicorn src.web.api:app --host 0.0.0.0 --port 7200
echo.
echo 3. Unity起動:
echo    ..\unity_avatar\aituber_3d\ プロジェクトを Unity で開く
echo.
echo 🔧 問題が発生した場合:
echo    docs\troubleshooting.md を参照してください
echo.
pause