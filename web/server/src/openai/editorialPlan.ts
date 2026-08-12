import type OpenAI from "openai";
import { getConfiguredModel, getOpenAIClient } from "./client.js";
import { type EditorialPlanPayload, parseEditorialPlan } from "./schema.js";

const MAX_ATTEMPTS = 2; // one initial attempt + one bounded retry.

/**
 * Editorial Plan instructions, following DEC-030's instruction-quality bar
 * (product/validation/Product_Decisions.md) - the same discipline applied
 * to the Editorial Direction task, per
 * docs/product/version2/Web_Walking_Skeleton_02_Scope.md Section 10.
 * Grounded in the State Machine's Editorial Plan behavioral spec
 * (docs/architecture/Version_1_1_State_Machine.md): the Author sees a
 * proposed Headline, Hook, Key Insights, Practical Takeaway, and Call to
 * Action before any article is written.
 */
const SYSTEM_PROMPT = `You are a skilled editor at Ramrattan AI Editorial Studio, proposing an
Editorial Plan for a LinkedIn article from an already-approved Editorial
Direction. Work concisely, accurately, and usefully - the plan is the
structure the Author commits to before a single word of the article is
written, so it must be specific enough to write from, not a restatement
of the direction.

- Headline: a specific, publication-ready headline that embodies the
  approved primary angle - not a generic label for the topic.
- Hook: the opening the article will actually use to earn the reader's
  attention, consistent with the approved audience and objective.
- Key Insights: one to five distinct, defensible points that develop the
  editorial thesis - each one must add something the others do not. Do
  not pad the list to reach five.
- Practical Takeaway: one concrete, actionable thing the audience can do
  or think differently as a result of reading.
- Call to Action Direction: what the article should invite the reader to
  do or consider next - a direction for the CTA, not necessarily its
  final wording.
- Ground every field in the supplied Editorial Direction - do not
  introduce claims, audience assumptions, or angles the direction did
  not already establish.
- Respond with the requested JSON object only.`;

const JSON_SCHEMA = {
  name: "editorial_plan",
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
      cta_direction: { type: "string" },
    },
    required: [
      "headline",
      "hook",
      "key_insights",
      "practical_takeaway",
      "cta_direction",
    ],
  },
} as const;

export interface EditorialDirectionInput {
  sourceUnderstanding: string;
  audience: string;
  objective: string;
  primaryAngle: string;
  supportingLenses: string[];
  editorialThesis: string;
}

export type EditorialPlanTaskResult =
  | { ok: true; data: EditorialPlanPayload }
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

function formatDirection(direction: EditorialDirectionInput): string {
  return [
    `Source understanding: ${direction.sourceUnderstanding}`,
    `Audience: ${direction.audience}`,
    `Objective: ${direction.objective}`,
    `Primary angle: ${direction.primaryAngle}`,
    direction.supportingLenses.length > 0
      ? `Supporting lenses: ${direction.supportingLenses.join("; ")}`
      : null,
    `Editorial thesis: ${direction.editorialThesis}`,
  ]
    .filter((line): line is string => line !== null)
    .join("\n");
}

async function requestOnce(
  client: OpenAI,
  model: string,
  direction: EditorialDirectionInput,
): Promise<EditorialPlanTaskResult> {
  const completion = await client.chat.completions.create({
    model,
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      {
        role: "user",
        content: `Approved Editorial Direction:\n\n${formatDirection(direction)}`,
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

  const validated = parseEditorialPlan(parsedJson);
  if (!validated.ok) {
    return { ok: false, error: `The model's output failed validation: ${validated.error}` };
  }

  return { ok: true, data: validated.data };
}

/**
 * Bounded editorial task: given an approved Editorial Direction, returns
 * one Editorial Plan proposal. Used both for the initial proposal (on
 * Direction approval) and for regeneration (on Request Revision) - both
 * are the same generation task against the same, unchanged Direction.
 * Never persists malformed output.
 */
export async function generateEditorialPlan(
  direction: EditorialDirectionInput,
): Promise<EditorialPlanTaskResult> {
  const client = getOpenAIClient();
  const model = getConfiguredModel();

  let lastError = "Unknown error.";
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    const result = await requestOnce(client, model, direction);
    if (result.ok) return result;
    lastError = result.error;
  }

  return { ok: false, error: lastError };
}
