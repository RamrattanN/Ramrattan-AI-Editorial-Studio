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
 * Fidelity notes (see docs/product/version2/Editorial_Direction_Quality_Investigation.md
 * Section 5 for the full fidelity proof):
 * - SYSTEM_PROMPT and JSON_SCHEMA below are verified byte-for-byte/deep-equal
 *   identical to web/server/src/openai/editorialDirection.ts.
 * - The request body (model, messages, response_format) and endpoint
 *   (POST https://api.openai.com/v1/chat/completions) match exactly what
 *   the `openai` SDK's `chat.completions.create` sends over the wire.
 * - Neither production nor this harness sets temperature/top_p/max_tokens,
 *   so both rely on identical API defaults.
 * - Source extraction (fetchAndExtractSource below) is a dependency-free,
 *   good-faith reproduction of web/server/src/source/retrieve.ts's rules
 *   (same selectors stripped, same 12,000-char cap) using regex-based tag
 *   stripping instead of the `html-to-text` package (unavailable - no
 *   `npm install` was authorized).  It is NOT byte-identical to
 *   `html-to-text`'s output.  This is disclosed, and does not bias the
 *   prompt-effect/model-effect comparison because the SAME extracted text
 *   is reused across all four matrix variants.
 *
 * Usage - fetch and inspect a source before spending any OpenAI budget:
 *   node web/server/eval/editorial-direction-eval.mjs \
 *     --mode fetch-source \
 *     --source-url "https://example.com/article" \
 *     --out-file /path/outside/the/repo/source.txt
 *
 * Usage - run the approved 4-call matrix (A/B/C/D) in one bounded pass:
 *   OPENAI_API_KEY=sk-... node web/server/eval/editorial-direction-eval.mjs \
 *     --mode run-matrix \
 *     --source-url "https://example.com/article" \
 *     --stronger-model gpt-5.6-terra \
 *     [--out /path/outside/the/repo]
 *
 * Usage - a single ad hoc call (not part of the approved 4-call bound):
 *   OPENAI_API_KEY=sk-... node web/server/eval/editorial-direction-eval.mjs \
 *     --mode single --model gpt-4o-mini --prompt current \
 *     --source /path/to/extracted-source-text.txt \
 *     --source-url "https://example.com/article" [--out /path]
 *
 * --out / --out-file  Defaults to the system temp directory, deliberately
 *           outside the repository - see the note on copyrighted source
 *           text below.
 *
 * Do NOT commit result files to the repository: they can contain the
 * model's echo of copyrighted source text via `source_understanding`.
 * Keep results local; report only rubric scores, token usage, and
 * estimated cost in the durable evidence artifact
 * (docs/product/version2/Editorial_Direction_Quality_Investigation.md).
 */

import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

// Loads web/server/.env into this process's own environment using Node's
// built-in loader (no `dotenv` package needed, since it is not installed
// here) - the same file production's own `dotenv.config()` call would
// load. This never prints, logs, or returns the file's contents; it only
// makes OPENAI_API_KEY available to this process via `process.env`,
// exactly as the running application does. Silently does nothing if the
// file is absent (e.g. `OPENAI_API_KEY` was exported some other way).
function loadLocalEnvIfPresent() {
  const here = dirname(fileURLToPath(import.meta.url));
  const envPath = join(here, "..", ".env");
  try {
    process.loadEnvFile(envPath);
  } catch {
    // No .env file at that path - fall through and rely on whatever is
    // already in process.env, matching production's own behavior.
  }
}

// Mirrors web/server/src/source/retrieve.ts's bounds exactly.
const FETCH_TIMEOUT_MS = 10_000;
const MAX_BYTES = 2_000_000;
const MAX_SUMMARY_CHARS = 12_000;

/**
 * Dependency-free, good-faith reproduction of retrieveSource()'s
 * `html-to-text` conversion: strips script/style/nav/footer blocks
 * (including their content), strips img tags, drops all remaining tags
 * (so link text survives but hrefs do not - matching `ignoreHref`),
 * decodes common entities, and collapses blank-line runs the same way
 * (`\n{3,}` -> `\n\n`, then trim). Not byte-identical to `html-to-text`.
 */
function stripHtmlToText(html) {
  let text = html;
  text = text.replace(/<script[\s\S]*?<\/script>/gi, "");
  text = text.replace(/<style[\s\S]*?<\/style>/gi, "");
  text = text.replace(/<nav[\s\S]*?<\/nav>/gi, "");
  text = text.replace(/<footer[\s\S]*?<\/footer>/gi, "");
  text = text.replace(/<img\b[^>]*>/gi, "");
  // Insert newlines at common block boundaries so paragraph structure
  // survives tag stripping, approximating html-to-text's block handling.
  text = text.replace(/<\/(p|div|li|h[1-6]|tr|blockquote)>/gi, "\n");
  text = text.replace(/<br\s*\/?>/gi, "\n");
  text = text.replace(/<[^>]+>/g, "");
  text = text
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ");
  text = text.replace(/[ \t]{2,}/g, " ");
  text = text.replace(/\n{3,}/g, "\n\n").trim();
  return text;
}

/**
 * Fetch and extract, mirroring retrieveSource()'s network behavior
 * (timeout, headers, byte cap, content-type check, minimum-length guard,
 * MAX_SUMMARY_CHARS truncation) without the SSRF guard - not needed for
 * a deliberately chosen, known-public evaluation fixture, unlike
 * production's arbitrary Author-submitted URLs.
 */
async function fetchAndExtractSource(rawUrl) {
  const url = new URL(rawUrl);
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const response = await fetch(url, {
      signal: controller.signal,
      redirect: "follow",
      headers: {
        "User-Agent": "RamrattanEditorialStudio/0.1 (+walking-skeleton-01-eval)",
        Accept: "text/html,application/xhtml+xml",
      },
    });
    if (!response.ok) {
      throw new Error(`The source could not be retrieved (HTTP ${response.status}).`);
    }
    const contentType = response.headers.get("content-type") ?? "";
    if (!contentType.includes("html") && !contentType.includes("text")) {
      throw new Error("This source's content type is not supported.");
    }
    const reader = response.body?.getReader();
    if (!reader) throw new Error("The source returned no content.");
    let received = 0;
    const chunks = [];
    while (received < MAX_BYTES) {
      const { done, value } = await reader.read();
      if (done) break;
      if (value) {
        chunks.push(value);
        received += value.byteLength;
      }
    }
    await reader.cancel().catch(() => undefined);
    const html = Buffer.concat(chunks.map((c) => Buffer.from(c))).toString("utf-8");
    const text = stripHtmlToText(html);
    if (text.length < 200) {
      throw new Error(
        "Not enough readable content was found at this URL. It may require a browser, a login, or be paywalled.",
      );
    }
    return text.slice(0, MAX_SUMMARY_CHARS);
  } finally {
    clearTimeout(timeout);
  }
}

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
  const args = { out: tmpdir(), mode: "single" };
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    if (flag === "--mode") args.mode = argv[++i];
    else if (flag === "--model") args.model = argv[++i];
    else if (flag === "--prompt") args.prompt = argv[++i];
    else if (flag === "--source") args.source = argv[++i];
    else if (flag === "--source-url") args.sourceUrl = argv[++i];
    else if (flag === "--stronger-model") args.strongerModel = argv[++i];
    else if (flag === "--out") args.out = argv[++i];
    else if (flag === "--out-file") args.outFile = argv[++i];
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

function resolvePrompt(condition) {
  if (condition === "current") return CURRENT_SYSTEM_PROMPT;
  if (condition === "improved") return IMPROVED_SYSTEM_PROMPT;
  return null;
}

async function callOnce({ model, promptCondition, sourceUrl, sourceText, apiKey }) {
  const systemPrompt = resolvePrompt(promptCondition);
  const requestBody = {
    model,
    messages: [
      { role: "system", content: systemPrompt },
      {
        role: "user",
        content: `Source URL: ${sourceUrl ?? "(not supplied)"}\n\nSource content:\n${sourceText}`,
      },
    ],
    response_format: { type: "json_schema", json_schema: JSON_SCHEMA },
  };

  const startedAt = Date.now();
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
    body: JSON.stringify(requestBody),
  });
  const latencyMs = Date.now() - startedAt;
  const completion = await response.json();

  if (!response.ok) {
    return {
      variantMeta: { model, promptCondition, sourceUrl, timestamp: new Date().toISOString(), latencyMs },
      error: `OpenAI API error (${response.status}): ${completion.error?.message ?? JSON.stringify(completion)}`,
    };
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
  return {
    variantMeta: { model, promptCondition, sourceUrl, timestamp: new Date().toISOString(), latencyMs },
    usage: usage
      ? { promptTokens: usage.prompt_tokens, completionTokens: usage.completion_tokens, totalTokens: usage.total_tokens }
      : null,
    estimatedCostUsd: estimateCost(model, usage),
    parseError,
    editorialDirection: parsed,
  };
}

async function runFetchSource(args) {
  if (!args.sourceUrl) {
    console.error("Usage: --mode fetch-source --source-url <url> [--out-file <path>]");
    process.exitCode = 1;
    return;
  }
  const text = await fetchAndExtractSource(args.sourceUrl);
  console.log(`Extracted ${text.length} characters from ${args.sourceUrl}`);
  console.log("--- preview (first 500 chars) ---");
  console.log(text.slice(0, 500));
  console.log("--- end preview ---");
  if (args.outFile) {
    writeFileSync(args.outFile, text, "utf-8");
    console.log(`Full extracted text written to: ${args.outFile}`);
  } else {
    console.log("(pass --out-file <path> to save the full text for reuse)");
  }
}

async function runSingle(args, apiKey) {
  if (!args.model || !args.prompt || !args.source) {
    console.error(
      "Usage: --mode single --model <name> --prompt <current|improved> --source <path> [--source-url <url>] [--out <dir>]",
    );
    process.exitCode = 1;
    return;
  }
  if (!resolvePrompt(args.prompt)) {
    console.error('--prompt must be "current" or "improved".');
    process.exitCode = 1;
    return;
  }
  const sourceText = readFileSync(args.source, "utf-8");
  const result = await callOnce({
    model: args.model,
    promptCondition: args.prompt,
    sourceUrl: args.sourceUrl,
    sourceText,
    apiKey,
  });
  writeResult(args.out, `${args.model}-${args.prompt}`, result);
}

/**
 * The approved DS-01 bounded pass: exactly four calls (A/B/C/D), fetching
 * the source once and reusing it across all four, per the Repository
 * Author's approval of "one bounded evaluation pass of 4 OpenAI calls
 * total - variants A/B/C/D only." This function makes no more and no
 * fewer than four `callOnce` invocations.
 */
async function runMatrix(args, apiKey) {
  if (!args.sourceUrl) {
    console.error("Usage: --mode run-matrix --source-url <url> --stronger-model <name> [--out <dir>]");
    process.exitCode = 1;
    return;
  }
  if (!args.strongerModel) {
    console.error("--stronger-model is required, e.g. --stronger-model gpt-5.6-terra");
    process.exitCode = 1;
    return;
  }

  console.log(`Fetching and extracting source: ${args.sourceUrl}`);
  const sourceText = await fetchAndExtractSource(args.sourceUrl);
  console.log(`Extracted ${sourceText.length} characters.  Running the approved 4-call matrix (A/B/C/D)...`);

  const variants = [
    { id: "A", model: "gpt-4o-mini", promptCondition: "current" },
    { id: "B", model: "gpt-4o-mini", promptCondition: "improved" },
    { id: "C", model: args.strongerModel, promptCondition: "current" },
    { id: "D", model: args.strongerModel, promptCondition: "improved" },
  ];

  const results = [];
  for (const variant of variants) {
    console.log(`--- Variant ${variant.id}: ${variant.model} / ${variant.promptCondition} ---`);
    const result = await callOnce({ ...variant, sourceUrl: args.sourceUrl, sourceText, apiKey });
    results.push({ variantId: variant.id, ...result });
    if (result.error) {
      console.error(`Variant ${variant.id} FAILED: ${result.error}`);
    } else {
      console.log(
        `Variant ${variant.id} OK - tokens: ${result.usage?.totalTokens ?? "?"}, est. cost: $${result.estimatedCostUsd ?? "?"}, latency: ${result.variantMeta.latencyMs}ms`,
      );
    }
  }

  mkdirSync(args.out, { recursive: true });
  const outPath = join(args.out, `ds01-matrix-${Date.now()}.json`);
  writeFileSync(outPath, JSON.stringify({ sourceUrl: args.sourceUrl, results }, null, 2), "utf-8");
  console.log(`\nAll 4 results written to: ${outPath}`);
  console.log("Do not commit this file - see the header comment on copyrighted source text.");
}

function writeResult(outDir, label, result) {
  mkdirSync(outDir, { recursive: true });
  const outPath = join(outDir, `ds01-${label}-${Date.now()}.json`);
  writeFileSync(outPath, JSON.stringify(result, null, 2), "utf-8");
  if (result.error) {
    console.error(result.error);
  } else {
    console.log(
      `${label} - tokens: ${result.usage?.totalTokens ?? "?"}, est. cost: $${result.estimatedCostUsd ?? "?"}, latency: ${result.variantMeta.latencyMs}ms`,
    );
  }
  console.log(`Result written to: ${outPath}`);
}

async function main() {
  loadLocalEnvIfPresent();
  const args = parseArgs(process.argv.slice(2));

  if (args.mode === "fetch-source") {
    // No API key needed - this mode makes no OpenAI call.
    await runFetchSource(args);
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

  if (args.mode === "run-matrix") {
    await runMatrix(args, apiKey);
  } else if (args.mode === "single") {
    await runSingle(args, apiKey);
  } else {
    console.error('--mode must be "fetch-source", "single", or "run-matrix".');
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error("Evaluation harness failed:", error);
  process.exitCode = 1;
});
