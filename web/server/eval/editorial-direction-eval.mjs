#!/usr/bin/env node
/**
 * DS-01 Editorial Direction quality-investigation harness (BL-001 / BL-002).
 *
 * Standalone, dependency-free (Node's built-in `fetch` only - no `npm
 * install` required) so it can run in any environment with an
 * `OPENAI_API_KEY` already set, independent of whether `web/server`'s own
 * npm dependencies are installed.  It calls the OpenAI Chat Completions API
 * directly, replicating the exact request shape used by production
 * (`web/server/src/openai/editorialDirection.ts`), so a comparison is
 * apples-to-apples with what the application actually sends.
 *
 * This script is investigation tooling, not production code.  It is not
 * imported by `src/`, not covered by `npm run lint`/`typecheck` (both
 * scoped to `src`/`tests`), and must never be wired into the application.
 *
 * Usage:
 *   OPENAI_API_KEY=sk-... node web/server/eval/editorial-direction-eval.mjs \
 *     --model gpt-4o-mini \
 *     --prompt current \
 *     --source /path/to/extracted-source-text.txt \
 *     --source-url "https://example.com/original-article" \
 *     [--out /path/outside/the/repo]
 *
 * --model   Any current Chat Completions model name (see MODEL_PRICING
 *           below for the reference set this investigation considered).
 * --prompt  "current" (verbatim production SYSTEM_PROMPT) or "improved"
 *           (DS-01's candidate baseline-aligned instructions - see
 *           IMPROVED_SYSTEM_PROMPT below).
 * --source  Path to a local text file containing already-extracted source
 *           text (the same shape `retrieveSource()` produces - plain text,
 *           boilerplate stripped).  This script does not fetch or parse
 *           HTML itself, to stay dependency-free; extract the source text
 *           the same way production does, or reuse a fixture already
 *           captured that way.
 * --source-url  Recorded in the result file for provenance only.
 * --out     Output directory for the JSON result file.  Defaults to the
 *           system temp directory, deliberately outside the repository -
 *           see the note on copyrighted source text below.
 *
 * Do NOT commit result files to the repository: they can contain the
 * model's echo of copyrighted source text via `source_understanding`.
 * Keep results local; report only rubric scores, token usage, and
 * estimated cost in the durable evidence artifact
 * (docs/product/version2/Editorial_Direction_Quality_Investigation.md).
 */

import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

// Verbatim copy of web/server/src/openai/editorialDirection.ts's SYSTEM_PROMPT
// (2026-08-11).  Keep these two in sync manually; this file intentionally
// does not import from src/ so it stays dependency-free and can run without
// `npm install`.
const CURRENT_SYSTEM_PROMPT = `You are an editorial assistant that reads source material and proposes
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

// DS-01 candidate baseline-aligned instructions: adds the locked GPT's
// missing quality framing (editor persona, verification, distinctiveness)
// without requiring a browsing tool the web app does not have.  See
// docs/product/version2/Editorial_Direction_Quality_Investigation.md,
// "Phase 2 - Difference Analysis" for the evidence behind each addition.
const IMPROVED_SYSTEM_PROMPT = `You are a skilled editor at Ramrattan AI Editorial Studio, reading source
material to propose a single, consolidated Editorial Direction for a
LinkedIn article. Work concisely, accurately, and usefully - the way an
experienced editor would brief a writer before drafting begins.

- Infer audience, objective, and editorial angle from the source itself.
  Do not ask the Author a question - this task returns exactly one
  structured result.
- Read critically, not just descriptively. Identify the source's strongest,
  most defensible claims and its central tension or non-obvious
  implication - the thing a generic summary would miss. A flat restatement
  of the source is not an editorial direction.
- Recommend exactly one primary editorial angle. Include zero, one, or two
  supporting lenses only when they add genuinely distinct value - do not
  pad the list to reach two. A strong single angle beats three shallow ones.
- Treat claims you cannot verify from the supplied source text as
  unverified: note the uncertainty in source_understanding rather than
  stating them as settled fact. You have no browsing access - work only
  from the supplied text, and say plainly when the source itself is thin
  on evidence for a claim.
- Default publication_language to "US English" unless the source content
  strongly and unambiguously indicates a different intended publication
  language.
- source_understanding should be a concise, accurate summary of what the
  source actually says, including any material uncertainty - never invent
  claims the source does not support.
- editorial_thesis should state a specific, defensible argument a
  manager or practitioner audience would find useful - not a generic
  observation restating the source's topic.
- Respond with the requested JSON object only.`;

// Verbatim copy of web/server/src/openai/editorialDirection.ts's JSON_SCHEMA.
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
      supporting_lenses: { type: "array", items: { type: "string" }, maxItems: 2 },
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
};

// Reference pricing captured 2026-08-11 from developers.openai.com/api/docs/pricing
// (USD per 1M tokens).  Verify against that page before relying on this for
// a production decision - pricing changes independently of this file.
const MODEL_PRICING = {
  "gpt-4o-mini": { input: 0.15, output: 0.6 },
  "gpt-4o": { input: 2.5, output: 10.0 },
  "gpt-5.6-luna": { input: 0.2, output: 1.2 },
  "gpt-5.6-terra": { input: 2.0, output: 12.0 },
  "gpt-5.6-sol": { input: 5.0, output: 30.0 },
};

function parseArgs(argv) {
  const args = { out: tmpdir() };
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    if (flag === "--model") args.model = argv[++i];
    else if (flag === "--prompt") args.prompt = argv[++i];
    else if (flag === "--source") args.source = argv[++i];
    else if (flag === "--source-url") args.sourceUrl = argv[++i];
    else if (flag === "--out") args.out = argv[++i];
  }
  return args;
}

function estimateCost(model, usage) {
  const pricing = MODEL_PRICING[model];
  if (!pricing || !usage) return null;
  const inputCost = (usage.prompt_tokens / 1_000_000) * pricing.input;
  const outputCost = (usage.completion_tokens / 1_000_000) * pricing.output;
  return Number((inputCost + outputCost).toFixed(6));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.model || !args.prompt || !args.source) {
    console.error(
      "Usage: node editorial-direction-eval.mjs --model <name> --prompt <current|improved> --source <path> [--source-url <url>] [--out <dir>]",
    );
    process.exitCode = 1;
    return;
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    // Mirrors web/server/src/openai/client.ts's guard: fail closed before
    // any network call, no key ever logged.
    console.error("OPENAI_API_KEY is required but was not set.");
    process.exitCode = 1;
    return;
  }

  const systemPrompt =
    args.prompt === "current"
      ? CURRENT_SYSTEM_PROMPT
      : args.prompt === "improved"
        ? IMPROVED_SYSTEM_PROMPT
        : null;
  if (!systemPrompt) {
    console.error('--prompt must be "current" or "improved".');
    process.exitCode = 1;
    return;
  }

  const sourceText = readFileSync(args.source, "utf-8");

  const requestBody = {
    model: args.model,
    messages: [
      { role: "system", content: systemPrompt },
      {
        role: "user",
        content: `Source URL: ${args.sourceUrl ?? "(not supplied)"}\n\nSource content:\n${sourceText}`,
      },
    ],
    response_format: { type: "json_schema", json_schema: JSON_SCHEMA },
  };

  const startedAt = Date.now();
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify(requestBody),
  });
  const latencyMs = Date.now() - startedAt;

  const completion = await response.json();

  if (!response.ok) {
    console.error(`OpenAI API error (${response.status}):`, completion.error?.message ?? completion);
    process.exitCode = 1;
    return;
  }

  const raw = completion.choices?.[0]?.message?.content;
  let parsed = null;
  let parseError = null;
  try {
    parsed = raw ? JSON.parse(raw) : null;
  } catch (error) {
    parseError = String(error);
  }

  const usage = completion.usage ?? null;
  const result = {
    variantMeta: {
      model: args.model,
      promptCondition: args.prompt,
      sourceUrl: args.sourceUrl ?? null,
      sourcePath: args.source,
      timestamp: new Date().toISOString(),
      latencyMs,
    },
    usage: usage
      ? {
          promptTokens: usage.prompt_tokens,
          completionTokens: usage.completion_tokens,
          totalTokens: usage.total_tokens,
        }
      : null,
    estimatedCostUsd: estimateCost(args.model, usage),
    parseError,
    editorialDirection: parsed,
  };

  mkdirSync(args.out, { recursive: true });
  const outPath = join(
    args.out,
    `ds01-${args.model}-${args.prompt}-${Date.now()}.json`,
  );
  writeFileSync(outPath, JSON.stringify(result, null, 2), "utf-8");

  console.log(`Model: ${args.model} | Prompt: ${args.prompt} | Latency: ${latencyMs}ms`);
  console.log(
    `Tokens - prompt: ${usage?.prompt_tokens ?? "?"}, completion: ${usage?.completion_tokens ?? "?"}, total: ${usage?.total_tokens ?? "?"}`,
  );
  console.log(`Estimated cost: $${result.estimatedCostUsd ?? "unknown (model not in MODEL_PRICING)"}`);
  console.log(`Result written to: ${outPath}`);
  if (parseError) console.error(`Schema/JSON parse error: ${parseError}`);
}

main().catch((error) => {
  console.error("Evaluation harness failed:", error);
  process.exitCode = 1;
});
