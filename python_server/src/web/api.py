import datetime
import pathlib
import random
from collections.abc import Iterator

import uvicorn
from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import ORJSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.config import settings
from src.databases.engine import session_scope
from src.get_faiss_vector import get_multiple_qa
from src.gpt import DocumentRetrievalType, generate_hallucination_response, generate_response
from src.logger import setup_logger
# YouTube関連リポジトリは削除済み
from src.schema.hallucination import HallucinationRequest, HallucinationResponse
from src.templates import TEMPLATE_MESSAGES, TEMPLATE_QUESTIONS
from src.text_to_speech import TextToSpeech
# YouTube関連はすべて削除済み

setup_logger()


# フィルタリング機能削除済み


app = FastAPI(
    default_response_class=ORJSONResponse,
)
# proxy機能は削除済み


# 現在の時刻を取得し、1時間ごとのファイル名を生成
current_time = datetime.datetime.now(tz=settings.LOCAL_TZ)

t_fmt = current_time.strftime("%Y%m%d_%H%M%S")
log_filename_json = pathlib.Path(__file__).parent.parent.parent / "log" / f"log_{t_fmt}.json"
log_filename_csv = pathlib.Path(__file__).parent.parent.parent / "log" / f"log_{t_fmt}.csv"


def get_session(request: Request) -> Iterator[Session]:
    """Get session from Session Local"""
    with session_scope() as session:
        yield session


@app.post("/reply")
async def reply(inputtext: str = Form(...)):
    """GPT に問い合わせた回答結果を取得する"""
    res1, res2 = await generate_response(
        text=inputtext, log_filename_json=log_filename_json, log_filename_csv=log_filename_csv, doc_retrieval_type=DocumentRetrievalType.multi, check_hal=True
    )

    if isinstance(res1, bytes):
        res1 = res1.decode("utf-8")
    if isinstance(res2, bytes):
        res2 = res2.decode("utf-8")

    response = {"response_text": res1, "image_filename": res2}

    return ORJSONResponse(content=response)


# YouTube Live関連のエンドポイントは削除済み（使用しない方針のため）


@app.api_route("/voice", methods=["POST"], response_class=Response)
async def voice(request: Request):
    """テキストを音声に変換する"""
    # NOTE: クエリパラメータから受け取るのが気持ち悪いが、unity側での修正が必要なので一旦既存実装を踏襲する
    text = request.query_params["text"]

    text_to_speech = TextToSpeech()

    audio = await text_to_speech.text_to_speech_stream(text)

    return Response(content=audio, media_type="audio/wav")


@app.api_route("/voice/v2", methods=["POST"], response_class=Response)
async def voice_v2(request: Request):
    """テキストを音声に変換する"""
    # NOTE: クエリパラメータから受け取るのが気持ち悪いが、unity側での修正が必要なので一旦既存実装を踏襲する
    text = request.query_params["text"]

    text_to_speech = TextToSpeech()

    audio = await text_to_speech.text_to_speech_with_azure_tts(text)

    return Response(content=audio, media_type="audio/wav")


@app.api_route("/voice/azure", methods=["POST"], response_class=Response)
async def voice_azure(request: Request):
    """テキストを音声に変換する"""
    # NOTE: クエリパラメータから受け取るのが気持ち悪いが、unity側での修正が必要なので一旦既存実装を踏襲する
    text = request.query_params["text"]

    text_to_speech = TextToSpeech()

    audio = await text_to_speech.azure_text_to_speech(text)

    return Response(content=audio, media_type="audio/wav")


@app.api_route("/voice/male", methods=["POST"], response_class=Response)
async def voice_male(request: Request):
    """テキストを音声に変換する"""
    # NOTE: クエリパラメータから受け取るのが気持ち悪いが、unity側での修正が必要なので一旦既存実装を踏襲する
    text = request.query_params["text"]

    text_to_speech = TextToSpeech()

    audio = await text_to_speech.azure_text_to_speech(text, voice_name="ja-JP-KeitaNeural")

    return Response(content=audio, media_type="audio/wav")


@app.get("/get_info")
async def get_information(
    query: str = Query(..., description="The query text for which to retrieve related information."), top_k: int = Query(5, description="The number of top results to retrieve.")
):
    """Retrieve and return information related to the provided query text using RAG."""
    try:
        # 一時的にFAISS QAを無効化してGeminiテスト
        # qa_items = get_multiple_qa(query=query, top_k=top_k)
        qa_items = ["FAQ: Nittoの事業・技術についてお気軽にご質問ください。"]
    except Exception as e:
        # エラーハンドリング: RAG情報の取得に失敗した場合
        raise HTTPException(status_code=500, detail=f"Failed to retrieve information: {str(e)}") from e
    # 関連情報をJSON形式で返す
    return {"query": query, "qa_items": qa_items}




@app.post("/hallucination")
async def hallucination(request: HallucinationRequest) -> HallucinationResponse:
    """ハルシネーション判定を実施"""
    res = await generate_hallucination_response(text=request.text, doc_retrieval_type=DocumentRetrievalType.multi)
    return res


@app.get("/template_message")
async def get_template_message():
    """テンプレートメッセージを取得する

    テンプレートメッセージ: youtube上でユーザーのコメントがないときに読み上げるメッセージ
    """
    message = random.choice(TEMPLATE_MESSAGES)  # noqa: S311
    return ORJSONResponse(content={"message": message})


@app.get("/template_question")
async def get_template_question():
    """テンプレート質問を取得する

    テンプレート質問: youtube上でユーザーのコメントがないときに読み上げる質問
    """
    question = random.choice(TEMPLATE_QUESTIONS)  # noqa: S311
    return ORJSONResponse(content={"question": question})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7200)
