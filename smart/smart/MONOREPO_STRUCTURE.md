# Smart Shiksha Monorepo Blueprint

```text
smart-shiksha/
  apps/
    mobile/                 # Flutter app (Android/iOS)
    web/                    # Next.js app (student + teacher portal)
  backend/
    app/
      main.py               # FastAPI entrypoint
      services/
        rag_service.py      # Retrieval + tutoring orchestration
    train_ai.py             # Curriculum ingestion/chunking/embedding/upsert script
    sql/
      schema.sql            # PostgreSQL schema
    requirements.txt
  data/
    textbooks/              # NCERT/State Board source PDFs and text files
  infrastructure/
    docker-compose.yml      # postgres + vector db + backend + web
```

## Current repository mapping
- `mobile/` currently acts as `apps/mobile`
- `web/` currently acts as `apps/web`
- `backend/` already matches the backend service
