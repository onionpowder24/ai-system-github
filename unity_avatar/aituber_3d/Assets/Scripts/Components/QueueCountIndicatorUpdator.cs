using System.Collections;
using System.Collections.Generic;
using Aituber;
using TMPro;
using UnityEngine;

public class QueueCountIndicatorUpdator : MonoBehaviour
{
    [SerializeField]
    private QueueIndicator queueIndicator;

    [SerializeField]
    private TMPro.TextMeshProUGUI counterLabel;

    private void Start()
    {
        // 受付済のご質問BOX全体を非表示にする
        this.gameObject.SetActive(false);
    }

    private void Update()
    {
        // 何もしない（BOX自体が非表示なので）
    }
}
