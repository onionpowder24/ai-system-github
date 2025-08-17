# Nitto AI Avatar System

**企業AI対話システム** - Nittoグループ統合報告書ベースの高精度RAGシステム

## 🎯 プロジェクト概要

このシステムは、日東電工株式会社（Nitto）の統合報告書を知識ベースとした、企業情報提供専用のAI対話システムです。Unity 3D VRMアバターとPython APIサーバーを組み合わせ、リアルタイムでの企業情報対話を実現します。

### 主要機能
- **🤖 3D VRMアバター**: Unity基盤のリアルタイム音声対話
- **📊 高精度RAG**: Gemini知能スライド選択システム
- **🔍 ハルシネーション検出**: 品質管理システム
- **🎵 音声合成**: Azure Speech Services統合
- **📈 統合報告書対応**: 全事業領域の包括的回答

## 🏗️ システム構成

```
nitto-ai-system/
├── unity_avatar/          # Unity 3D アバターシステム
├── python_server/         # Python API サーバー
├── docs/                  # ドキュメント
├── setup/                 # インストーラー
└── development_history/   # 開発経緯
```

## ⚡ 技術革新

### 1. Gemini知能スライド選択システム
従来のFAISS検索単体の課題（事業内容質問で役員報酬スライドが選ばれる等）を解決。

**Before**: FAISS → 不適切なスライド選択  
**After**: FAISS → Gemini知能判定 → 最適スライド選択

### 2. 多段階品質管理
- **初回検索**: FAISS/BM25ハイブリッド検索
- **知能選択**: Gemini による意味理解ベース選択
- **品質チェック**: ハルシネーション検出
- **自動再検索**: 不適切時の代替スライド選択

### 3. 包括的知識対応
データサイエンス専門制限を撤廃し、統合報告書全領域に対応：
- 財務情報・業績データ
- 事業戦略・技術情報  
- ESG・ガバナンス
- 経営理念・ビジョン

## 🚀 クイックスタート

### 必要環境
- **Python**: 3.12+
- **Unity**: 2022.3 LTS+
- **API キー**: Google Gemini, Azure Speech Services

### インストール
```bash
# 1. リポジトリクローン
git clone https://github.com/onionpowder24/nitto-ai-system.git
cd nitto-ai-system

# 2. 環境設定
cd setup
python setup_installer.py

# 3. APIキー設定
cp python_server/.env.template python_server/.env
# .envファイルを編集してAPIキーを設定

# 4. サーバー起動
cd python_server
python -m uvicorn src.web.api:app --host 0.0.0.0 --port 7200

# 5. Unity起動
# unity_avatar/aituber_3d/ プロジェクトを Unity で開く
```

## 📋 使用方法

1. **APIサーバー起動**: ポート7200でPython APIサーバーを起動
2. **Unity起動**: アバタープロジェクトを開いてPlay
3. **対話開始**: 画面下部の入力欄に質問を入力
4. **AI応答**: アバターが音声付きで回答

### 推奨テスト質問
- 「Nittoの事業内容は？」
- 「2024年度の売上高は？」  
- 「経営理念を教えて」
- 「データサイエンスグループの活動について」

## 🔧 設定

### API キー設定 (.env)
```bash
# Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here

# Azure Speech Services  
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region

# その他設定
DATABASE_TYPE=sqlite
SQLALCHEMY_DATABASE_URI=sqlite:///./aituber.db
```

## 📚 開発経緯

本システムは「その場しのぎではなく本質的解決」を重視して開発されました。

### 主要な技術的ブレークスルー

#### 1. FAISS検索品質問題の本質的解決
**問題**: 「事業内容」質問でslide_65（役員報酬）が1位選択される異常  
**解決**: Gemini知能選択システムで15候補から最適スライドを選択

#### 2. ハルシネーション完全無効化問題の解決  
**問題**: `if False:` でチェック機能が停止  
**解決**: 適切なハルシネーション検出システムの復活と品質向上

#### 3. 専門分野制限の撤廃
**問題**: 「データサイエンスが専門だから財務は答えられない」  
**解決**: 統合報告書全領域対応で包括的回答実現

### 開発哲学
- **本質重視**: 個別対応ではなく根本原因の解決
- **品質第一**: 複数段階での品質管理システム
- **包括性**: 企業情報の全領域対応
- **拡張性**: 他企業への応用可能な設計

## 🤝 コントリビューション

このプロジェクトはNitto データサイエンスグループによって開発されました。

### 連絡先
- **GitHub**: [@onionpowder24](https://github.com/onionpowder24)
- **プロジェクト**: Nitto AI Avatar System

## 📄 ライセンス

このプロジェクトは企業情報提供目的で開発されています。  
商用利用については事前にお問い合わせください。

---

**🎉 Achievement**: 役員報酬スライドが事業内容で選ばれる問題から、適切なスライド選択システムへの完全進化を達成！