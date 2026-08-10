import type { Pool } from "pg";
import supertest from "supertest";
import { afterAll, beforeEach, describe, expect, it } from "vitest";
import { closeTestDb, setupTestDb, truncateAll } from "./helpers/testDb.js";
import { buildTestApp } from "./helpers/testApp.js";

let pool: Pool;

describe("authentication", () => {
  beforeEach(async () => {
    pool = await setupTestDb();
    await truncateAll(pool);
  });

  afterAll(async () => {
    await closeTestDb();
  });

  it("rejects unauthenticated access to projects", async () => {
    const { app } = buildTestApp(pool);
    const response = await supertest(app).get("/api/projects");
    expect(response.status).toBe(401);
  });

  it("completes the magic-link flow and establishes a session", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = supertest.agent(app);

    const requestResponse = await agent
      .post("/api/auth/request-link")
      .send({ email: "author@example.com" });
    expect(requestResponse.status).toBe(200);
    expect(emailProvider.sent).toHaveLength(1);
    expect(emailProvider.sent[0].email).toBe("author@example.com");

    const token = emailProvider.lastToken();
    const callbackResponse = await agent
      .post("/api/auth/callback")
      .send({ token });
    expect(callbackResponse.status).toBe(200);
    expect(callbackResponse.body.email).toBe("author@example.com");

    const meResponse = await agent.get("/api/auth/me");
    expect(meResponse.status).toBe(200);
    expect(meResponse.body.email).toBe("author@example.com");

    const projectsResponse = await agent.get("/api/projects");
    expect(projectsResponse.status).toBe(200);
  });

  it("rejects an invalid or already-used token", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = supertest.agent(app);

    await agent.post("/api/auth/request-link").send({ email: "once@example.com" });
    const token = emailProvider.lastToken();

    const first = await agent.post("/api/auth/callback").send({ token });
    expect(first.status).toBe(200);

    const second = await supertest
      .agent(app)
      .post("/api/auth/callback")
      .send({ token });
    expect(second.status).toBe(401);

    const bogus = await supertest
      .agent(app)
      .post("/api/auth/callback")
      .send({ token: "not-a-real-token" });
    expect(bogus.status).toBe(401);
  });

  it("signs out and revokes access", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = supertest.agent(app);

    await agent.post("/api/auth/request-link").send({ email: "signout@example.com" });
    await agent.post("/api/auth/callback").send({ token: emailProvider.lastToken() });

    const beforeLogout = await agent.get("/api/projects");
    expect(beforeLogout.status).toBe(200);

    const logout = await agent.post("/api/auth/logout");
    expect(logout.status).toBe(204);

    const afterLogout = await agent.get("/api/projects");
    expect(afterLogout.status).toBe(401);
  });
});
