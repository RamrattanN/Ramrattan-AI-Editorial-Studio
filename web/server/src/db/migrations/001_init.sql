-- Web Walking Skeleton 01 - initial schema.
-- Entities per docs/product/version2/Web_Product_Foundation_v1.md Section 6.
-- Intentionally minimal: Article, HeroVisual, Publication, and
-- ReaderEngagement are deferred and are not modeled here. This schema does
-- not block their later addition (see the foundation document).

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS authors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Magic-link login tokens. Only a hash of the token is stored; the raw
-- token exists only in the emailed/logged link and in the callback URL.
CREATE TABLE IF NOT EXISTS login_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_login_tokens_email ON login_tokens (email);

-- Editorial Project. The id follows the REP-[A-F0-9]{8} shape already
-- established by studio/portable_editorial_project.py so the web product
-- and the Portable Editorial Project format share one identity scheme.
CREATE TABLE IF NOT EXISTS editorial_projects (
    id TEXT PRIMARY KEY,
    author_id UUID NOT NULL REFERENCES authors (id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    stage TEXT NOT NULL DEFAULT 'source_intake'
        CHECK (stage IN ('source_intake', 'editorial_direction')),
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_editorial_projects_author
    ON editorial_projects (author_id);

CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    editorial_project_id TEXT NOT NULL
        REFERENCES editorial_projects (id) ON DELETE CASCADE,
    kind TEXT NOT NULL DEFAULT 'url' CHECK (kind IN ('url')),
    raw_reference TEXT NOT NULL,
    retrieved_summary TEXT,
    retrieval_status TEXT NOT NULL DEFAULT 'pending'
        CHECK (retrieval_status IN ('pending', 'succeeded', 'failed')),
    retrieval_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sources_project ON sources (editorial_project_id);

CREATE TABLE IF NOT EXISTS editorial_directions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    editorial_project_id TEXT NOT NULL UNIQUE
        REFERENCES editorial_projects (id) ON DELETE CASCADE,
    source_understanding TEXT NOT NULL,
    audience TEXT NOT NULL,
    objective TEXT NOT NULL,
    publication_language TEXT NOT NULL,
    primary_angle TEXT NOT NULL,
    supporting_lenses JSONB NOT NULL DEFAULT '[]'::jsonb,
    editorial_thesis TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'proposed'
        CHECK (status IN ('proposed', 'approved', 'rejected')),
    reject_feedback TEXT,
    decided_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- connect-pg-simple manages its own "session" table, created on first use
-- when createTableIfMissing is enabled (see src/auth/session.ts).
