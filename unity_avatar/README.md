# Unity Avatar Project

## 📁 ディレクトリ構成

```
unity_avatar/
└── aituber_3d/          # Unity 3D VRMアバタープロジェクト
    ├── Assets/           # アセットファイル
    ├── ProjectSettings/  # プロジェクト設定
    └── Packages/         # パッケージ依存関係
```

## 🚀 セットアップ手順

### 1. Unity プロジェクトのコピー

元のプロジェクトから必要なファイルを手動でコピーしてください：

```
元のプロジェクト: C:\temp\nitto-ai-avatar\aituber_3d\
コピー先: unity_avatar\aituber_3d\
```

**必要なフォルダ:**
- `Assets/` - すべてのアセットファイル
- `ProjectSettings/` - プロジェクト設定
- `Packages/` - パッケージ設定

**除外するフォルダ（一時ファイル）:**
- `Library/` - Unity生成キャッシュ
- `Temp/` - 一時ファイル
- `Obj/` - ビルド一時ファイル
- `Logs/` - ログファイル
- `UserSettings/` - ユーザー固有設定

### 2. Unity バージョン要件

- **推奨**: Unity 2022.3 LTS 以上
- **VRM対応**: VRM4U または UniVRM パッケージ

### 3. 重要なアセット

- **VRMアバター**: 安野たかひろ 3Dモデル
- **AudioSource**: 音声再生システム
- **UI System**: 対話インターフェース
- **API通信**: Python サーバー連携

## 🔧 Unity設定

### VRM パッケージインストール
```
Package Manager > Add package from git URL
URL: https://github.com/vrm-c/UniVRM.git?path=/Assets/VRM
```

### AudioSource 設定
1. `TextToSpeech` オブジェクトを選択
2. `AudioSource` コンポーネントを確認
3. Volume を 0.8 に設定

### API サーバー接続設定
- **エンドポイント**: `http://localhost:7200`
- **Unity Script**: API通信コンポーネント
- **CORS**: 必要に応じて設定

## 🎮 使用方法

1. **Unity起動**: プロジェクトを Unity で開く
2. **Play**: シーンを再生モード開始
3. **対話**: 画面下部の入力欄に質問を入力
4. **応答**: アバターが音声付きで回答

### テスト質問例
- 「こんにちは」
- 「Nittoの事業内容は？」
- 「2024年度の売上高は？」
- 「データサイエンスグループの活動について」

## 🔍 トラブルシューティング

### VRM モデルが表示されない
1. VRM パッケージがインストールされているか確認
2. Inspector でVRMコンポーネントを確認
3. マテリアルが正しく設定されているか確認

### 音声が再生されない
1. AudioSource の Volume 設定を確認
2. Python API サーバーが起動しているか確認
3. ネットワーク接続を確認

### API 通信エラー
1. Python サーバーのポート7200が開いているか確認
2. CORS設定を確認
3. ファイアウォール設定を確認

---

**注意**: Unity プロジェクトのサイズが大きいため、Gitリポジトリには含まれていません。手動コピーが必要です。