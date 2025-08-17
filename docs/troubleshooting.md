# Nitto AI Avatar System - トラブルシューティング

## 🔧 よくある問題と解決法

### 1. APIキー関連エラー

#### Google Gemini API エラー
```
Error: Google API key not found or invalid
```

**解決方法:**
1. [Google AI Studio](https://makersuite.google.com/app/apikey) でAPIキーを取得
2. `.env` ファイルの `GOOGLE_API_KEY` を設定
3. APIキーが有効か確認

#### Azure Speech Services エラー
```
Error: Azure Speech service authentication failed
```

**解決方法:**
1. [Azure Portal](https://portal.azure.com) で Speech Services リソースを作成
2. `.env` ファイルの `AZURE_SPEECH_KEY` と `AZURE_SPEECH_REGION` を設定
3. リソースがアクティブか確認

### 2. Python依存関係エラー

#### パッケージインストールエラー
```
ERROR: Could not install packages due to an EnvironmentError
```

**解決方法:**
```bash
# 管理者権限で実行 (Windows)
python -m pip install -r setup/requirements.txt --user

# または仮想環境を使用
python -m venv venv
venv\Scripts\activate
pip install -r setup/requirements.txt
```

#### FAISS インストールエラー
```
ERROR: Failed building wheel for faiss-cpu
```

**解決方法:**
```bash
# Windows の場合
pip install faiss-cpu --only-binary=:all:

# または conda を使用
conda install -c conda-forge faiss-cpu
```

### 3. データベース関連エラー

#### Alembic マイグレーションエラー
```
ERROR: Can't locate revision identified by
```

**解決方法:**
```bash
cd python_server
python -m alembic stamp head
python -m alembic upgrade head
```

#### SQLite ファイル作成エラー
```
ERROR: unable to open database file
```

**解決方法:**
1. `python_server` ディレクトリに書き込み権限があるか確認
2. ディスク容量を確認
3. アンチウイルスソフトの除外設定を確認

### 4. Unity関連エラー

#### Unity プロジェクトが開けない
```
Error: Failed to open project
```

**解決方法:**
1. Unity 2022.3 LTS 以上がインストールされているか確認
2. Unity Hub から「プロジェクトを追加」で `unity_avatar/aituber_3d/` を選択
3. プロジェクトフォルダが完全にコピーされているか確認

#### VRM アバターが表示されない
```
Error: Missing VRM components
```

**解決方法:**
1. VRM Package をインポート: `Package Manager > Add package from git URL`
2. URL: `https://github.com/vrm-c/UniVRM.git?path=/Assets/VRM`
3. プロジェクトをリビルド

### 5. ネットワーク関連エラー

#### APIサーバー接続エラー
```
Error: Connection refused to localhost:7200
```

**解決方法:**
1. APIサーバーが起動しているか確認:
```bash
cd python_server
python -m uvicorn src.web.api:app --host 0.0.0.0 --port 7200
```
2. ファイアウォールでポート7200が許可されているか確認
3. アンチウイルスソフトの設定を確認

#### CORS エラー
```
Error: Access to fetch at 'http://localhost:7200' from origin 'null' has been blocked by CORS policy
```

**解決方法:**
1. `src/web/api.py` でCORS設定を確認
2. 必要に応じてUnityのドメインを追加

### 6. 音声関連エラー

#### 音声が再生されない
```
Error: AudioSource is not configured
```

**解決方法:**
1. Unity で `TextToSpeech` オブジェクトを確認
2. `AudioSource` コンポーネントが設定されているか確認
3. Volume が 0 でないか確認

#### 音声ファイル生成エラー
```
Error: Failed to synthesize speech
```

**解決方法:**
1. Azure Speech Services のAPIキーを確認
2. リージョン設定を確認
3. ネットワーク接続を確認

### 7. RAG システム関連エラー

#### スライド選択が不適切
```
問題: 事業内容質問で役員報酬スライドが選ばれる
```

**解決方法:**
1. ログで `Gemini選択:` メッセージを確認
2. `get_faiss_vector.py` の判定基準を調整
3. FAISS インデックスを再構築

#### ハルシネーション検出が機能しない
```
問題: 不適切な応答が検出されない
```

**解決方法:**
1. `gpt.py` の `check_hallucination` 関数を確認
2. `if False:` などで無効化されていないか確認
3. Gemini API の応答を確認

### 8. パフォーマンス問題

#### 応答が遅い
```
問題: 質問から回答まで10秒以上かかる
```

**解決方法:**
1. FAISS インデックスサイズを確認
2. `top_k` パラメータを調整 (15 → 10)
3. Gemini API のレスポンス時間を確認

#### メモリ使用量が高い
```
問題: システムメモリ不足
```

**解決方法:**
1. FAISS インデックスをファイルに保存
2. 不要なデータを定期的にクリア
3. バッチサイズを調整

## 🆘 緊急時の対処法

### システム完全リセット
```bash
# 1. プロセス停止
taskkill /F /IM python.exe
taskkill /F /IM Unity.exe

# 2. データベースリセット
cd python_server
del aituber.db
python -m alembic upgrade head

# 3. ログクリア
rmdir /S log
mkdir log

# 4. 再起動
python -m uvicorn src.web.api:app --host 0.0.0.0 --port 7200
```

### 設定ファイルリセット
```bash
# .env ファイルを初期状態に戻す
cd python_server
copy .env.template .env
# APIキーを再設定
```

## 📞 サポート

### ログファイルの場所
- **APIサーバーログ**: `python_server/log/`
- **Unityログ**: Unity Console Window
- **システムログ**: イベントビューアー (Windows)

### デバッグモード有効化
```bash
# 詳細ログ出力
export DEBUG=true
python -m uvicorn src.web.api:app --log-level debug
```

### 問題報告時の情報
問題を報告する際は、以下の情報を含めてください:

1. **環境情報**:
   - OS: Windows 10/11
   - Python バージョン
   - Unity バージョン

2. **エラーメッセージ**:
   - 完全なエラーログ
   - 再現手順

3. **設定情報**:
   - .env ファイル (APIキー以外)
   - 実行したコマンド

### GitHub Issues
詳細なサポートが必要な場合は、GitHubで Issues を作成してください:
https://github.com/onionpowder24/nitto-ai-system/issues