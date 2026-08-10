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
