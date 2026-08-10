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

export function getConfiguredModel(): string {
  return process.env.OPENAI_MODEL ?? "gpt-4o-mini";
}
