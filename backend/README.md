# Smart Shiksha AI Backend

Python FastAPI backend for Smart Shiksha intelligent tutoring system.

## Features

- 🤖 AI Tutor with RAG (Retrieval Augmented Generation)
- 🎓 Education-only content filtering
- 🌍 Multilingual support (10+ Indian languages) using LibreTranslate
- 📚 6000+ medical education questions
- 🔍Vector-based semantic search
- ✅ Quiz generation system

## Installation

1. **Install Python 3.9+**

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   - Copy `.env` file and update if needed
   - Default uses free LibreTranslate API

4. **Start the server:**

   ```bash
   python main.py
   ```

   Server will run on `http://localhost:8000`

## First Run

On first run, the system will:

1. Load 6000+ questions from JSONL file
2. Generate embeddings (takes 5-10 minutes)
3. Store in ChromaDB for fast retrieval

Subsequent runs will be instant!

## API Endpoints

### Chat

```bash
POST /chat
{
  "message": "What is the function of the heart?",
  "language": "en",
  "subject": "Anatomy"
}
```

### Translate

```bash
POST /translate
{
  "text": "Hello",
  "source_lang": "en",
  "target_lang": "hi"
}
```

### Generate Quiz

```bash
POST /quiz/generate
{
  "subject": "Anatomy",
  "num_questions": 10
}
```

### Get Subjects

```bash
GET /subjects
```

### Get Topics

```bash
GET /topics/Anatomy
```

### Get Statistics

```bash
GET /stats
```

## Supported Languages

- English (en)
- Hindi (hi) - हिंदी
- Tamil (ta) - தமிழ்
- Telugu (te) - తెలుగు
- Bengali (bn) - বাংলা
- Marathi (mr) - मराठी
- Gujarati (gu) - ગુજરાતી
- Kannada (kn) - ಕನ್ನಡ
- Malayalam (ml) - മലയാളം
- Punjabi (pa) - ਪੰਜਾਬੀ

## Architecture

- **FastAPI**: Modern Python web framework
- **ChromaDB**: Vector database for semantic search
- **Sentence Transformers**: Generate embeddings
- **LibreTranslate**: Free translation API
- **LangChain**: AI agent framework (optional)

## Testing

```bash
# Health check
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain photosynthesis"}'
```

## Notes

- First run takes time to build vector index
- ChromaDB persists to `./chroma_db` directory
- Uses free LibreTranslate API (no limits!)
- All medical data from NEET MedMCQA dataset
