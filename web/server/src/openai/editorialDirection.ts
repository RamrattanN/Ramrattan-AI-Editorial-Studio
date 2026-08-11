import type OpenAI from "openai";
import { getConfiguredModel, getOpenAIClient } from "./client.js";
import {
  type EditorialDirectionPayload,
  parseEditorialDirection,
} from "./schema.js";

const MAX_ATTEMPTS = 2; // one initial attempt + one bounded retry.

const SYSTEM_PROMPT = `You are an editorial assistant that reads source material and proposes
a single, consolidated Editorial Direction for a LinkedIn article. Follow
these rules:

- Infer audience, objective, and editorial angle from the source itself.
  Do not ask the Author a question - this task returns exactly one
  structured result.
- Recommend exactly one primary editorial angle. Include zero, one, or two
  supporting lenses only when they add genuinely distinct value - do not
  pad the list to reach two.
- Default publication_language to "US English" unless the source content
  strongly and unambiguously indicates a different intended publication
  language.
- source_understanding should be a concise, accurate summary of what the
  source actually says - never invent claims the source does not support.
- Respond with the requested JSON object only.`;

const JSON_SCHEMA = {
  name: "editorial_direction",
  strict: true,
  schema: {
    type: "object",
    additionalProperties: false,
    properties: {
      source_understanding: { type: "string" },
      audience: { type: "string" },
      objective: { type: "string" },
      publication_language: { type: "string" },
      primary_angle: { type: "string" },
      supporting_lenses: {
        type: "array",
        items: { type: "string" },
        maxItems: 2,
      },
      editorial_thesis: { type: "string" },
    },
    required: [
      "source_understanding",
      "audience",
      "objective",
      "publication_language",
      "primary_angle",
      "supporting_lenses",
      "editorial_thesis",
    ],
  },
} as const;

export type EditorialDirectionTaskResult =
  | { ok: true; data: EditorialDirectionPayload }
  | { ok: false; error: string };

/**
 * Development cost observability: logs non-secret usage metadata for every
 * completed request (regardless of downstream validation outcome), so
 * cost-per-Editorial-Project can eventually be measured. Never logs the
 * prompt or source text.
 */
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

async function requestOnce(
  client: OpenAI,
  model: string,
  sourceUrl: string,
  sourceText: string,
): Promise<EditorialDirectionTaskResult> {
  const completion = await client.chat.completions.create({
    model,
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      {
        role: "user",
        content: `Source URL: ${sourceUrl}\n\nSource content:\n${sourceText}`,
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

  const validated = parseEditorialDirection(parsedJson);
  if (!validated.ok) {
    return { ok: false, error: `The model's output failed validation: ${validated.error}` };
  }

  return { ok: true, data: validated.data };
}

/**
 * Bounded editorial task: given retrieved source text and its URL, returns
 * one consolidated, schema-validated Editorial Direction. Never persists
 * malformed output - retries once on an invalid response, then returns a
 * clear application error.
 */
export async function generateEditorialDirection(
  sourceUrl: string,
  sourceText: string,
): Promise<EditorialDirectionTaskResult> {
  const client = getOpenAIClient();
  const model = getConfiguredModel();

  let lastError = "Unknown error.";
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    const result = await requestOnce(client, model, sourceUrl, sourceText);
    if (result.ok) return result;
    lastError = result.error;
  }

  return { ok: false, error: lastError };
}
