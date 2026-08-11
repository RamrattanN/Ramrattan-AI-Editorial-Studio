import OpenAI from "openai";

let client: OpenAI | undefined;

/**
 * Server-side-only OpenAI client. The API key is read from the process
 * environment and never sent to, or readable by, the browser - the
 * frontend package has no dependency on this module or on `openai`.
 */
export function getOpenAIClient(): OpenAI {
  if (!client) {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      throw new Error(
        "OPENAI_API_KEY is required but was not set. See web/.env.example.",
      );
    }
    client = new OpenAI({ apiKey });
  }
  return client;
}

/**
 * DEC-030 (product/validation/Product_Decisions.md): `gpt-5.6-terra` is the
 * approved Editorial Direction model, replacing `gpt-4o-mini`, following
 * DS-01's two-source controlled evaluation
 * (docs/product/version2/Editorial_Direction_Quality_Investigation.md).
 * `OPENAI_MODEL` remains available as an explicit override.
 */
export function getConfiguredModel(): string {
  return process.env.OPENAI_MODEL ?? "gpt-5.6-terra";
}
