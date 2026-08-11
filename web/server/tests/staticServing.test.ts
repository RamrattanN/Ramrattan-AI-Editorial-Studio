import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { Pool } from "pg";
import supertest from "supertest";
import { afterAll, afterEach, beforeEach, describe, expect, it } from "vitest";
import { closeTestDb, setupTestDb, truncateAll } from "./helpers/testDb.js";
import { buildTestApp } from "./helpers/testApp.js";

let pool: Pool;
let distDir: string | undefined;

describe("single-origin static serving (hosted deployment topology)", () => {
  beforeEach(async () => {
    pool = await setupTestDb();
    await truncateAll(pool);
  });

  afterEach(() => {
    if (distDir) {
      rmSync(distDir, { recursive: true, force: true });
      distDir = undefined;
    }
  });

  afterAll(async () => {
    await closeTestDb();
  });

  it("falls back to index.html for a client-routed path when a client build is present", async () => {
    distDir = mkdtempSync(join(tmpdir(), "ramrattan-client-dist-"));
    writeFileSync(join(distDir, "index.html"), "<!doctype html><title>Ramrattan</title>");

    const { app } = buildTestApp(pool, distDir);
    const response = await supertest(app).get("/projects/REP-AAAAAAAA");
    expect(response.status).toBe(200);
    expect(response.text).toContain("<title>Ramrattan</title>");
  });

  it("still serves the real API under /api/* instead of the SPA fallback", async () => {
    distDir = mkdtempSync(join(tmpdir(), "ramrattan-client-dist-"));
    writeFileSync(join(distDir, "index.html"), "<!doctype html><title>Ramrattan</title>");

    const { app } = buildTestApp(pool, distDir);
    const response = await supertest(app).get("/api/projects");
    expect(response.status).toBe(401);
    expect(response.body).toEqual({ error: "Authentication required." });
  });

  it("returns a plain 404 for an unmatched route when no client build is configured", async () => {
    const { app } = buildTestApp(pool);
    const response = await supertest(app).get("/projects/REP-AAAAAAAA");
    expect(response.status).toBe(404);
  });
});
