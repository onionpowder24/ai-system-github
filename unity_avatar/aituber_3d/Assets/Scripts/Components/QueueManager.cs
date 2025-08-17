using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using UnityEngine.UI;
using System.IO;
using System;
using System.Linq;
using Cysharp.Threading.Tasks;
using Assets.Scripts.Components;
using UnityEditor;

namespace Aituber
{
    public class QueueManager : MonoBehaviour
    {
        private const string REPLY_URL = Constants.SERVER_BASE_URL + "/reply";
        private const string DEFAULT_QUESTION_URL = Constants.SERVER_BASE_URL + "/template_question";
        private const string TEMPLATE_MESSAGE_URL = Constants.SERVER_BASE_URL + "/template_message";
        public TextMeshProUGUI responseText;
        public Button fetchCommentsButton;
        public Button stopChatButton;
        public Button loadCSVButton;
        public TextToSpeech textToSpeech;
        public TMP_InputField inputField;
        public NewCommentIndicatorQueue newCommentIndicatorQueue;

        public QueueIndicator queueIndicator;


        // フィルタリング関連の設定項目類

        public int minQuestionCountToQueueAutoQuestions = 5;

        public int minSecondsToEnqueueAutoQuestions = 15;

        public float defaultQuestionRatio = 0.8f;

        public int maxBackoffRetryCount = 5;


        private Queue<Question> inputQueue = new Queue<Question>();
        private Queue<Question> approvedQuestionsQueue = new Queue<Question>();

        private bool isStopped = false; // 停止ボタンが押された状態を示すフラグ（デフォルトで処理開始）

        private Color originalButtonColor;

        private string stopWordsDirectoryPath = "Text";
        private List<string> stopWords = new List<string>();

        public CommentPanelManager commentPanelManager;

        public string restext;
        public string csvFilePath = "Assets/Resources/CSV/demo_questions.csv"; // テスト用CSVファイル

        private string staticResponse = "なるほどですね！皆さんの声を聞かせていただき、ありがとうございます";

        private Speech currentSpeech = null;


        List<string> request_q = new List<string> {"ほしい", "欲しい"};

        List<string> requestingQuestionsMessage = new List<string>()
        {
            "東京都民の皆さん、東京都知事候補の安野です。質問があればYoutubeコメントで聞いてください。",
            "質問はありませんか?",
            "私は安野の政策を学習したAIです。様々な質問に対してお答えいたします!"
        };


        void Start()
        {
            // 停止ボタンのクリックイベントにリスナーを追加
            stopChatButton.onClick.AddListener(StopQueueProcessing);

            // 開始ボタンのクリックイベントにリスナーを追加
            fetchCommentsButton.onClick.AddListener(StartQueueProcessingFromButton);

            // 停止ボタンの元の色を記憶
            originalButtonColor = stopChatButton.GetComponent<Image>().color;

            // InputFieldのイベントにリスナーを追加
            inputField.onEndEdit.AddListener(HandleEndEdit);

            // loadCSVButtonのクリックイベントにリスナーを追加
            loadCSVButton.onClick.AddListener(ReadCSVAndQueueQuestions);

            // Resourcesフォルダ内のTextフォルダ直下のテキストファイルをすべて取得
            TextAsset[] textFiles = Resources.LoadAll<TextAsset>(stopWordsDirectoryPath);
            if (textFiles != null && textFiles.Length > 0)
            {
                foreach (var textFile in textFiles)
                {
                    var words = textFile.text.Split('\n')
                        .Select(word => word.Trim())
                        .Where(word =>
                            !string.IsNullOrEmpty(word) && !word.StartsWith("//")); // 行の先頭に"//"がある場合は無視（ストップされない）

                    stopWords.AddRange(words);
                }
            }

            ProcessSimpleInputQueue();
            ProcessReplyGenerateAsync();
            ProcessSpeech();
            ProcessAutoQuestions();
        }

        void OnDestroy()
        {
            // オブジェクト破棄時にイベントリスナーを解除
            stopChatButton.onClick.RemoveListener(StopQueueProcessing);
            fetchCommentsButton.onClick.RemoveListener(StartQueueProcessingFromButton);
            inputField.onEndEdit.RemoveListener(HandleEndEdit);
            loadCSVButton.onClick.RemoveListener(ReadCSVAndQueueQuestions);
        }

        void Update()
        {
            var cpm = GameObject.Find("CommentPanelManager").GetComponent<CommentPanelManager>();
            if (!textToSpeech.isSpeaking && textToSpeech.HasNext())
            {
                textToSpeech.PlayNext();
            }

            if (textToSpeech.isSpeaking && textToSpeech.currentSpeech != null)
            {
                if (currentSpeech != textToSpeech.currentSpeech)
                {
                    cpm.ShowUserComment(textToSpeech.currentSpeech.Conversation.question.question,
                        textToSpeech.currentSpeech.Conversation.question.userName,
                        textToSpeech.currentSpeech.Conversation.question.imageIcon);
                    currentSpeech = textToSpeech.currentSpeech;
                }
            }
            else
            {
                //commentPanel.SetActive(false);
            }
        }

        private async UniTask ProcessSpeech()
        {
            while (true)
            {
                if (textToSpeech.HasNext())
                {
                    await textToSpeech.PlayNext();
                    await UniTask.Delay(TimeSpan.FromSeconds(1));
                }
                else
                {
                    await UniTask.Delay(TimeSpan.FromSeconds(1));
                }
            }
        }

        private async UniTask ProcessAutoQuestions()
        {
            while (true)
            {
                bool hasEnoughQuestionsInQueue = true;
                for (int i = 0; i < Math.Max(1,this.minSecondsToEnqueueAutoQuestions) * 10; i++)
                {
                    if (queueIndicator != null && this.minQuestionCountToQueueAutoQuestions > queueIndicator.QueueLength)
                    {
                        hasEnoughQuestionsInQueue = false;
                    }

                    await UniTask.Delay(TimeSpan.FromSeconds(0.1f));
                }

                if (hasEnoughQuestionsInQueue)
                {
                    continue;
                }

                var randValue = UnityEngine.Random.Range(0f, 1f);
                if (randValue < this.defaultQuestionRatio)
                {
                    while (true)
                    {
                        try
                        {
                            using (UnityWebRequest getDefaultReq = UnityWebRequest.Get(DEFAULT_QUESTION_URL))
                            {
                                await getDefaultReq.SendWebRequest();
                                if (getDefaultReq.result == UnityWebRequest.Result.Success)
                                {
                                    var responseText = getDefaultReq.downloadHandler.text;

                                    var decodedResponse = JsonUtility.FromJson<DefaultQuestionResponse>(responseText);
                                    this.GenerateApprovedDefaultQuestion(decodedResponse.question);
                                    break;
                                }
                            }
                        }
                        catch (Exception e)
                        {
                            Debug.LogWarning(e);
                            await UniTask.Delay(TimeSpan.FromSeconds(1));
                        }
                    }
                }
                else
                {
                    while (true)
                    {
                        try
                        {
                            using (UnityWebRequest getDefaultReq = UnityWebRequest.Get(TEMPLATE_MESSAGE_URL))
                            {
                                await getDefaultReq.SendWebRequest();
                                if (getDefaultReq.result == UnityWebRequest.Result.Success)
                                {
                                    var responseText = getDefaultReq.downloadHandler.text;

                                    var decodedResponse = JsonUtility.FromJson<TemplateMessageResponse>(responseText);
                                    this.GenerateTemplateMessage(decodedResponse.message);
                                    break;
                                }
                            }
                        }
                        catch (Exception e)
                        {
                            Debug.LogWarning(e);
                            await UniTask.Delay(TimeSpan.FromSeconds(1));
                        }
                    }
                }

            }
        }


        private void StopQueueProcessing()
        {
            // 処理を停止
            isStopped = true;

            // 停止ボタンの色を変更
            stopChatButton.GetComponent<Image>().color = Color.red;
        }

        private void StartQueueProcessingFromButton()
        {
            // 処理を再開
            isStopped = false;
        }

        public void AddTextToQueue(Question q)
        {
            Debug.Log("AddTextToQueue called with question: " + q?.question);
            // 新しいテキストをキューに追加
            if (!string.IsNullOrEmpty(q.question))
            {
                inputQueue.Enqueue(q);
                Debug.Log("Info: Add to Queue - " + q + ", Queue count: " + inputQueue.Count);
            }
            else
            {
                Debug.LogWarning("Question is null or empty!");
            }
        }

        /// <summary>
        /// 入力キューを監視し、すべての質問を直接承認キューに移動（フィルタリングなし）
        /// </summary>
        /// <returns></returns>
        async void ProcessSimpleInputQueue()
        {
            while (true)
            {
                while (inputQueue.Count > 0)
                {
                    var q = inputQueue.Dequeue();
                    this.approvedQuestionsQueue.Enqueue(q);
                    this.newCommentIndicatorQueue.questions.Enqueue(q);
                    if (this.queueIndicator != null)
                        this.queueIndicator.AppendInIndicator(q);
                    
                    Debug.Log("Info: Question approved directly - " + q.question);
                }

                await UniTask.Delay(TimeSpan.FromSeconds(0.1f));
            }
        }

        /// <summary>
        /// フィルタ済みのコメントへの返信を考えてTextToSpeechのQueueに入れておく
        /// </summary>
        /// <returns></returns>
        async UniTask ProcessReplyGenerateAsync()
        {
            while (true)
            {
                Debug.Log($"ProcessReply: Queue={approvedQuestionsQueue.Count}, Capacity={textToSpeech.HasCapacityToEnqueue()}, isStopped={isStopped}");
                if (approvedQuestionsQueue.Count > 0 && textToSpeech.HasCapacityToEnqueue())
                {
                    Question nextQuestion = null;
                    if (hasQuestionFromUser(approvedQuestionsQueue))
                    {
                        while (this.approvedQuestionsQueue.Count > 0)
                        {
                            var nextQuestionCand = this.approvedQuestionsQueue.Dequeue();
                            if (!nextQuestionCand.isAutoQuestion) // 自動生成ではない質問
                            {
                                nextQuestion = nextQuestionCand;
                                break;
                            }
                            else
                            {
                                Debug.Log("Skipping auto question:" + nextQuestionCand.question);
                                if (this.queueIndicator != null)
                                    this.queueIndicator.RemoveFromIndicator(nextQuestionCand);
                            }
                        }
                    }
                    else
                    {
                        nextQuestion = approvedQuestionsQueue.Dequeue();
                    }

                    if (StringHelper.ContainsAny(nextQuestion.question, request_q.ToList()))
                    {
                        await UniTask.Delay(TimeSpan.FromSeconds(1)); // 1秒待機
                        textToSpeech.EnqueueConversation(new Conversation(nextQuestion, staticResponse, "slide_1"));
                    }
                    else
                    {
                        await RequestReply(REPLY_URL, nextQuestion);
                    }
                }

                await UniTask.Delay(TimeSpan.FromSeconds(1));
            }
        }

        async UniTask RequestReply(string url, Question question)
        {
            int currentWaitTimeInSeconds = 1;
            for (var attempt = 0; attempt < maxBackoffRetryCount; attempt++)
            {
                try
                {
                    // 指定されたURLにテキストデータをPOSTリクエストで送信し、結果を表示
                    WWWForm form = new WWWForm();
                    form.AddField("inputtext", question.question);
                    using (UnityWebRequest webRequest = UnityWebRequest.Post(url, form))
                    {
                        await webRequest.SendWebRequest();
                        if (webRequest.result == UnityWebRequest.Result.Success)
                        {
                            string res = webRequest.downloadHandler.text;

                            // JSONレスポンスをパース
                            var responseData = JsonUtility.FromJson<ReplyResponseData>(res);

                            // 各フィールドのデータを取得
                            restext = responseData.response_text;
                            var image_filename = responseData.image_filename;


                            string restextFullKana = KanaConverter.ConvertHalfWidthToFullWidthKana(restext);
                            string restextHanAlp = HankakuAlphabet.ConvertZenkakuToHankaku(restextFullKana);


                            if (!stopWords.Any(word => restextHanAlp.Contains(word)))
                            {
                                Debug.Log("Info: No StopWord. - " + restextHanAlp);
                                textToSpeech.EnqueueConversation(new Conversation(question, restextHanAlp,
                                    image_filename));
                            }
                            else
                            {
                                Debug.Log("Info: Is StopWord. - " + restextHanAlp);
                                textToSpeech.EnqueueConversation(new Conversation(question, restextHanAlp,
                                    image_filename));
                            }

                            break;
                        }
                        else
                        {
                            await UniTask.Delay(TimeSpan.FromSeconds(currentWaitTimeInSeconds));
                            currentWaitTimeInSeconds *= 2;
                        }
                    }
                }
                catch (Exception ex)
                {
                    Debug.LogException(ex);
                    await UniTask.Delay(TimeSpan.FromSeconds(currentWaitTimeInSeconds));
                    currentWaitTimeInSeconds *= 2;
                }
            }
        }

        private void HandleEndEdit(string text)
        {
            // InputManagerで処理されるため、重複を避けるため無効化
            /*
            if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
            {
                AddTextToQueue(new Question(text, "名無しさん", "",false));
                inputField.text = ""; // 入力フィールドをクリア

            }
            */
        }


        private void ReadCSVAndQueueQuestions()
        {
            List<QuestionData> questions = null;

            try
            {
                questions = CSVSerializer.Deserialize(csvFilePath);
            }
            catch (FileNotFoundException ex)
            {
                Debug.LogError($"CSV file not found: {ex.Message}");
                // 必要に応じて、UIにエラーメッセージを表示する等の処理を追加
                return;
            }
            catch (Exception ex)
            {
                Debug.LogError($"Error reading CSV file: {ex.Message}");
                // 必要に応じて、UIにエラーメッセージを表示する等の処理を追加
                return;
            }

            if (questions == null || questions.Count == 0)
            {
                Debug.LogError("No questions found in the CSV file.");
                // 必要に応じて、UIにエラーメッセージを表示する等の処理を追加
                return;
            }

            foreach (var questionData in questions)
            {
                Debug.Log("Info: questionData.question - " + questionData.question);
                AddTextToQueue(new Question(questionData.question, "名無しさん", "",true));

            }

            isStopped = false;
        }

        /// <summary>
        /// よくある質問枠として質問を投稿する
        /// </summary>
        /// <param name="question"></param>
        private void GenerateApprovedDefaultQuestion(string question)
        {
            var q = new Question(question, "AIあんの(よくある質問)", "Sprites/usericon_noname", true);
            approvedQuestionsQueue.Enqueue(q);
            if (queueIndicator != null)
                queueIndicator.AppendInIndicator(q);
        }

        private void GenerateTemplateMessage(string message)
        {
            var q = new Question("", "AIあんの(よくある質問)", "Sprites/usericon_noname", true);
            var conv = new Conversation(q, message, "slide_1");
            textToSpeech.EnqueueConversation(conv);
        }

        bool hasQuestionFromUser(Queue<Question> questions)
        {
            var array = questions.ToArray();
            return array.Any(x => !x.isAutoQuestion);
        }
    }

    [System.Serializable]
    public class ReplyResponseData
    {
        public string response_text;
        public string image_filename;
    }


    [System.Serializable]
    class DefaultQuestionResponse
    {
        public string question;
    }

    [System.Serializable]
    class TemplateMessageResponse
    {
        public string message;
    }

    public class Question
    {
        public string question;

        public string userName;

        public string imageIcon;

        public bool isAutoQuestion;

        public GUID id;

        public Question(string question, string userName, string imageIcon, bool isAutoQuestion)
        {
            this.id = GUID.Generate();
            this.question = question;
            this.userName = userName;
            this.imageIcon = imageIcon;
            this.isAutoQuestion = isAutoQuestion;
        }
    }

    /// <summary>
    /// 質問と応答の揃った型。これをもとに音声生成を行う。
    /// </summary>
    public class Conversation
    {
        public Question question;

        public string response;

        public string imageFileName;

        public Conversation(Question question, string response, string imageFileName)
        {
            this.question = question;
            this.response = response;
            this.imageFileName = imageFileName;
        }
    }
}
