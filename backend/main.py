from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from config import settings
from ai_tutor import ai_tutor
from translator import translation_service
from data_processor import data_processor
import uvicorn
import pdfplumber
import io

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI-powered educational tutoring system with multilingual support"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # More permissive for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for requests/responses
class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "en"
    subject: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    is_educational: bool
    sources: List[dict] = []
    original_language: str = "en"

class TranslateRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "hi"

class TranslateResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str

class QuizRequest(BaseModel):
    subject: Optional[str] = None
    topic: Optional[str] = None
    num_questions: int = 10

class QuizResponse(BaseModel):
    questions: List[dict]
    subject: Optional[str] = None

# Startup event to initialize AI tutor
@app.on_event("startup")
async def startup_event():
    """Initialize AI tutor on startup"""
    print("Starting up Smart Shiksha AI Backend...")
    ai_tutor.initialize()
    print("Backend ready!")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Smart Shiksha AI Backend",
        "version": settings.API_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_initialized": ai_tutor.is_initialized,
        "data_loaded": len(data_processor.data) > 0
    }

# Chat endpoint (main AI tutor interface)
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint with AI tutor
    Supports education-only queries with multilingual support
    """
    try:
        user_message = request.message
        target_lang = request.language or "en"
        
        # Translate to English if needed
        if target_lang != "en":
            user_message = await translation_service.translate(
                user_message,
                source_lang=target_lang,
                target_lang="en"
            )
        
        # Generate response
        response = await ai_tutor.generate_response(
            query=user_message,
            language=target_lang,
            subject_filter=request.subject
        )
        
        answer = response["answer"]
        
        # Translate answer back to target language
        if target_lang != "en":
            answer = await translation_service.translate(
                answer,
                source_lang="en",
                target_lang=target_lang
            )
        
        return ChatResponse(
            answer=answer,
            is_educational=response["is_educational"],
            sources=response.get("sources", []),
            original_language=request.language or "en"
        )
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Translation endpoint
@app.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    Translate text between languages using LibreTranslate
    """
    try:
        translated = await translation_service.translate(
            request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        return TranslateResponse(
            translated_text=translated,
            source_language=request.source_lang,
            target_language=request.target_lang
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get supported languages
@app.get("/languages")
async def get_languages():
    """Get list of supported languages"""
    return translation_service.get_supported_languages()

# Get subjects
@app.get("/subjects")
async def get_subjects():
    """Get list of available subjects"""
    return {
        "subjects": data_processor.get_subjects(),
        "total": len(data_processor.get_subjects())
    }

# Get topics for a subject
@app.get("/topics/{subject}")
async def get_topics(subject: str):
    """Get topics for a specific subject"""
    topics = data_processor.get_topics(subject=subject)
    return {
        "subject": subject,
        "topics": topics,
        "total": len(topics)
    }

# Generate quiz
@app.post("/quiz/generate", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """
    Generate a quiz with random questions
    """
    try:
        questions = data_processor.get_random_questions(
            n=request.num_questions,
            subject=request.subject,
            topic=request.topic
        )
        
        # Format questions for frontend
        formatted_questions = []
        for q in questions:
            formatted_questions.append({
                "id": q.get("id"),
                "question": q.get("question"),
                "options": q.get("options"),
                "correct_answer_index": q.get("correct_answer_index"),
                "explanation": q.get("explanation"),
                "subject": q.get("subject"),
                "topic": q.get("topic")
            })
        
        return QuizResponse(
            questions=formatted_questions,
            subject=request.subject
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PDFResponse(BaseModel):
    text: str
    filename: str

# PDF Upload Endpoint
@app.post("/pdf/upload", response_model=PDFResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and parse PDF file to extract text
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        content = await file.read()
        text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        
        return PDFResponse(text=text, filename=file.filename)
    except Exception as e:
        print(f"PDF processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

# Get dataset statistics
@app.get("/stats")
async def get_stats():
    """Get statistics about the dataset"""
    return data_processor.get_statistics()

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
