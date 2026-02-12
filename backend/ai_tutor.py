from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from config import settings
from data_processor import data_processor
import re
from groq import Groq
import ollama

class AITutor:
    """
    AI Tutor with RAG (Retrieval Augmented Generation) and education-only guardrails
    """
    
    def __init__(self):
        # Initialize embedding model
        print(f"Loading embedding model: {settings.LOCAL_MODEL_NAME}")
        self.embedding_model = SentenceTransformer(settings.LOCAL_MODEL_NAME)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR
        )
        
        # Initialize Groq client
        self.groq_client = None
        if settings.GROQ_API_KEY and not settings.USE_OLLAMA:
            try:
                self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
                print(f"Groq client initialized with model: {settings.GROQ_MODEL}")
            except Exception as e:
                print(f"Groq initialization failed: {e}")
        
        if settings.USE_OLLAMA:
            print(f"Using Ollama with model: {settings.OLLAMA_MODEL}")
        
        self.collection = None
        self.is_initialized = False
    
    def initialize(self):
        """
        Initialize the AI tutor by loading data and creating embeddings
        """
        if self.is_initialized:
            return
        
        print("Initializing AI Tutor...")
        
        # Load JSONL data
        data = data_processor.load_data()
        if not data:
            print("Warning: No data loaded!")
            return
        
        # Get or create collection
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"description": "Education Q&A embeddings"}
            )
            print(f"Accessed collection with {self.collection.count()} items")
            
            # Always upsert data to ensure it matches JSONL file
            self._add_data_to_collection(data)
        except Exception as e:
            print(f"Error initializing collection: {e}")
        
        self.is_initialized = True
        print("AI Tutor initialized successfully!")
    
    def _add_data_to_collection(self, data: List[Dict[str, Any]]):
        """
        Add data to ChromaDB collection with embeddings
        """
        print(f"Adding {len(data)} items to collection...")
        
        batch_size = 100
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            
            documents = []
            metadatas = []
            ids = []
            
            for j, entry in enumerate(batch):
                # Format entry for embedding
                doc_text = data_processor.format_qa_for_embedding(entry)
                documents.append(doc_text)
                
                # Store metadata
                metadatas.append({
                    "source": entry.get("source", ""),
                    "subject": entry.get("subject", ""),
                    "topic": entry.get("topic", ""),
                    "question": entry.get("question", ""),
                    "explanation": entry.get("explanation", "")[:500],  # Limit size
                    "correct_answer": data_processor.get_correct_answer(entry)
                })
                
                ids.append(entry.get("id", f"qa_{i + j}"))
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(documents).tolist()
            
            # Add to collection
            # Add to collection (using upsert to handle updates/duplicates)
            self.collection.upsert(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            if (i + batch_size) % 1000 == 0:
                print(f"Processed {i + batch_size}/{len(data)} items...")
        
        print(f"Added {len(data)} items to collection!")
    
    def is_educational_query(self, query: str) -> bool:
        """
        Check if query is education-related using keyword matching
        """
        query_lower = query.lower()
        
        # Check for educational keywords
        education_keywords = settings.EDUCATION_KEYWORDS
        if any(keyword in query_lower for keyword in education_keywords):
            return True
        
        # Check for question patterns
        question_patterns = [
            r'\bwhat\b', r'\bhow\b', r'\bwhy\b', r'\bwhen\b', r'\bwhere\b',
            r'\bexplain\b', r'\bdescribe\b', r'\bdefine\b', r'\bsolve\b'
        ]
        if any(re.search(pattern, query_lower) for pattern in question_patterns):
            # Likely educational if it's a question
            return True
        
        # Check against restricted topics
        restricted_keywords = [
            'movie', 'film', 'celebrity', 'actor', 'actress',
            'sports', 'football', 'cricket', 'match', 'game',
            'politics', 'election', 'party', 'minister',
            'relationship', 'dating', 'love'
        ]
        if any(keyword in query_lower for keyword in restricted_keywords):
            return False
        
        # Default to True for ambiguous cases
        return True
    
    def get_rejection_response(self) -> str:
        """
        Return a friendly rejection message for non-educational queries
        """
        return """I'm your study buddy! 🎓 Let's focus on learning.

I can help you with:
📚 **Science**: Physics, Chemistry, Biology, Medicine
🔢 **Mathematics**: Algebra, Calculus, Geometry, Statistics
💻 **Computer Science**: Programming, Algorithms, Web Development
🌍 **Social Studies**: History, Geography, Economics
📝 **Languages**: English, Hindi, Grammar, Literature

What subject would you like to learn about today?"""
    
    async def search_similar(
        self,
        query: str,
        n_results: int = 3,
        subject_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar questions using vector similarity
        """
        if not self.is_initialized:
            self.initialize()
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Build where clause for filtering
        where = {}
        if subject_filter:
            where["subject"] = subject_filter
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where if where else None
        )
        
        # Format results
        formatted_results = []
        if results and results.get('metadatas'):
            for i, metadata in enumerate(results['metadatas'][0]):
                formatted_results.append({
                    "question": metadata.get("question", ""),
                    "explanation": metadata.get("explanation", ""),
                    "subject": metadata.get("subject", ""),
                    "topic": metadata.get("topic", ""),
                    "correct_answer": metadata.get("correct_answer", ""),
                    "distance": results['distances'][0][i] if results.get('distances') else 0
                })
        
        return formatted_results
    
    async def generate_response(
        self,
        query: str,
        language: str = "en",
        subject_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate response to user query with education guardrails
        
        Args:
            query: User's question
            language: Target language code
            subject_filter: Optional subject to filter results
        
        Returns:
            Response dict with answer, sources, and metadata
        """
        # Check if query is educational
        if not self.is_educational_query(query):
            return {
                "answer": self.get_rejection_response(),
                "is_educational": False,
                "sources": []
            }
        
        # Search for similar content to build context
        similar_items = await self.search_similar(query, n_results=5, subject_filter=subject_filter)
        
        # Build context from retrieved items
        context_parts = []
        if similar_items:
            for i, item in enumerate(similar_items[:3], 1):
                context_parts.append(f"""
Context {i}:
Subject: {item['subject']}
Topic: {item['topic']}
Question: {item['question']}
Answer: {item['correct_answer']}
Explanation: {item['explanation']}
""")
        
        context = "\n".join(context_parts) if context_parts else "No specific context available from the database."
        
        # Use Ollama or Groq to generate intelligent response
        try:
            # Build the prompt
            system_prompt = """You are an expert AI tutor for Smart Shiksha, a personalized education platform. Your role is to:

1. Provide clear, accurate, and educational answers
2. Use the provided context from the knowledge base when relevant
3. Explain concepts in a student-friendly way
4. Focus on education topics: Science, Math, Computer Science, History, Languages, etc.
5. Format responses with proper structure using markdown when helpful
6. Be encouraging and supportive

If the context is relevant, use it to inform your answer. If not directly applicable, use your knowledge to provide an educational response."""

            user_prompt = f"""Context from knowledge base:
{context}

Student's question: {query}

Please provide a comprehensive, educational answer to the student's question. Use the context if it's relevant, but feel free to provide a complete answer using your knowledge."""

            answer = ""
            
            if settings.USE_OLLAMA:
                print(f"DEBUG: Calling Ollama with model {settings.OLLAMA_MODEL}")
                response = ollama.chat(model=settings.OLLAMA_MODEL, messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ])
                answer = response['message']['content']
                print("DEBUG: Received response from Ollama")
                
            elif self.groq_client:
                print("DEBUG: Sending request to Groq...")
                completion = self.groq_client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=0.9
                )
                answer = completion.choices[0].message.content
                print("DEBUG: Received response from Groq")
            
            if answer:
                return {
                    "answer": answer,
                    "is_educational": True,
                    "sources": similar_items[:3] if similar_items else [],
                    "subject": similar_items[0]['subject'] if similar_items else "General",
                    "topic": similar_items[0]['topic'] if similar_items else "General Knowledge"
                }

        except Exception as e:
            print(f"ERROR: AI Generation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            pass
        
        # Fallback if AI generation failed (or client not initialized) AND no similar items found
        if not similar_items:
            print("DEBUG: No similar items found and AI failed/missing. Returning fallback.")
            return {
                "answer": "I couldn't generate a response at the moment. Please ensure Ollama is running or try asking a different question.",
                "is_educational": True,
                "sources": []
            }
        
        # Build response from top result as fallback
        top_result = similar_items[0]
        
        answer = f"""**Subject**: {top_result['subject']}
**Topic**: {top_result['topic']}

**Question**: {top_result['question']}

**Answer**: {top_result['correct_answer']}

**Explanation**: {top_result['explanation']}"""
        
        return {
            "answer": answer,
            "is_educational": True,
            "sources": similar_items[:3],
            "subject": top_result['subject'],
            "topic": top_result['topic']
        }

# Global AI tutor instance
ai_tutor = AITutor()
