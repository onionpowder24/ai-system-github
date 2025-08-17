using UnityEngine;
using UnityEngine.UI;

public class BackgroundFinder : MonoBehaviour
{
    void Start()
    {
        Debug.Log("=== 全背景オブジェクト検索開始 ===");
        
        // 全てのImageコンポーネントを検索
        Image[] allImages = FindObjectsOfType<Image>();
        
        foreach (Image img in allImages)
        {
            Debug.Log($"オブジェクト: {img.gameObject.name}");
            Debug.Log($"  - アクティブ: {img.gameObject.activeInHierarchy}");
            Debug.Log($"  - スプライト: {(img.sprite != null ? img.sprite.name : "None")}");
            Debug.Log($"  - 親オブジェクト: {(img.transform.parent != null ? img.transform.parent.name : "なし")}");
            Debug.Log("---");
        }
        
        Debug.Log("=== 検索完了 ===");
    }
}