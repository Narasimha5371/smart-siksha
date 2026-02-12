# Smart Shiksha Web (Next.js)

## Run
1. `cd web`
2. `npm install`
3. `npm run dev`

## Routes
- `/` landing
- `/student` student portal (chat + textbook split view)
- `/teacher` teacher dashboard (curriculum upload + stats)

## Required env
Create `web/.env.local`:

```env
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

Backend must be running with endpoints from `backend/app/main.py`.
