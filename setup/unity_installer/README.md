# Unity Hub インストーラー

## 📥 オフラインインストール対応

Unity公式サイトにアクセスできない環境での Unity インストールを支援します。

### 🎮 含まれるファイル

- **Unity Hub.exe**: Unity Hub インストーラー (バージョン 3.x)
- **サイズ**: 約 100MB
- **対応OS**: Windows 10/11 (64bit)

### 🚀 インストール手順

#### 1. Unity Hub インストール
```bash
# Unity Hub.exe を実行
./Unity Hub.exe
```

#### 2. Unity Editor インストール
Unity Hub起動後:
1. **Installs** タブを選択
2. **Install Editor** をクリック
3. **Unity 2022.3 LTS** を選択（推奨）
4. 必要なモジュールを選択:
   - ✅ Microsoft Visual Studio Community
   - ✅ Windows Build Support (IL2CPP)
   - ⭕ Documentation (オプション)

#### 3. プロジェクト開く
```bash
# Unity Hub で「プロジェクトを追加」
# パス: unity_avatar/aituber_3d/
```

### 🌐 代替ダウンロード方法

Unity公式サイトがアクセス可能な場合:
- **Unity Hub**: https://unity3d.com/get-unity/download
- **Unity Archives**: https://unity3d.com/get-unity/download/archive

### ⚡ 推奨システム要件

- **OS**: Windows 10 (64bit) 以上
- **CPU**: Intel Core i5 以上
- **RAM**: 8GB以上（16GB推奨）
- **ストレージ**: 10GB以上の空き容量
- **GPU**: DirectX 11対応

### 🔧 インストール後の設定

1. **プロジェクト依存関係**: Unity初回起動時に自動インストール
   - VRM (VRMアバター用)
   - TextMeshPro (UI表示用)
   - DOTween (アニメーション用)

2. **フォント設定**: 大容量フォントファイル除外時の対応
   - Window > TextMeshPro > Font Asset Creator
   - システムフォント（メイリオ等）を使用

### 🚨 トラブルシューティング

#### Unity Hub が起動しない
- Windows Defender の除外設定を確認
- 管理者権限で実行を試行

#### Unity Editor ダウンロードエラー
- インターネット接続を確認
- ファイアウォール設定を確認
- VPN経由でのアクセスを試行

---

**💡 重要**: Unity のライセンス認証にはインターネット接続が必要です。オフライン環境では Personal ライセンスの認証に制限があります。