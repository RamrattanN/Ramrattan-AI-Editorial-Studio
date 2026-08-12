import { z } from "zod";

/**
 * Structured contract for the Editorial Direction task
 * (see the OpenAI Task Contract in the Web Walking Skeleton 01 work
 * order). Zero to two supporting lenses, matching the validated GPT
 * principle of one primary angle plus up to two supporting lenses.
 */
export const editorialDirectionSchema = z.object({
  source_understanding: z.string().min(1).max(2000),
  audience: z.string().min(1).max(300),
  objective: z.string().min(1).max(300),
  publication_language: z.string().min(1).max(60),
  primary_angle: z.string().min(1).max(500),
  supporting_lenses: z.array(z.string().min(1).max(500)).max(2),
  editorial_thesis: z.string().min(1).max(1000),
});

export type EditorialDirectionPayload = z.infer<typeof editorialDirectionSchema>;

export function parseEditorialDirection(
  raw: unknown,
):
  | { ok: true; data: EditorialDirectionPayload }
  | { ok: false; error: string } {
  const result = editorialDirectionSchema.safeParse(raw);
  if (!result.success) {
    return { ok: false, error: result.error.message };
  }
  return { ok: true, data: result.data };
}

/**
 * Structured contract for the Editorial Plan task (Web Walking Skeleton
 * 02, docs/product/version2/Web_Walking_Skeleton_02_Scope.md Section 4).
 * Fields mirror Web_Product_Foundation_v1.md Section 6's EditorialPlan
 * sketch.
 */
export const editorialPlanSchema = z.object({
  headline: z.string().min(1).max(300),
  hook: z.string().min(1).max(500),
  key_insights: z.array(z.string().min(1).max(500)).min(1).max(5),
  practical_takeaway: z.string().min(1).max(500),
  cta_direction: z.string().min(1).max(300),
});

export type EditorialPlanPayload = z.infer<typeof editorialPlanSchema>;

export function parseEditorialPlan(
  raw: unknown,
): { ok: true; data: EditorialPlanPayload } | { ok: false; error: string } {
  const result = editorialPlanSchema.safeParse(raw);
  if (!result.success) {
    return { ok: false, error: result.error.message };
  }
  return { ok: true, data: result.data };
}

/**
 * Structured contract for the Article Draft task (Web Walking Skeleton
 * 02, Section 5). Deliberately narrower than studio/article_engine's
 * ArticleDraft - hashtags, linkedin_description, and hero_visual_prompt
 * are out of scope for this slice (see the scope document Section 9).
 * No source_citation field: the model is given only the approved plan,
 * not the original source text, so a model-authored citation would be
 * unsound. The route handler builds the SourceAttribution deterministically
 * from the project's already-retrieved Source instead.
 */
export const articleDraftSchema = z.object({
  headline: z.string().min(1).max(300),
  hook: z.string().min(1).max(500),
  key_insights: z.array(z.string().min(1).max(500)).min(1).max(5),
  practical_takeaway: z.string().min(1).max(500),
  cta: z.string().min(1).max(300),
  article_markdown: z.string().min(1).max(20000),
});

export type ArticleDraftPayload = z.infer<typeof articleDraftSchema>;

export function parseArticleDraft(
  raw: unknown,
): { ok: true; data: ArticleDraftPayload } | { ok: false; error: string } {
  const result = articleDraftSchema.safeParse(raw);
  if (!result.success) {
    return { ok: false, error: result.error.message };
  }
  return { ok: true, data: result.data };
}
