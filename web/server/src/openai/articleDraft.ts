import type OpenAI from "openai";
import { getConfiguredModel, getOpenAIClient } from "./client.js";
import { type ArticleDraftPayload, parseArticleDraft } from "./schema.js";

const MAX_ATTEMPTS = 2; // one initial attempt + one bounded retry.

/**
 * Article Draft (Generation) instructions, following DEC-030's
 * instruction-quality bar. Grounded in the State Machine's Generation
 * behavioral spec: the complete article is produced once, from the
 * approved plan alone - not a second round of editorial judgment.
 * Deliberately narrower than the full Publication Package (see
 * docs/product/version2/Web_Walking_Skeleton_02_Scope.md Section 5/9):
 * no hashtags, no LinkedIn description, no Hero Visual prompt.
 */
const SYSTEM_PROMPT = `You are a skilled editor at Ramrattan AI Editorial Studio, writing the
complete first draft of a LinkedIn article from an already-approved
Editorial Plan. The plan is the sole input - do not introduce a new
angle, insight, or claim the plan did not already establish.

- Headline, Hook, Key Insights, Practical Takeaway, and Call to Action
  should carry the approved plan's content forward into finished,
  publication-ready language - not merely restate the plan verbatim.
- Article Markdown: the complete article body in Markdown, developing
  each Key Insight, opening with the Hook, and closing with the Practical
  Takeaway and Call to Action. Write for the plan's audience and
  objective as already established - do not invent a new audience.
- Respond with the requested JSON object only.`;

const JSON_SCHEMA = {
  name: "article_draft",
  strict: true,
  schema: {
    type: "object",
    additionalProperties: false,
    properties: {
      headline: { type: "string" },
      hook: { type: "string" },
      key_insights: {
        type: "array",
        items: { type: "string" },
        maxItems: 5,
      },
      practical_takeaway: { type: "string" },
      cta: { type: "string" },
      article_markdown: { type: "string" },
    },
    required: [
      "headline",
      "hook",
      "key_insights",
      "practical_takeaway",
      "cta",
      "article_markdown",
    ],
  },
} as const;

export interface EditorialPlanInput {
  headline: string;
  hook: string;
  keyInsights: string[];
  practicalTakeaway: string;
  ctaDirection: string;
}

export type ArticleDraftTaskResult =
  | { ok: true; data: ArticleDraftPayload }
  | { ok: false; error: string };

function logUsage(completion: OpenAI.Chat.Completions.ChatCompletion): void {
  console.info("[openai-usage]", {
    model: completion.model,
    requestId: completion.id,
    promptTokens: completion.usage?.prompt_tokens ?? null,
    completionTokens: completion.usage?.completion_tokens ?? null,
    totalTokens: completion.usage?.total_tokens ?? null,
    timestamp: new Date().toISOString(),
  });
}

function formatPlan(plan: EditorialPlanInput): string {
  return [
    `Headline: ${plan.headline}`,
    `Hook: ${plan.hook}`,
    `Key insights: ${plan.keyInsights.join("; ")}`,
    `Practical takeaway: ${plan.practicalTakeaway}`,
    `Call to action direction: ${plan.ctaDirection}`,
  ].join("\n");
}

async function requestOnce(
  client: OpenAI,
  model: string,
  plan: EditorialPlanInput,
): Promise<ArticleDraftTaskResult> {
  const completion = await client.chat.completions.create({
    model,
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      {
        role: "user",
        content: `Approved Editorial Plan:\n\n${formatPlan(plan)}`,
      },
    ],
    response_format: { type: "json_schema", json_schema: JSON_SCHEMA },
  });

  logUsage(completion);

  const raw = completion.choices[0]?.message?.content;
  if (!raw) {
    return { ok: false, error: "The model returned no content." };
  }

  let parsedJson: unknown;
  try {
    parsedJson = JSON.parse(raw);
  } catch {
    return { ok: false, error: "The model did not return valid JSON." };
  }

  const validated = parseArticleDraft(parsedJson);
  if (!validated.ok) {
    return { ok: false, error: `The model's output failed validation: ${validated.error}` };
  }

  return { ok: true, data: validated.data };
}

/**
 * Bounded editorial task: given an approved Editorial Plan, returns one
 * complete Article Draft. Generated exactly once, synchronously, on plan
 * approval. Never persists malformed output; a failure here is the
 * technical-failure Generation outcome (see the scope document Section
 * 5) - the risk-based block outcome is out of scope for this slice.
 */
export async function generateArticleDraft(
  plan: EditorialPlanInput,
): Promise<ArticleDraftTaskResult> {
  const client = getOpenAIClient();
  const model = getConfiguredModel();

  let lastError = "Unknown error.";
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    const result = await requestOnce(client, model, plan);
    if (result.ok) return result;
    lastError = result.error;
  }

  return { ok: false, error: lastError };
}
