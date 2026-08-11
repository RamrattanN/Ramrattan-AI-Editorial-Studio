-- Adds the canonical "editorial_plan" project stage so Approve can advance
-- EditorialProject.stage per DEC-029, instead of only updating
-- editorial_directions.status. This stage was already named and referenced
-- (Web_Product_Foundation_v1.md Section 6's EditorialPlan entity; the
-- Approve UI copy "The next stage will be Editorial Plan") but was missing
-- from the stage CHECK constraint. Editorial Plan generation itself remains
-- out of scope for this walking skeleton.

ALTER TABLE editorial_projects
    DROP CONSTRAINT editorial_projects_stage_check;

ALTER TABLE editorial_projects
    ADD CONSTRAINT editorial_projects_stage_check
    CHECK (stage IN ('source_intake', 'editorial_direction', 'editorial_plan'));
