import pathlib
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings

load_dotenv(override=True)


class Settings(BaseSettings):
    """Settings for python_server"""

# YouTube関連設定は削除済み
    ELEVENLABS_API_KEY: str
    AZURE_SPEECH_KEY: str

    PROJECT_ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent.parent
    AITUBER_3D_ROOT: pathlib.Path = PROJECT_ROOT / "aituber_3d"
    PYTHON_SERVER_ROOT: pathlib.Path = PROJECT_ROOT / "python_server"
    FAISS_QA_DB_DIR: pathlib.Path = PYTHON_SERVER_ROOT / "faiss_qa"
    FAISS_KNOWLEDGE_DB_DIR: pathlib.Path = PYTHON_SERVER_ROOT / "faiss_knowledge"
    BM25_KNOWLEDGE_DB_DIR: pathlib.Path = PYTHON_SERVER_ROOT / "bm25_knowledge_manifest_demo_csv_db"

    GOOGLE_API_KEY: str  # Gemini用

    # Database configuration
    DATABASE_TYPE: str = "postgresql"  # "postgresql" or "sqlite"
    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "password"
    PG_DATABASE: str = "aituber_dev"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_TYPE.lower() == "sqlite":
            db_path = self.PYTHON_SERVER_ROOT / "aituber.db"
            return f"sqlite:///{db_path}"
        else:
            return f"postgresql+psycopg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}"

    LOCAL_TZ: ZoneInfo = ZoneInfo("Asia/Tokyo")


settings = Settings()
