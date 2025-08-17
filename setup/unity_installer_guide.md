# Unity インストールガイド

## 🎮 Unity 2022.3 LTS インストール方法

### 📥 方法1: Unity Hub経由（推奨）
1. **Unity Hub ダウンロード**: https://unity3d.com/get-unity/download
2. **Unity Hub インストール**: ダウンロードした UnityHubSetup.exe を実行
3. **Unity LTS バージョン**: Unity Hub で 2022.3 LTS をインストール

### 📥 方法2: 直接ダウンロード
Unity公式サイトにアクセスできない場合:

```
Unity 2022.3 LTS (推奨バージョン)
ファイル名: UnitySetup64-2022.3.XX.exe
サイズ: 約 3-4 GB
```

### 🌐 **代替ダウンロードサイト**
Unity公式サイトがアクセスできない場合:

1. **Unity Archives**: https://unity3d.com/get-unity/download/archive
2. **Unity China**: https://unity.cn/ (中国版)
3. **GitHub Mirror**: 一部のミラーサイトで配布

### 📦 **最小インストール構成**
Unity インストール時に選択する項目:

✅ **必須**:
- Unity Editor 2022.3 LTS
- Microsoft Visual Studio Community (Windows)
- Windows Build Support (IL2CPP)

⭕ **オプション**:
- Documentation
- Example Projects
- Android Build Support (モバイル対応時)
- iOS Build Support (iOS対応時)

### 🔧 **インストール後設定**

#### 1. プロジェクト開く
```bash
# Unity Hub で「プロジェクトを追加」
# パス: unity_avatar/aituber_3d/
```

#### 2. 必要パッケージ自動インストール
Unity初回起動時に自動でインストールされます:
- VRM (VRMアバター用)
- TextMeshPro (UI表示用)
- DOTween (アニメーション用)

#### 3. フォント設定（重要）
大容量フォントファイルが除外されている場合:

1. **Window > TextMeshPro > Font Asset Creator**
2. **フォントファイル**: Windowsシステムフォント（メイリオ等）を使用
3. **文字セット**: 「Characters from File」で日本語文字を含める
4. **Generate Font Atlas**: フォントアセット生成

### ⚡ **動作確認手順**
1. Unity プロジェクト開く
2. **Play** ボタン押下
3. 日本語UI が正常表示されることを確認
4. 質問入力欄でテスト入力

### 🚨 **トラブルシューティング**

#### エラー: "Package resolution error"
```bash
# Unity Package Manager で手動インストール
Window > Package Manager
> VRM: https://github.com/vrm-c/UniVRM.git?path=/Assets/VRM
```

#### エラー: "Assembly definition errors"
```bash
# プロジェクト全体をリビルド
Assets > Reimport All
```

#### 日本語文字化け
```bash
# フォントアセット再作成
Window > TextMeshPro > Font Asset Creator
```

---

**💡 重要**: Unity のダウンロードやインストールで問題が発生した場合は、システム管理者に相談するか、VPN経由でのアクセスを試してください。