-- Web Walking Skeleton 02 - Editorial Plan + Draft.
-- Adds the two entities scoped in
-- docs/product/version2/Web_Walking_Skeleton_02_Scope.md: EditorialPlan
-- (already sketched, not built, in Web_Product_Foundation_v1.md Section 6)
-- and Article (the Draft, deliberately narrower than the full
-- studio/article_engine.ArticleDraft it is modeled on - see the scope
-- document Section 5 for what is intentionally excluded). Additive only;
-- no existing table or column is changed beyond the stage CHECK
-- constraint, which gains one new value.

ALTER TABLE editorial_projects
    DROP CONSTRAINT editorial_projects_stage_check;

ALTER TABLE editorial_projects
    ADD CONSTRAINT editorial_projects_stage_check
    CHECK (stage IN ('source_intake', 'editorial_direction', 'editorial_plan', 'draft'));

-- EditorialPlan.status uses its own vocabulary, distinct from
-- editorial_directions.status, per the resolved Repository Author
-- decision recorded in Web_Walking_Skeleton_02_Scope.md Section 11:
-- revision_requested is a transient, self-clearing state (regeneration
-- returns it to proposed), never the terminal, stage-local meaning
-- editorial_directions' rejected carries.
CREATE TABLE IF NOT EXISTS editorial_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    editorial_project_id TEXT NOT NULL UNIQUE
        REFERENCES editorial_projects (id) ON DELETE CASCADE,
    headline TEXT NOT NULL,
    hook TEXT NOT NULL,
    key_insights JSONB NOT NULL DEFAULT '[]'::jsonb,
    practical_takeaway TEXT NOT NULL,
    cta_direction TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'proposed'
        CHECK (status IN ('proposed', 'approved', 'revision_requested')),
    decided_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Article (the Draft). One approved draft per project in this slice - no
-- Author editing surface exists yet (deferred, see the scope document
-- Section 9), so the row is written once, on successful Draft generation,
-- and not revised thereafter within this slice.
CREATE TABLE IF NOT EXISTS articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    editorial_project_id TEXT NOT NULL UNIQUE
        REFERENCES editorial_projects (id) ON DELETE CASCADE,
    headline TEXT NOT NULL,
    hook TEXT NOT NULL,
    key_insights JSONB NOT NULL DEFAULT '[]'::jsonb,
    practical_takeaway TEXT NOT NULL,
    cta TEXT NOT NULL,
    article_markdown TEXT NOT NULL,
    source_attributions JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
