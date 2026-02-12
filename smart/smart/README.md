# Smart Shiksha - Intelligent Tutoring System

Smart Shiksha is an AI-driven, Offline-First Intelligent Tutoring System (ITS) designed for students in rural areas with limited connectivity.

## Core Philosophy
- **Offline-First**: Functional without internet. Syncs when online.
- **Low-Resource**: Optimized for basic Android smartphones.
- **Vernacular**: Multilingual support for local languages.

## Tech Stack
- **Backend**: FastAPI (Python), PostgreSQL, SQLAlchemy.
- **Mobile**: Flutter (Dart), WatermelonDB/SQLite (Local DB).
- **AI**: OpenAI (Cloud) + TensorFlow Lite (Edge/Offline).

## Project Structure
- `backend/`: FastAPI application, API endpoints, and database models.
- `mobile/`: Flutter mobile application code.

## Getting Started

### Backend
1. Navigate to `backend/`
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `uvicorn app.main:app --reload`

### Mobile
1. Navigate to `mobile/`
2. Run `flutter pub get`
3. Run `flutter run`
