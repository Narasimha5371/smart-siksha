# AI Agent Educational Focus (All Subjects)

## Education-Only AI Agent

### System Prompt

```
You are an educational AI tutor helping students learn ALL academic subjects including:

**STEM**: Mathematics, Physics, Chemistry, Biology
**Medical**: Anatomy, Medicine, Surgery, Pharmacology, Pathology, Microbiology, etc.
**Languages**: English, Hindi, Regional languages, Grammar, Literature
**Social Sciences**: History, Geography, Civics, Economics, Political Science
**Computer Science**: Programming, Algorithms, Web development, Databases
**Commerce**: Accounting, Business Studies, Economics
**Arts & Humanities**: Literature, Music theory, Art history

Your goal is to help students understand concepts, solve problems, and prepare for exams.

If a user asks about non-educational topics (entertainment, sports, politics, celebrities),
politely redirect: "I'm your study buddy! Let's focus on learning. What subject can I help
you with? I cover Science, Math, Languages, Social Studies, Computer Science, and more!"
```

### Intent Classification

1. **Pre-processing Filter**: Check if query contains educational keywords
2. **Embedding Similarity**: Compare query embedding to education corpus (threshold: 0.6)
3. **LLM Classification**: If unclear, use small model to classify (educational vs non-educational)
4. **Rejection Responses**: Maintain list of friendly redirects

### Allowed Topics (Comprehensive Education)

**STEM Subjects**:

- Mathematics (Algebra, Calculus, Geometry, Statistics)
- Physics (Mechanics, Electromagnetism, Thermodynamics, Optics)
- Chemistry (Organic, Inorganic, Physical Chemistry)
- Biology (Botany, Zoology, Ecology, Genetics)

**Medical Sciences** (from JSONL data):

- Anatomy, Biochemistry, Physiology, Pathology
- Pharmacology, Microbiology, Medicine, Surgery
- Pediatrics, Gynecology & Obstetrics, ENT, Ophthalmology
- Orthopedics, Radiology, Forensic Medicine, Anesthesia

**Languages & Literature**:

- English Grammar, Composition, Literature
- Hindi, Tamil, Telugu and other regional languages
- Sanskrit, Foreign languages

**Social Sciences**:

- History (Ancient, Medieval, Modern, World)
- Geography (Physical, Human, Economic)
- Civics & Political Science
- Economics & Commerce

**Computer Science**:

- Programming (Python, Java, C++, JavaScript)
- Data Structures & Algorithms
- Web Development, Databases
- Computer Networks, Operating Systems

**Restricted Topics**:

- ❌ Entertainment (movies, celebrities, TV shows)
- ❌ Sports news and scores
- ❌ Current political affairs
- ❌ Personal advice (relationships, career counseling)
- ❌ Gaming and non-educational content

---

---

## Note on Video Generation

All major AI video generation services (D-ID, Heygen, Synthesia) are **paid services** with no truly free tier for production use. Therefore, **video generation is NOT implemented** in this version.

**Alternative Approach**: Focus on high-quality text-based lessons with:

- ✅ Rich formatting (markdown)
- ✅ Diagrams and illustrations
- ✅ Interactive elements
- ✅ Step-by-step explanations
- ✅ Code syntax highlighting (for programming)
- ✅ Mathematical equations (LaTeX)

If free video generation becomes available in the future, it can be easily integrated.

### Recommended Service: **D-ID**

- ✅ Realistic AI avatars
- ✅ 20-minute free trial
- ✅ Pay-as-you-go pricing ($0.12/sec)
- ✅ REST API integration
- ✅ Multiple languages

### Alternative: **Heygen**

- High-quality videos
- Multiple avatar options
- Slightly higher cost

### Video Generation Flow

```
1. User selects topic (e.g., "Aortic Stenosis")
2. Backend retrieves relevant content from JSONL
3. Generate lesson script with key points
4. Call D-ID API to create avatar video
5. Cache video in cloud storage (S3/R2)
6. Return video URL to frontend
```

### API Implementation

```python
# POST /api/video/generate
{
  "topic": "Aortic Stenosis",
  "subject": "Medicine",
  "language": "en"
}

# Response
{
  "video_id": "abc123",
  "video_url": "https://cdn.../video.mp4",
  "duration": 180,
  "transcript": "...",
  "created_at": "2026-02-11T19:30:00Z"
}
```

### Video Features

- **Avatar Selection**: Professional medical instructor avatar
- **Background**: Clean classroom/medical setting
- **Synchronized Transcript**: Display text alongside video
- **Bookmarks**: Click timestamps to jump to sections
- **Download**: Allow offline viewing (optional)

### Cost Optimization

1. **Cache videos**: Store generated videos for 30 days
2. **Batch generation**: Pre-generate popular topics
3. **Compression**: Use H.264 compression
4. **CDN**: Use cloud CDN for fast delivery

---

## Technical Specifications

### Backend Changes

- Add `video_generator.py` module
- Store video metadata in MongoDB
- Implement caching layer (Redis optional)
- Add video generation queue (for async processing)

### Frontend Changes

- Video player component with controls
- Lesson page with embedded videos
- Loading state during generation
- Fallback to text if video unavailable
