# Multilingual & Vernacular Language Support

## Supported Languages

### Primary Languages

- **English** (en) - Default
- **Hindi** (hi) - हिंदी
- **Tamil** (ta) - தமிழ்
- **Telugu** (te) - తెలుగు
- **Bengali** (bn) - বাংলা
- **Marathi** (mr) - मराठी
- **Gujarati** (gu) - ગુજરાતી
- **Kannada** (kn) - ಕನ್ನಡ
- **Malayalam** (ml) - മലയാളം
- **Punjabi** (pa) - ਪੰਜਾਬੀ

## Translation Implementation

### Free Translation Options

#### Option 1: Google Translate API (Free Tier)

- ✅ Free up to 500,000 characters/month
- ✅ High quality translations
- ✅ Supports all Indian languages
- ✅ REST API integration

#### Option 2: LibreTranslate (Open Source)

- ✅ 100% free and open source
- ✅ Self-hosted or cloud
- ✅ No API limits
- ⚠️ Quality slightly lower than Google

#### Option 3: Azure Translator (Free Tier)

- ✅ 2M characters/month free
- ✅ Excellent quality
- ✅ Good for Indic languages

**Recommended**: Start with Google Translate API free tier, switch to LibreTranslate if limits exceeded.

## Language Features

### 1. UI Translation

All interface elements translated:

- Navigation menus
- Buttons and labels
- Form fields
- Error messages
- Notifications

### 2. Content Translation

- Lesson text
- Quiz questions and options
- Explanations
- Chat responses

### 3. Language Selection

- Dropdown in header
- Persisted in user profile
- Auto-detect browser language
- Remember last selection

## Technical Implementation

### Frontend (i18next)

```javascript
// Language configuration
const resources = {
  en: {
    translation: {
      welcome: "Welcome to Smart Shiksha",
      lessons: "Lessons",
      quizzes: "Quizzes",
      progress: "Progress",
    },
  },
  hi: {
    translation: {
      welcome: "स्मार्ट शिक्षा में आपका स्वागत है",
      lessons: "पाठ",
      quizzes: "प्रश्नोत्तरी",
      progress: "प्रगति",
    },
  },
  // ... other languages
};

// Initialize i18next
i18next.init({
  lng: "en",
  resources: resources,
});

// Use in HTML
<h1 data-i18n="welcome"></h1>;
```

### Backend Translation API

```python
# POST /api/translate
{
  "text": "What is the function of the heart?",
  "from": "en",
  "to": "hi"
}

# Response
{
  "translated_text": "हृदय का कार्य क्या है?",
  "source_language": "en",
  "target_language": "hi"
}
```

### Real-time Chat Translation

```
User types in Hindi → Backend translates to English → AI processes →
AI responds in English → Backend translates to Hindi → User sees Hindi response
```

## AI Agent Educational Scope (All Subjects)

### Allowed Topics

- **STEM**: Math, Physics, Chemistry, Biology
- **Medical**: Anatomy, Medicine, Surgery (from JSONL data)
- **Languages**: English, Hindi, Regional languages
- **Social Sciences**: History, Geography, Civics, Economics
- **Computer Science**: Programming, Web development, Data structures
- **Commerce**: Accounting, Business studies
- **Arts**: Literature, Music theory, Art history

### Restricted Topics

- ❌ Entertainment (movies, TV shows, celebrities)
- ❌ Sports scores and news
- ❌ Politics and current affairs
- ❌ Personal advice (relationships, career)
- ❌ Religion and philosophy
- ❌ Games and gaming

### Guardrail Prompts

```
You are an educational AI tutor covering ALL academic subjects including:
- Science (Physics, Chemistry, Biology, Math)
- Medical sciences (Anatomy, Medicine, Surgery, etc.)
- Languages and Literature
- Social Sciences (History, Geography, Economics)
- Computer Science and Technology
- Commerce and Business

You help students learn, understand concepts, solve problems, and prepare for exams.

If asked about non-educational topics, respond with:
"I'm here to help with your studies! Let's focus on education.
What subject would you like to learn about? I can help with Science, Math,
Languages, Social Studies, Computer Science, and more!"
```

## Database Schema Updates

### User Profile

```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  preferredLanguage: String, // "en", "hi", "ta", etc.
  languageHistory: [String], // Track language switches
  // ... other fields
}
```

### Content Cache

```javascript
{
  _id: ObjectId,
  originalText: String,
  originalLanguage: String,
  translations: {
    "hi": String,
    "ta": String,
    "te": String,
    // ... other languages
  },
  createdAt: Date
}
```

## Performance Optimization

1. **Cache Translations**: Store frequently translated phrases
2. **Batch Requests**: Translate multiple strings in one API call
3. **Lazy Loading**: Translate only visible content
4. **Client-side Storage**: Store UI translations locally
5. **CDN**: Serve language files from CDN

## Cost Estimation

### Google Translate API Free Tier

- 500,000 characters/month free
- Average lesson: ~2,000 characters
- **250 lesson translations/month free**
- Beyond that: $20/1M characters

### Optimization Strategy

- Cache common translations
- Pre-translate popular lessons
- Use free tier for UI, cache content translations
- **Expected monthly cost: $0** (within free tier)

## Implementation Priority

1. ✅ Setup i18next for frontend UI translation
2. ✅ Add language dropdown to header
3. ✅ Integrate Google Translate API for content
4. ✅ Update AI agent to handle multilingual queries
5. ✅ Add translation caching
6. ✅ Test with Hindi, Tamil, Telugu
