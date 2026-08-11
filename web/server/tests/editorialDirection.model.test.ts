import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

/**
 * DEC-030 (product/validation/Product_Decisions.md) regression coverage:
 * guards the two things that decision actually approved - the Editorial
 * Direction model and the exact instructions text - against silent drift,
 * while confirming everything DEC-030 explicitly left unchanged (schema,
 * request shape) really is unchanged.  Mocks the `openai` package at the
 * module boundary so no real network call is made; `projects.test.ts`
 * already covers the surrounding persistence/workflow behavior by mocking
 * `generateEditorialDirection` itself, one level up from here.
 */

// Independently transcribed from web/server/eval/editorial-direction-eval.mjs's
// IMPROVED_SYSTEM_PROMPT (verified byte-for-byte identical to production's
// SYSTEM_PROMPT at implementation time - see
// docs/product/version2/Editorial_Direction_Quality_Investigation.md
// Section 15).  Kept as a separate literal, not re-imported from source, so
// this test actually catches accidental drift in the production constant.
const APPROVED_SYSTEM_PROMPT = `You are a skilled editor at Ramrattan AI Editorial Studio, reading source
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

const APPROVED_SCHEMA = {
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

const SAMPLE_COMPLETION = {
  model: "gpt-5.6-terra",
  id: "test-request-id",
  usage: { prompt_tokens: 10, completion_tokens: 5, total_tokens: 15 },
  choices: [
    {
      message: {
        content: JSON.stringify({
          source_understanding: "Summary.",
          audience: "Audience",
          objective: "Objective",
          publication_language: "US English",
          primary_angle: "Angle",
          supporting_lenses: [],
          editorial_thesis: "Thesis.",
        }),
      },
    },
  ],
};

const mockCreate = vi.fn();

vi.mock("openai", () => ({
  default: vi.fn().mockImplementation(function () {
    return { chat: { completions: { create: mockCreate } } };
  }),
}));

describe("Editorial Direction model and prompt configuration (DEC-030)", () => {
  const originalApiKey = process.env.OPENAI_API_KEY;
  const originalModel = process.env.OPENAI_MODEL;

  beforeEach(() => {
    vi.resetModules();
    mockCreate.mockReset();
    mockCreate.mockResolvedValue(SAMPLE_COMPLETION);
    process.env.OPENAI_API_KEY = "test-key";
    delete process.env.OPENAI_MODEL;
  });

  afterEach(() => {
    if (originalApiKey === undefined) delete process.env.OPENAI_API_KEY;
    else process.env.OPENAI_API_KEY = originalApiKey;
    if (originalModel === undefined) delete process.env.OPENAI_MODEL;
    else process.env.OPENAI_MODEL = originalModel;
  });

  it("uses the DEC-030-approved gpt-5.6-terra model by default", async () => {
    const { generateEditorialDirection } = await import("../src/openai/editorialDirection.js");
    await generateEditorialDirection("https://example.com/article", "Source text.");

    expect(mockCreate).toHaveBeenCalledTimes(1);
    expect(mockCreate.mock.calls[0][0]).toMatchObject({ model: "gpt-5.6-terra" });
  });

  it("still respects an explicit OPENAI_MODEL override", async () => {
    process.env.OPENAI_MODEL = "gpt-4o";
    const { generateEditorialDirection } = await import("../src/openai/editorialDirection.js");
    await generateEditorialDirection("https://example.com/article", "Source text.");

    expect(mockCreate.mock.calls[0][0]).toMatchObject({ model: "gpt-4o" });
  });

  it("sends the exact DEC-030-approved Editorial Direction instructions as the system message", async () => {
    const { generateEditorialDirection } = await import("../src/openai/editorialDirection.js");
    await generateEditorialDirection("https://example.com/article", "Source text.");

    const requestBody = mockCreate.mock.calls[0][0] as {
      messages: Array<{ role: string; content: string }>;
    };
    const systemMessage = requestBody.messages.find((message) => message.role === "system");
    expect(systemMessage?.content).toBe(APPROVED_SYSTEM_PROMPT);
  });

  it("leaves the Structured Outputs schema unchanged, per DEC-030's scope boundary", async () => {
    const { generateEditorialDirection } = await import("../src/openai/editorialDirection.js");
    await generateEditorialDirection("https://example.com/article", "Source text.");

    const requestBody = mockCreate.mock.calls[0][0] as {
      response_format: { type: string; json_schema: unknown };
    };
    expect(requestBody.response_format).toEqual({
      type: "json_schema",
      json_schema: APPROVED_SCHEMA,
    });
  });

  it("includes the source URL and text in the user message, unchanged from before DEC-030", async () => {
    const { generateEditorialDirection } = await import("../src/openai/editorialDirection.js");
    await generateEditorialDirection("https://example.com/article", "Source text.");

    const requestBody = mockCreate.mock.calls[0][0] as {
      messages: Array<{ role: string; content: string }>;
    };
    const userMessage = requestBody.messages.find((message) => message.role === "user");
    expect(userMessage?.content).toBe(
      "Source URL: https://example.com/article\n\nSource content:\nSource text.",
    );
  });
});
