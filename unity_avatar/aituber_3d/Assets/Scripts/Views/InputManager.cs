using TMPro;
using UnityEngine;

namespace Aituber
{
    public class InputManager : MonoBehaviour
    {
        public TMP_InputField inputField;
        public QueueManager queueManager;

        void Start()
        {
            inputField.onEndEdit.AddListener(HandleEndEdit);
        }

        private void HandleEndEdit(string text)
        {
            Debug.Log("InputManager.HandleEndEdit called with: " + text);
            if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
            {
                Debug.Log("Enter key detected in InputManager, adding to queue...");
                if (queueManager != null)
                {
                    queueManager.AddTextToQueue(new Question(text,"ユーザー","Sprites/usericon_noname",false));
                }
                else
                {
                    Debug.LogError("QueueManager is null in InputManager!");
                }
            }
        }
    }
}