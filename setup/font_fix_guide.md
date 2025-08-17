# 日本語フォント修正ガイド

## 🔤 大容量フォントファイル除外への対応

### 📋 **問題の説明**
GitHubの100MBファイル制限により、以下のファイルが除外されています：
```
unity_avatar/aituber_3d/Assets/Font/MPLUS1p-Regular SDF.asset (130.88 MB)
```

### ⚠️ **影響範囲**
- Unity UI の日本語テキストが □□□ で表示
- 質問入力欄の文字化け
- アバター応答テキストの表示不良
- システム全体のユーザビリティ低下

## 🔧 **修正手順（推奨）**

### 方法1: TextMeshPro Font Asset 再作成

#### 1. Unity プロジェクト開く
```bash
unity_avatar/aituber_3d/ をUnity 2022.3で開く
```

#### 2. Font Asset Creator 起動
```
Window > TextMeshPro > Font Asset Creator
```

#### 3. フォント設定
- **Source Font File**: 日本語対応フォントを選択
  - Windows: `C:\Windows\Fonts\meiryo.ttc` (メイリオ)
  - または: `C:\Windows\Fonts\NotoSansCJK-Regular.ttc`
- **Sampling Point Size**: 42
- **Padding**: 5
- **Packing Method**: Optimum

#### 4. 文字セット設定
- **Character Set**: Characters from File
- **Character File**: 以下の内容でテキストファイル作成
```
あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん
アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン
0123456789
！？「」、。ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
こんにちはNittoの事業内容は売上高営業利益について教えてください申し訳ございませんが
データサイエンスグループ活動政策質問回答音声合成テストシステム
```

#### 5. Generate Font Atlas
- **Generate Font Atlas** ボタンクリック
- 生成完了後、**Save as** で保存: `Assets/Font/MPLUS1p-Regular SDF`

### 方法2: 既存フォント置換

#### 1. Windowsシステムフォント使用
```bash
# Unity Project Settings
Edit > Project Settings > XR Plug-in Management
```

#### 2. UI要素の手動設定
各UI TextMeshPro コンポーネントで：
- **Font Asset**: 新しく作成したフォントを設定
- **Material**: 自動生成されたマテリアルを使用

## 🚀 **自動修正スクリプト**

Unity Editor用の自動修正スクリプト：

```csharp
// Assets/Editor/FontFixer.cs
using UnityEngine;
using UnityEditor;
using TMPro;

public class FontFixer : EditorWindow
{
    [MenuItem("Tools/Fix Japanese Font")]
    static void FixJapaneseFont()
    {
        // 全てのTextMeshProコンポーネントを検索
        TextMeshProUGUI[] texts = FindObjectsOfType<TextMeshProUGUI>();
        
        // デフォルトフォントを設定
        TMP_FontAsset defaultFont = Resources.Load<TMP_FontAsset>("Fonts & Materials/LiberationSans SDF");
        
        foreach (var text in texts)
        {
            text.font = defaultFont;
            EditorUtility.SetDirty(text);
        }
        
        Debug.Log($"Fixed {texts.Length} TextMeshPro components");
    }
}
```

## 📋 **検証手順**

### 1. 動作確認
1. Unity Play モード開始
2. 質問入力欄に「こんにちは」入力
3. 日本語文字が正常表示されることを確認

### 2. 全UI要素チェック
- ✅ 質問入力欄
- ✅ 応答表示エリア  
- ✅ スライド画像のタイトル
- ✅ システムメッセージ

### 3. アバター対話テスト
1. 「Nittoの事業内容は？」と入力
2. アバターが音声付きで回答
3. UI上でも適切に日本語表示

## 🔄 **代替手法**

### Git LFS使用（上級者向け）
```bash
# Git Large File Storage セットアップ
git lfs install
git lfs track "*.asset"
git add .gitattributes
git add Assets/Font/MPLUS1p-Regular\ SDF.asset
git commit -m "Add large font file with LFS"
```

### 分割ダウンロード
大容量ファイルを別途配布：
- Google Drive
- Dropbox  
- 専用ファイルサーバー

---

**⚡ 重要**: フォント修正は Unity プロジェクトの完全動作に必須です。上記手順で必ず対応してください。