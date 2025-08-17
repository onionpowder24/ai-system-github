using UnityEngine;
using UnityEngine.UI;

namespace Aituber
{
    public class SlideDisplayer : MonoBehaviour
    {
        public TextToSpeech textToSpeech;
        public QueueManager queueManager; // QueueManagerの参照
        public Image displayImage; // 表示するImageコンポーネント
        public Sprite defaultSprite; // 画像が無い場合に表示するデフォルトのスプライト

        [System.Diagnostics.CodeAnalysis.SuppressMessage("CodeQuality", "IDE0052")]
        private bool wasSpeaking = false;
        private string prevImage = "";

        void Start()
        {
            if (queueManager == null)
            {
                Debug.LogError("QueueManagerが設定されていません。");
                return;
            }

            // 起動時はスライド1枚目（企業表紙）を表示
            UpdateImage("slide_1");
            
            // 全てのImageコンポーネントを持つオブジェクトを探して政治関連画像を特定
            UnityEngine.UI.Image[] allImages = FindObjectsOfType<UnityEngine.UI.Image>();
            foreach (var img in allImages)
            {
                if (img.sprite != null)
                {
                    Debug.Log($"画像オブジェクト発見: {img.gameObject.name} - スプライト: {img.sprite.name}");
                    
                    // 政治関連キーワードを含む画像を非表示
                    if (img.sprite.name.Contains("安野") || img.sprite.name.Contains("takahiro") || 
                        img.sprite.name.Contains("poster") || img.sprite.name.Contains("manifesto"))
                    {
                        img.gameObject.SetActive(false);
                        Debug.Log($"政治関連画像を非表示: {img.gameObject.name}");
                    }
                }
            }
        }

        void Update()
        {
            if (textToSpeech != null)
            {
                // 現在話している内容がある場合はそのスライドを表示
                if (textToSpeech.currentTalkSegment?.slidePath != null)
                {
                    var currentSlide = textToSpeech.currentTalkSegment.slidePath;
                    if (currentSlide != prevImage)
                    {
                        prevImage = currentSlide;
                        UpdateImage(currentSlide);
                    }
                }
                // アイドル時は最後のスライドを保持（初回起動時のみslide_1表示）
                else if (string.IsNullOrEmpty(prevImage))
                {
                    prevImage = "slide_1";
                    UpdateImage("slide_1");
                }
            }
        }

        public void UpdateImage(string fileName)
        {
            string replacedFilename = fileName.Replace(".png", "");
            
            string imageFilename;
            // inovasの場合は image/フォルダから読み込み
            if (replacedFilename == "inovas")
            {
                imageFilename = "image/inovas";
            }
            // ファイル名がすでにnitto_PDF/を含む場合は、Slides/のみ追加
            else if (replacedFilename.StartsWith("nitto_PDF/"))
            {
                imageFilename = "Slides/" + replacedFilename;
            }
            else
            {
                imageFilename = "Slides/nitto_PDF/" + replacedFilename;
            }
            Debug.Log("Display Slide: " + imageFilename);

            if (!string.IsNullOrEmpty(imageFilename))
            {
                // Resourcesフォルダから画像を読み込む（Texture2D経由でSprite作成）
                Texture2D texture = Resources.Load<Texture2D>(imageFilename);
                if (texture != null)
                {
                    Sprite newSprite = Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height), new Vector2(0.5f, 0.5f), 100f);
                    // テクスチャフィルタリング改善
                    texture.filterMode = FilterMode.Trilinear;
                    displayImage.sprite = newSprite;
                    displayImage.color = Color.white; // 透明度修正
                    displayImage.enabled = true;
                    Debug.Log($"画像表示成功: {imageFilename}");
                }
                else
                {
                    Debug.LogError($"画像ファイルが見つかりません: {imageFilename}");
                    SetDefaultSlide();
                }
            }
            else
            {
                SetDefaultSlide();
            }
        }

        public void SetDefaultSlide()
        {
            displayImage.sprite = defaultSprite;
            displayImage.enabled = (defaultSprite != null);
            if (defaultSprite == null)
            {
                Debug.LogWarning("デフォルトのスプライトが設定されていません。");
            }
        }

        public void HideSlide()
        {
            displayImage.enabled = false;
        }
    }
}