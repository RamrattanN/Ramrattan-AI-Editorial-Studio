import type { Pool } from "pg";
import { afterAll, beforeEach, describe, expect, it, vi } from "vitest";
import { closeTestDb, setupTestDb, truncateAll } from "./helpers/testDb.js";
import { buildTestApp, signInAgent } from "./helpers/testApp.js";

vi.mock("../src/openai/editorialDirection.js", () => ({
  generateEditorialDirection: vi.fn(),
}));
vi.mock("../src/source/retrieve.js", () => ({
  retrieveSource: vi.fn(),
}));

import { generateEditorialDirection } from "../src/openai/editorialDirection.js";
import { retrieveSource } from "../src/source/retrieve.js";

const mockedGenerate = vi.mocked(generateEditorialDirection);
const mockedRetrieve = vi.mocked(retrieveSource);

const SAMPLE_DIRECTION = {
  source_understanding: "The source explains a shift in editorial workflow ownership.",
  audience: "Product and engineering leaders",
  objective: "Explain why application-owned state beats prompt-driven workflows",
  publication_language: "US English",
  primary_angle: "The application must own workflow state, not the model",
  supporting_lenses: ["A migration path for teams still prompt-driving state"],
  editorial_thesis:
    "Durable products keep AI bounded to editorial tasks and let real UI own the workflow.",
};

let pool: Pool;

describe("editorial projects", () => {
  beforeEach(async () => {
    pool = await setupTestDb();
    await truncateAll(pool);
    mockedGenerate.mockReset();
    mockedRetrieve.mockReset();
  });

  afterAll(async () => {
    await closeTestDb();
  });

  it("creates a project with a persistent REP- id scoped to the Author", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "creator@example.com");

    const created = await agent.post("/api/projects");
    expect(created.status).toBe(201);
    expect(created.body.project.id).toMatch(/^REP-[A-F0-9]{8}$/);
    expect(created.body.project.stage).toBe("source_intake");

    const listed = await agent.get("/api/projects");
    expect(listed.status).toBe(200);
    expect(listed.body.projects).toHaveLength(1);
    expect(listed.body.projects[0].id).toBe(created.body.project.id);
  });

  it("rejects an invalid submitted URL", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "badurl@example.com");
    const created = await agent.post("/api/projects");
    const projectId = created.body.project.id;

    const response = await agent
      .post(`/api/projects/${projectId}/source`)
      .send({ url: "not a url" });
    expect(response.status).toBe(400);

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.source).toBeNull();
    expect(mockedRetrieve).not.toHaveBeenCalled();
  });

  it("persists the source URL and the resulting Editorial Direction", async () => {
    mockedRetrieve.mockResolvedValue({ ok: true, text: "Retrieved article text." });
    mockedGenerate.mockResolvedValue({ ok: true, data: SAMPLE_DIRECTION });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "flow@example.com");
    const created = await agent.post("/api/projects");
    const projectId = created.body.project.id;

    const submitted = await agent
      .post(`/api/projects/${projectId}/source`)
      .send({ url: "https://example.com/article" });
    expect(submitted.status).toBe(200);
    expect(submitted.body.editorialDirection.primaryAngle).toBe(
      SAMPLE_DIRECTION.primary_angle,
    );
    expect(submitted.body.editorialDirection.supportingLenses).toHaveLength(1);
    expect(submitted.body.editorialDirection.status).toBe("proposed");

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.project.stage).toBe("editorial_direction");
    expect(view.body.source.rawReference).toBe("https://example.com/article");
    expect(view.body.source.retrievalStatus).toBe("succeeded");
    expect(view.body.editorialDirection.editorialThesis).toBe(
      SAMPLE_DIRECTION.editorial_thesis,
    );
  });

  it("never persists a source URL request again after a successful submission", async () => {
    mockedRetrieve.mockResolvedValue({ ok: true, text: "Retrieved article text." });
    mockedGenerate.mockResolvedValue({ ok: true, data: SAMPLE_DIRECTION });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "nourl@example.com");
    const created = await agent.post("/api/projects");
    const projectId = created.body.project.id;

    await agent
      .post(`/api/projects/${projectId}/source`)
      .send({ url: "https://example.com/article" });

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.source.rawReference).toBe("https://example.com/article");
  });

  it("does not persist malformed OpenAI structured output", async () => {
    mockedRetrieve.mockResolvedValue({ ok: true, text: "Retrieved article text." });
    mockedGenerate.mockResolvedValue({
      ok: false,
      error: "The model's output failed validation.",
    });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "malformed@example.com");
    const created = await agent.post("/api/projects");
    const projectId = created.body.project.id;

    const submitted = await agent
      .post(`/api/projects/${projectId}/source`)
      .send({ url: "https://example.com/article" });
    expect(submitted.status).toBe(502);

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.editorialDirection).toBeNull();
    expect(view.body.project.stage).toBe("source_intake");
  });

  it("returns a plain failure when source retrieval fails, without fabricating content", async () => {
    mockedRetrieve.mockResolvedValue({
      ok: false,
      error: "The source could not be retrieved.",
    });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "retrievalfail@example.com");
    const created = await agent.post("/api/projects");
    const projectId = created.body.project.id;

    const submitted = await agent
      .post(`/api/projects/${projectId}/source`)
      .send({ url: "https://example.com/unreachable" });
    expect(submitted.status).toBe(422);
    expect(mockedGenerate).not.toHaveBeenCalled();

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.source.retrievalStatus).toBe("failed");
    expect(view.body.editorialDirection).toBeNull();
  });

  it("approves the Editorial Direction and advances state", async () => {
    mockedRetrieve.mockResolvedValue({ ok: true, text: "Retrieved article text." });
    mockedGenerate.mockResolvedValue({ ok: true, data: SAMPLE_DIRECTION });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "approve@example.com");
    const created = await agent.post("/api/projects");
    const projectId = created.body.project.id;
    await agent
      .post(`/api/projects/${projectId}/source`)
      .send({ url: "https://example.com/article" });

    const approved = await agent.post(`/api/projects/${projectId}/direction/approve`);
    expect(approved.status).toBe(200);
    expect(approved.body.editorialDirection.status).toBe("approved");
    expect(approved.body.editorialDirection.decidedAt).not.toBeNull();
  });

  it("persists rejection feedback without discarding the project or source", async () => {
    mockedRetrieve.mockResolvedValue({ ok: true, text: "Retrieved article text." });
    mockedGenerate.mockResolvedValue({ ok: true, data: SAMPLE_DIRECTION });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "reject@example.com");
    const created = await agent.post("/api/projects");
    const projectId = created.body.project.id;
    await agent
      .post(`/api/projects/${projectId}/source`)
      .send({ url: "https://example.com/article" });

    const rejected = await agent
      .post(`/api/projects/${projectId}/direction/reject`)
      .send({ feedback: "Please sharpen the primary angle." });
    expect(rejected.status).toBe(200);
    expect(rejected.body.editorialDirection.status).toBe("rejected");
    expect(rejected.body.editorialDirection.rejectFeedback).toBe(
      "Please sharpen the primary angle.",
    );
    // DEC-029: Reject is a durable, stage-local decision - it persists a
    // decision timestamp like Approve does, and does not advance the
    // project stage (unlike Approve, which does).
    expect(rejected.body.editorialDirection.decidedAt).not.toBeNull();

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.project.id).toBe(projectId);
    expect(view.body.project.stage).toBe("editorial_direction");
    expect(view.body.source.rawReference).toBe("https://example.com/article");
    expect(view.body.editorialDirection.status).toBe("rejected");
  });

  it("rehydrates full project state after a simulated page refresh", async () => {
    mockedRetrieve.mockResolvedValue({ ok: true, text: "Retrieved article text." });
    mockedGenerate.mockResolvedValue({ ok: true, data: SAMPLE_DIRECTION });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "refresh@example.com");
    const created = await agent.post("/api/projects");
    const projectId = created.body.project.id;
    await agent
      .post(`/api/projects/${projectId}/source`)
      .send({ url: "https://example.com/article" });
    await agent.post(`/api/projects/${projectId}/direction/approve`);

    // A "refresh" is simply a fresh GET with the same session cookie - the
    // application/database state is authoritative, not any in-memory or
    // conversational state.
    const rehydrated = await agent.get(`/api/projects/${projectId}`);
    expect(rehydrated.status).toBe(200);
    expect(rehydrated.body.project.stage).toBe("editorial_direction");
    expect(rehydrated.body.source.rawReference).toBe("https://example.com/article");
    expect(rehydrated.body.editorialDirection.status).toBe("approved");
    expect(rehydrated.body.editorialDirection.primaryAngle).toBe(
      SAMPLE_DIRECTION.primary_angle,
    );
  });
});
