import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "Smart Shiksha AI Backend"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "smart_shiksha"
    
    # LibreTranslate Configuration
    LIBRETRANSLATE_URL: str = "https://libretranslate.com/translate"
    LIBRETRANSLATE_API_KEY: str = ""  # Optional, for hosted service
    
    # AI Model Configuration
    OPENAI_API_KEY: str = ""  # Optional, leave empty to use local model
    USE_LOCAL_MODEL: bool = True  # Set to False to use OpenAI
    LOCAL_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Groq API Configuration
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Ollama Configuration
    USE_OLLAMA: bool = True
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    
    # Vector Database Configuration
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "education_qa"
    
    # JSONL Data Path
    JSONL_DATA_PATH: str = "./questions.jsonl"
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",
    ]
    
    # Education Filter Configuration
    EDUCATION_KEYWORDS: list = [
        "learn", "study", "education", "teach", "exam", "test", "quiz",
        "anatomy", "medicine", "surgery", "physics", "chemistry", "biology",
        "mathematics", "history", "geography", "programming", "computer",
        "science", "language", "grammar", "literature", "economics"
    ]
    
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        case_sensitive = True

settings = Settings()
