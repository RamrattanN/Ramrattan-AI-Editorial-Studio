import { describe, expect, it } from "vitest";
import { parseArticleDraft, parseEditorialPlan } from "../src/openai/schema.js";

describe("editorial plan structured-output validation", () => {
  it("accepts a well-formed payload", () => {
    const result = parseEditorialPlan({
      headline: "Headline",
      hook: "Hook",
      key_insights: ["Insight one", "Insight two"],
      practical_takeaway: "Takeaway",
      cta_direction: "CTA direction",
    });
    expect(result.ok).toBe(true);
  });

  it("rejects an empty key_insights array", () => {
    const result = parseEditorialPlan({
      headline: "Headline",
      hook: "Hook",
      key_insights: [],
      practical_takeaway: "Takeaway",
      cta_direction: "CTA direction",
    });
    expect(result.ok).toBe(false);
  });

  it("rejects more than five key insights", () => {
    const result = parseEditorialPlan({
      headline: "Headline",
      hook: "Hook",
      key_insights: ["1", "2", "3", "4", "5", "6"],
      practical_takeaway: "Takeaway",
      cta_direction: "CTA direction",
    });
    expect(result.ok).toBe(false);
  });

  it("rejects a payload missing a required field", () => {
    const result = parseEditorialPlan({
      headline: "Headline",
      hook: "Hook",
      key_insights: ["Insight"],
      practical_takeaway: "Takeaway",
      // cta_direction intentionally omitted
    });
    expect(result.ok).toBe(false);
  });
});

describe("article draft structured-output validation", () => {
  it("accepts a well-formed payload", () => {
    const result = parseArticleDraft({
      headline: "Headline",
      hook: "Hook",
      key_insights: ["Insight one"],
      practical_takeaway: "Takeaway",
      cta: "CTA",
      article_markdown: "# Headline\n\nBody.",
    });
    expect(result.ok).toBe(true);
  });

  it("rejects a payload missing article_markdown", () => {
    const result = parseArticleDraft({
      headline: "Headline",
      hook: "Hook",
      key_insights: ["Insight one"],
      practical_takeaway: "Takeaway",
      cta: "CTA",
    });
    expect(result.ok).toBe(false);
  });

  it("rejects a non-object payload", () => {
    const result = parseArticleDraft("just a string");
    expect(result.ok).toBe(false);
  });
});
