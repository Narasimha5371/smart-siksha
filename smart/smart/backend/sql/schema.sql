-- Smart Shiksha unified relational schema (PostgreSQL)
-- Extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL CHECK (role IN ('student', 'teacher', 'admin')),
    grade_level INT,
    preferred_language TEXT DEFAULT 'en',
    password_hash TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Curriculum
CREATE TABLE IF NOT EXISTS curriculum (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject TEXT NOT NULL,
    chapter TEXT NOT NULL,
    topic TEXT NOT NULL,
    content_url TEXT NOT NULL,
    board_name TEXT DEFAULT 'NCERT',
    grade_level INT,
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Performance
CREATE TABLE IF NOT EXISTS performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quiz_id UUID NOT NULL,
    score NUMERIC(5,2) NOT NULL,
    time_taken_seconds INT,
    weakness_tags TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Chat History
CREATE TABLE IF NOT EXISTS chat_history (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_log JSONB NOT NULL,
    ai_feedback JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Learning Path
CREATE TABLE IF NOT EXISTS learning_path (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recommended_modules JSONB NOT NULL,
    rationale TEXT,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_curriculum_subject_topic ON curriculum(subject, topic);
CREATE INDEX IF NOT EXISTS idx_performance_user_created_at ON performance(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_learning_path_user_active ON learning_path(user_id, active);
