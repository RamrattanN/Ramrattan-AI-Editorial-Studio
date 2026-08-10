import type { Pool } from "pg";
import { afterAll, beforeEach, describe, expect, it } from "vitest";
import { closeTestDb, setupTestDb, truncateAll } from "./helpers/testDb.js";
import { buildTestApp, signInAgent } from "./helpers/testApp.js";

let pool: Pool;

describe("Author isolation", () => {
  beforeEach(async () => {
    pool = await setupTestDb();
    await truncateAll(pool);
  });

  afterAll(async () => {
    await closeTestDb();
  });

  it("prevents one Author from reading another Author's project by id", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const ownerAgent = await signInAgent(app, emailProvider, "owner@example.com");
    const intruderAgent = await signInAgent(app, emailProvider, "intruder@example.com");

    const created = await ownerAgent.post("/api/projects");
    const projectId = created.body.project.id;

    const ownerView = await ownerAgent.get(`/api/projects/${projectId}`);
    expect(ownerView.status).toBe(200);

    const intruderView = await intruderAgent.get(`/api/projects/${projectId}`);
    expect(intruderView.status).toBe(404);
  });

  it("prevents one Author's project from appearing in another Author's list", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const ownerAgent = await signInAgent(app, emailProvider, "listowner@example.com");
    const otherAgent = await signInAgent(app, emailProvider, "otherlist@example.com");

    await ownerAgent.post("/api/projects");
    const otherList = await otherAgent.get("/api/projects");

    expect(otherList.status).toBe(200);
    expect(otherList.body.projects).toHaveLength(0);
  });

  it("prevents a non-owner from submitting a source to another Author's project", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const ownerAgent = await signInAgent(app, emailProvider, "sourceowner@example.com");
    const intruderAgent = await signInAgent(app, emailProvider, "sourceintruder@example.com");

    const created = await ownerAgent.post("/api/projects");
    const projectId = created.body.project.id;

    const attempt = await intruderAgent
      .post(`/api/projects/${projectId}/source`)
      .send({ url: "https://example.com/article" });
    expect(attempt.status).toBe(404);
  });

  it("prevents a non-owner from approving or rejecting another Author's Editorial Direction", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const ownerAgent = await signInAgent(app, emailProvider, "decisionowner@example.com");
    const intruderAgent = await signInAgent(
      app,
      emailProvider,
      "decisionintruder@example.com",
    );

    const created = await ownerAgent.post("/api/projects");
    const projectId = created.body.project.id;

    const approveAttempt = await intruderAgent.post(
      `/api/projects/${projectId}/direction/approve`,
    );
    expect(approveAttempt.status).toBe(404);

    const rejectAttempt = await intruderAgent
      .post(`/api/projects/${projectId}/direction/reject`)
      .send({ feedback: "not mine to reject" });
    expect(rejectAttempt.status).toBe(404);
  });

  it("rejects a project id that does not exist for any Author", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "nonexistent@example.com");

    const response = await agent.get("/api/projects/REP-DEADBEEF");
    expect(response.status).toBe(404);
  });
});
