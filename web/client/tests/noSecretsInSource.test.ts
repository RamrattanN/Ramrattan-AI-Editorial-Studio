import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SRC_DIR = join(__dirname, "..", "src");
const PACKAGE_JSON = join(__dirname, "..", "package.json");

function collectFiles(dir: string): string[] {
  const entries = readdirSync(dir);
  const files: string[] = [];
  for (const entry of entries) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      files.push(...collectFiles(full));
    } else {
      files.push(full);
    }
  }
  return files;
}

/**
 * Web Walking Skeleton 01 requires that the OpenAI API key never reach the
 * browser build. This test enforces that at the source level: the client
 * package must never reference OPENAI_API_KEY, an OpenAI-style secret
 * value, or import the `openai` SDK - the same guarantee a build-artifact
 * scan would provide, without requiring a build step in the unit-test run.
 */
describe("no secrets in frontend source", () => {
  it("never references OPENAI_API_KEY in client source", () => {
    const files = collectFiles(SRC_DIR);
    for (const file of files) {
      const content = readFileSync(file, "utf-8");
      expect(content, `${file} must not reference OPENAI_API_KEY`).not.toMatch(
        /OPENAI_API_KEY/,
      );
      expect(content, `${file} must not contain an OpenAI-style secret key`).not.toMatch(
        /sk-[A-Za-z0-9]{20,}/,
      );
    }
  });

  it("does not depend on the openai SDK in the client package", () => {
    const pkg = JSON.parse(readFileSync(PACKAGE_JSON, "utf-8"));
    const allDeps = {
      ...(pkg.dependencies ?? {}),
      ...(pkg.devDependencies ?? {}),
    };
    expect(allDeps).not.toHaveProperty("openai");
  });
});
