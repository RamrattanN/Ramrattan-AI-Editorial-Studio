import { Router } from "express";
import { z } from "zod";
import { getAuthorId, requireAuth } from "../auth/middleware.js";
import { generateArticleDraft } from "../openai/articleDraft.js";
import { generateEditorialDirection } from "../openai/editorialDirection.js";
import { generateEditorialPlan } from "../openai/editorialPlan.js";
import { retrieveSource } from "../source/retrieve.js";
import { isValidProjectId } from "./id.js";
import { ProjectNotFoundError, ProjectRepository } from "./repository.js";

const submitSourceSchema = z.object({
  url: z.string().trim().min(1),
});

const rejectSchema = z.object({
  feedback: z.string().trim().max(2000).optional().default(""),
});

/**
 * Wraps a route param project id check plus a shared 404 mapping for
 * ProjectNotFoundError, so ownership failures always render as 404 rather
 * than leaking whether a project id exists for a different Author.
 */
function projectIdParam(req: { params: Record<string, string> }): string | null {
  const id = req.params.id;
  return isValidProjectId(id) ? id : null;
}

export function createProjectsRouter(repository: ProjectRepository): Router {
  const router = Router();
  router.use(requireAuth);

  router.get("/", async (req, res) => {
    const authorId = getAuthorId(req);
    const projects = await repository.listProjects(authorId);
    res.json({ projects });
  });

  router.post("/", async (req, res) => {
    const authorId = getAuthorId(req);
    const project = await repository.createProject(authorId);
    res.status(201).json({ project });
  });

  router.get("/:id", async (req, res) => {
    const authorId = getAuthorId(req);
    const id = projectIdParam(req);
    if (!id) {
      res.status(404).json({ error: "Project not found." });
      return;
    }
    const view = await repository.getProjectView(id, authorId);
    if (!view) {
      res.status(404).json({ error: "Project not found." });
      return;
    }
    res.json(view);
  });

  router.post("/:id/source", async (req, res) => {
    const authorId = getAuthorId(req);
    const id = projectIdParam(req);
    if (!id) {
      res.status(404).json({ error: "Project not found." });
      return;
    }

    const parsed = submitSourceSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: "A URL is required." });
      return;
    }

    let url: URL;
    try {
      url = new URL(parsed.data.url);
    } catch {
      res.status(400).json({ error: "That does not look like a valid URL." });
      return;
    }

    let source;
    try {
      source = await repository.createSource(id, authorId, url.toString());
    } catch (error) {
      if (error instanceof ProjectNotFoundError) {
        res.status(404).json({ error: "Project not found." });
        return;
      }
      throw error;
    }

    const retrieval = await retrieveSource(url.toString());
    if (!retrieval.ok) {
      await repository.markSourceFailed(source.id, retrieval.error);
      res.status(422).json({ error: retrieval.error });
      return;
    }

    await repository.markSourceSucceeded(source.id, retrieval.text);

    const direction = await generateEditorialDirection(url.toString(), retrieval.text);
    if (!direction.ok) {
      res.status(502).json({
        error:
          "The editorial direction could not be generated right now. Please try again.",
        detail: direction.error,
      });
      return;
    }

    const saved = await repository.createEditorialDirection(id, authorId, {
      sourceUnderstanding: direction.data.source_understanding,
      audience: direction.data.audience,
      objective: direction.data.objective,
      publicationLanguage: direction.data.publication_language,
      primaryAngle: direction.data.primary_angle,
      supportingLenses: direction.data.supporting_lenses,
      editorialThesis: direction.data.editorial_thesis,
    });

    res.status(200).json({ editorialDirection: saved });
  });

  router.post("/:id/direction/approve", async (req, res) => {
    const authorId = getAuthorId(req);
    const id = projectIdParam(req);
    if (!id) {
      res.status(404).json({ error: "Project not found." });
      return;
    }
    try {
      const approved = await repository.approveDirection(id, authorId);
      if (!approved) {
        res.status(404).json({ error: "No Editorial Direction to approve yet." });
        return;
      }

      // Web Walking Skeleton 02 (BL-003): the Repository Author's
      // synchronous-generation decision (Web_Walking_Skeleton_02_Scope.md
      // Section 11) extends this same request to also propose the
      // Editorial Plan, mirroring how /source already generates the
      // Editorial Direction synchronously with retrieval.
      const direction = approved.direction;
      const plan = await generateEditorialPlan({
        sourceUnderstanding: direction.sourceUnderstanding,
        audience: direction.audience,
        objective: direction.objective,
        primaryAngle: direction.primaryAngle,
        supportingLenses: direction.supportingLenses,
        editorialThesis: direction.editorialThesis,
      });
      if (!plan.ok) {
        // The Direction approval itself already succeeded and persisted;
        // only the Plan proposal failed. Report it distinctly so the
        // client can retry plan generation without re-approving.
        res.status(200).json({
          editorialDirection: approved.direction,
          project: approved.project,
          editorialPlan: null,
          planError: plan.error,
        });
        return;
      }

      const savedPlan = await repository.upsertEditorialPlan(id, authorId, {
        headline: plan.data.headline,
        hook: plan.data.hook,
        keyInsights: plan.data.key_insights,
        practicalTakeaway: plan.data.practical_takeaway,
        ctaDirection: plan.data.cta_direction,
      });

      res.status(200).json({
        editorialDirection: approved.direction,
        project: approved.project,
        editorialPlan: savedPlan,
      });
    } catch (error) {
      if (error instanceof ProjectNotFoundError) {
        res.status(404).json({ error: "Project not found." });
        return;
      }
      throw error;
    }
  });

  router.post("/:id/direction/reject", async (req, res) => {
    const authorId = getAuthorId(req);
    const id = projectIdParam(req);
    if (!id) {
      res.status(404).json({ error: "Project not found." });
      return;
    }
    const parsed = rejectSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: "Invalid feedback." });
      return;
    }
    try {
      const direction = await repository.rejectDirection(
        id,
        authorId,
        parsed.data.feedback,
      );
      if (!direction) {
        res.status(404).json({ error: "No Editorial Direction to reject yet." });
        return;
      }
      res.json({ editorialDirection: direction });
    } catch (error) {
      if (error instanceof ProjectNotFoundError) {
        res.status(404).json({ error: "Project not found." });
        return;
      }
      throw error;
    }
  });

  router.post("/:id/plan/approve", async (req, res) => {
    const authorId = getAuthorId(req);
    const id = projectIdParam(req);
    if (!id) {
      res.status(404).json({ error: "Project not found." });
      return;
    }
    try {
      const approvedPlan = await repository.approvePlan(id, authorId);
      if (!approvedPlan) {
        res.status(404).json({ error: "No Editorial Plan to approve yet." });
        return;
      }

      // Synchronous Draft generation, per the same Repository Author
      // decision applied to Editorial Plan generation
      // (Web_Walking_Skeleton_02_Scope.md Section 11).
      const draft = await generateArticleDraft({
        headline: approvedPlan.headline,
        hook: approvedPlan.hook,
        keyInsights: approvedPlan.keyInsights,
        practicalTakeaway: approvedPlan.practicalTakeaway,
        ctaDirection: approvedPlan.ctaDirection,
      });
      if (!draft.ok) {
        // Technical-failure Generation outcome (scope document Section
        // 5): no Article is persisted and the project stage does not
        // advance. The plan stays approved so retrying is just a
        // re-call of this same endpoint.
        res.status(200).json({
          editorialPlan: approvedPlan,
          article: null,
          draftError: draft.error,
        });
        return;
      }

      const view = await repository.getProjectView(id, authorId);
      const sourceReference = view?.source?.rawReference ?? "Author-supplied source.";

      const result = await repository.createArticleAndAdvanceStage(id, authorId, {
        headline: draft.data.headline,
        hook: draft.data.hook,
        keyInsights: draft.data.key_insights,
        practicalTakeaway: draft.data.practical_takeaway,
        cta: draft.data.cta,
        articleMarkdown: draft.data.article_markdown,
        sourceAttributions: [{ citation: sourceReference }],
      });

      res.status(200).json({
        editorialPlan: approvedPlan,
        article: result.article,
        project: result.project,
      });
    } catch (error) {
      if (error instanceof ProjectNotFoundError) {
        res.status(404).json({ error: "Project not found." });
        return;
      }
      throw error;
    }
  });

  router.post("/:id/plan/revise", async (req, res) => {
    const authorId = getAuthorId(req);
    const id = projectIdParam(req);
    if (!id) {
      res.status(404).json({ error: "Project not found." });
      return;
    }
    try {
      const revisionRequested = await repository.requestPlanRevision(id, authorId);
      if (!revisionRequested) {
        res.status(404).json({ error: "No Editorial Plan to revise yet." });
        return;
      }

      const direction = await repository.getEditorialDirection(id, authorId);
      if (!direction) {
        res.status(404).json({ error: "No Editorial Direction found for this project." });
        return;
      }

      const plan = await generateEditorialPlan({
        sourceUnderstanding: direction.sourceUnderstanding,
        audience: direction.audience,
        objective: direction.objective,
        primaryAngle: direction.primaryAngle,
        supportingLenses: direction.supportingLenses,
        editorialThesis: direction.editorialThesis,
      });
      if (!plan.ok) {
        // revision_requested is a transient state: on regeneration
        // failure the plan simply stays there (with its prior content
        // still visible) so the Author can retry, rather than silently
        // reverting to the old proposal.
        res.status(200).json({ editorialPlan: revisionRequested, planError: plan.error });
        return;
      }

      const savedPlan = await repository.upsertEditorialPlan(id, authorId, {
        headline: plan.data.headline,
        hook: plan.data.hook,
        keyInsights: plan.data.key_insights,
        practicalTakeaway: plan.data.practical_takeaway,
        ctaDirection: plan.data.cta_direction,
      });

      res.status(200).json({ editorialPlan: savedPlan });
    } catch (error) {
      if (error instanceof ProjectNotFoundError) {
        res.status(404).json({ error: "Project not found." });
        return;
      }
      throw error;
    }
  });

  return router;
}
