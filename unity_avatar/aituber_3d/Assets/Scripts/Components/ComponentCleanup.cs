using UnityEngine;

namespace Aituber
{
    /// <summary>
    /// 削除されたコンポーネントの参照を検出・無効化するクリーンアップスクリプト
    /// </summary>
    public class ComponentCleanup : MonoBehaviour
    {
        void Start()
        {
            // シーン内のすべてのGameObjectをチェック
            GameObject[] allObjects = FindObjectsOfType<GameObject>();
            
            foreach (GameObject obj in allObjects)
            {
                // 削除されたコンポーネントを検出
                Component[] components = obj.GetComponents<Component>();
                
                for (int i = 0; i < components.Length; i++)
                {
                    if (components[i] == null)
                    {
                        Debug.LogWarning($"Missing component detected on GameObject: {obj.name}");
                    }
                }
                
                // YouTubeChatDisplayとGetCommentFromOneコンポーネントを探して無効化
                MonoBehaviour[] monoBehaviours = obj.GetComponents<MonoBehaviour>();
                foreach (MonoBehaviour mb in monoBehaviours)
                {
                    if (mb != null)
                    {
                        string typeName = mb.GetType().Name;
                        if (typeName == "YouTubeChatDisplay" || typeName == "GetCommentFromOne")
                        {
                            Debug.LogWarning($"Disabling obsolete component {typeName} on {obj.name}");
                            mb.enabled = false;
                        }
                    }
                }
            }
        }
    }
}