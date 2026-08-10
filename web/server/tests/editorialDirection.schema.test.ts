import { describe, expect, it } from "vitest";
import { parseEditorialDirection } from "../src/openai/schema.js";

describe("editorial direction structured-output validation", () => {
  it("accepts a well-formed payload with two supporting lenses", () => {
    const result = parseEditorialDirection({
      source_understanding: "The article argues X based on Y.",
      audience: "Engineering leaders",
      objective: "Explain why X matters",
      publication_language: "US English",
      primary_angle: "X changes how teams should think about Y",
      supporting_lenses: ["A counterpoint worth naming", "A practical implication"],
      editorial_thesis: "X is the right lens because Y and Z.",
    });
    expect(result.ok).toBe(true);
  });

  it("accepts zero supporting lenses", () => {
    const result = parseEditorialDirection({
      source_understanding: "Summary.",
      audience: "Audience",
      objective: "Objective",
      publication_language: "US English",
      primary_angle: "Angle",
      supporting_lenses: [],
      editorial_thesis: "Thesis.",
    });
    expect(result.ok).toBe(true);
  });

  it("rejects more than two supporting lenses", () => {
    const result = parseEditorialDirection({
      source_understanding: "Summary.",
      audience: "Audience",
      objective: "Objective",
      publication_language: "US English",
      primary_angle: "Angle",
      supporting_lenses: ["One", "Two", "Three"],
      editorial_thesis: "Thesis.",
    });
    expect(result.ok).toBe(false);
  });

  it("rejects a payload missing a required field", () => {
    const result = parseEditorialDirection({
      source_understanding: "Summary.",
      audience: "Audience",
      objective: "Objective",
      publication_language: "US English",
      primary_angle: "Angle",
      supporting_lenses: [],
      // editorial_thesis intentionally omitted
    });
    expect(result.ok).toBe(false);
  });

  it("rejects a payload with the wrong type for supporting_lenses", () => {
    const result = parseEditorialDirection({
      source_understanding: "Summary.",
      audience: "Audience",
      objective: "Objective",
      publication_language: "US English",
      primary_angle: "Angle",
      supporting_lenses: "not an array",
      editorial_thesis: "Thesis.",
    });
    expect(result.ok).toBe(false);
  });

  it("rejects a non-object payload", () => {
    const result = parseEditorialDirection("just a string");
    expect(result.ok).toBe(false);
  });
});
