import type { Pool } from "pg";
import type { Agent } from "supertest";
import { afterAll, beforeEach, describe, expect, it, vi } from "vitest";
import { closeTestDb, setupTestDb, truncateAll } from "./helpers/testDb.js";
import { buildTestApp, signInAgent } from "./helpers/testApp.js";

vi.mock("../src/openai/editorialDirection.js", () => ({
  generateEditorialDirection: vi.fn(),
}));
vi.mock("../src/openai/editorialPlan.js", () => ({
  generateEditorialPlan: vi.fn(),
}));
vi.mock("../src/openai/articleDraft.js", () => ({
  generateArticleDraft: vi.fn(),
}));
vi.mock("../src/source/retrieve.js", () => ({
  retrieveSource: vi.fn(),
}));

import { generateArticleDraft } from "../src/openai/articleDraft.js";
import { generateEditorialDirection } from "../src/openai/editorialDirection.js";
import { generateEditorialPlan } from "../src/openai/editorialPlan.js";
import { retrieveSource } from "../src/source/retrieve.js";

const mockedGenerateDirection = vi.mocked(generateEditorialDirection);
const mockedGeneratePlan = vi.mocked(generateEditorialPlan);
const mockedGenerateDraft = vi.mocked(generateArticleDraft);
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

const SAMPLE_PLAN = {
  headline: "Why Your Product Should Own Its Own Workflow State",
  hook: "Most AI features quietly outsource state management to the model. That's a mistake.",
  key_insights: [
    "The model should propose; the application should decide and persist.",
    "Durable stage transitions belong in the database, not in conversation history.",
  ],
  practical_takeaway: "Audit every AI-touched workflow for who actually owns the next-state decision.",
  cta_direction: "Invite readers to share where their own products blur this line.",
};

const SAMPLE_PLAN_REVISION = {
  ...SAMPLE_PLAN,
  headline: "Revised: Why Your Product Should Own Its Own Workflow State",
};

const SAMPLE_DRAFT = {
  headline: SAMPLE_PLAN.headline,
  hook: SAMPLE_PLAN.hook,
  key_insights: SAMPLE_PLAN.key_insights,
  practical_takeaway: SAMPLE_PLAN.practical_takeaway,
  cta: SAMPLE_PLAN.cta_direction,
  article_markdown: "# Why Your Product Should Own Its Own Workflow State\n\nFull article body.",
};

let pool: Pool;

async function createApprovedDirectionProject(agent: Agent) {
  mockedRetrieve.mockResolvedValue({ ok: true, text: "Retrieved article text." });
  mockedGenerateDirection.mockResolvedValue({ ok: true, data: SAMPLE_DIRECTION });
  mockedGeneratePlan.mockResolvedValue({ ok: true, data: SAMPLE_PLAN });

  const created = await agent.post("/api/projects");
  const projectId = created.body.project.id;
  await agent.post(`/api/projects/${projectId}/source`).send({
    url: "https://example.com/article",
  });
  return projectId as string;
}

describe("Editorial Plan and Draft (Web Walking Skeleton 02)", () => {
  beforeEach(async () => {
    pool = await setupTestDb();
    await truncateAll(pool);
    mockedGenerateDirection.mockReset();
    mockedGeneratePlan.mockReset();
    mockedGenerateDraft.mockReset();
    mockedRetrieve.mockReset();
  });

  afterAll(async () => {
    await closeTestDb();
  });

  it("generates and persists an Editorial Plan synchronously with Direction approval", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "plan-approve@example.com");
    const projectId = await createApprovedDirectionProject(agent);

    const approved = await agent.post(`/api/projects/${projectId}/direction/approve`);
    expect(approved.status).toBe(200);
    expect(approved.body.project.stage).toBe("editorial_plan");
    expect(approved.body.editorialPlan.status).toBe("proposed");
    expect(approved.body.editorialPlan.headline).toBe(SAMPLE_PLAN.headline);
    expect(mockedGeneratePlan).toHaveBeenCalledTimes(1);

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.editorialPlan.headline).toBe(SAMPLE_PLAN.headline);
    expect(view.body.editorialPlan.keyInsights).toHaveLength(2);
  });

  it("does not persist a malformed Editorial Plan and leaves the direction approved", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "plan-malformed@example.com");
    const projectId = await createApprovedDirectionProject(agent);
    mockedGeneratePlan.mockResolvedValue({
      ok: false,
      error: "The model's output failed validation.",
    });

    const approved = await agent.post(`/api/projects/${projectId}/direction/approve`);
    expect(approved.status).toBe(200);
    expect(approved.body.editorialDirection.status).toBe("approved");
    expect(approved.body.editorialPlan).toBeNull();
    expect(approved.body.planError).toBeTruthy();

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.editorialPlan).toBeNull();
  });

  it("approves the plan, generates a Draft, and advances the project to draft", async () => {
    mockedGenerateDraft.mockResolvedValue({ ok: true, data: SAMPLE_DRAFT });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "draft-generate@example.com");
    const projectId = await createApprovedDirectionProject(agent);
    await agent.post(`/api/projects/${projectId}/direction/approve`);

    const approvedPlan = await agent.post(`/api/projects/${projectId}/plan/approve`);
    expect(approvedPlan.status).toBe(200);
    expect(approvedPlan.body.editorialPlan.status).toBe("approved");
    expect(approvedPlan.body.article.articleMarkdown).toBe(SAMPLE_DRAFT.article_markdown);
    expect(approvedPlan.body.project.stage).toBe("draft");
    expect(approvedPlan.body.article.sourceAttributions).toHaveLength(1);
    expect(approvedPlan.body.article.sourceAttributions[0].citation).toBe(
      "https://example.com/article",
    );

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.project.stage).toBe("draft");
    expect(view.body.article.headline).toBe(SAMPLE_DRAFT.headline);
  });

  it("does not persist a malformed Draft and keeps the project at editorial_plan", async () => {
    mockedGenerateDraft.mockResolvedValue({
      ok: false,
      error: "The model's output failed validation.",
    });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "draft-malformed@example.com");
    const projectId = await createApprovedDirectionProject(agent);
    await agent.post(`/api/projects/${projectId}/direction/approve`);

    const approvedPlan = await agent.post(`/api/projects/${projectId}/plan/approve`);
    expect(approvedPlan.status).toBe(200);
    expect(approvedPlan.body.article).toBeNull();
    expect(approvedPlan.body.draftError).toBeTruthy();

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.project.stage).toBe("editorial_plan");
    expect(view.body.article).toBeNull();
    // The plan itself was already marked approved and stays approved,
    // so retrying is a plain re-call of the same endpoint.
    expect(view.body.editorialPlan.status).toBe("approved");
  });

  it("regenerates the plan on Request Revision, returning status to proposed", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "plan-revise@example.com");
    const projectId = await createApprovedDirectionProject(agent);
    await agent.post(`/api/projects/${projectId}/direction/approve`);

    mockedGeneratePlan.mockResolvedValue({ ok: true, data: SAMPLE_PLAN_REVISION });
    const revised = await agent.post(`/api/projects/${projectId}/plan/revise`);
    expect(revised.status).toBe(200);
    expect(revised.body.editorialPlan.status).toBe("proposed");
    expect(revised.body.editorialPlan.headline).toBe(SAMPLE_PLAN_REVISION.headline);
    expect(mockedGeneratePlan).toHaveBeenCalledTimes(2); // initial + revision

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.project.stage).toBe("editorial_plan");
    expect(view.body.editorialPlan.headline).toBe(SAMPLE_PLAN_REVISION.headline);
  });

  it("leaves the plan at revision_requested if regeneration fails, rather than reverting silently", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "plan-revise-fail@example.com");
    const projectId = await createApprovedDirectionProject(agent);
    await agent.post(`/api/projects/${projectId}/direction/approve`);

    mockedGeneratePlan.mockResolvedValue({
      ok: false,
      error: "The model's output failed validation.",
    });
    const revised = await agent.post(`/api/projects/${projectId}/plan/revise`);
    expect(revised.status).toBe(200);
    expect(revised.body.editorialPlan.status).toBe("revision_requested");
    expect(revised.body.planError).toBeTruthy();

    const view = await agent.get(`/api/projects/${projectId}`);
    expect(view.body.editorialPlan.status).toBe("revision_requested");
  });

  it("rehydrates the full Plan and Draft state after a simulated page refresh", async () => {
    mockedGenerateDraft.mockResolvedValue({ ok: true, data: SAMPLE_DRAFT });

    const { app, emailProvider } = buildTestApp(pool);
    const agent = await signInAgent(app, emailProvider, "rehydrate@example.com");
    const projectId = await createApprovedDirectionProject(agent);
    await agent.post(`/api/projects/${projectId}/direction/approve`);
    await agent.post(`/api/projects/${projectId}/plan/approve`);

    const rehydrated = await agent.get(`/api/projects/${projectId}`);
    expect(rehydrated.status).toBe(200);
    expect(rehydrated.body.project.stage).toBe("draft");
    expect(rehydrated.body.editorialPlan.status).toBe("approved");
    expect(rehydrated.body.article.headline).toBe(SAMPLE_DRAFT.headline);
    expect(rehydrated.body.editorialDirection.status).toBe("approved");
  });

  it("prevents a non-owner from approving or revising another Author's Editorial Plan", async () => {
    const { app, emailProvider } = buildTestApp(pool);
    const ownerAgent = await signInAgent(app, emailProvider, "plan-owner@example.com");
    const intruderAgent = await signInAgent(
      app,
      emailProvider,
      "plan-intruder@example.com",
    );

    const projectId = await createApprovedDirectionProject(ownerAgent);
    await ownerAgent.post(`/api/projects/${projectId}/direction/approve`);

    const approveAttempt = await intruderAgent.post(
      `/api/projects/${projectId}/plan/approve`,
    );
    expect(approveAttempt.status).toBe(404);

    const reviseAttempt = await intruderAgent.post(
      `/api/projects/${projectId}/plan/revise`,
    );
    expect(reviseAttempt.status).toBe(404);
  });
});
