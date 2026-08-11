import { Router } from "express";
import { z } from "zod";
import { getAuthorId, requireAuth } from "../auth/middleware.js";
import { generateEditorialDirection } from "../openai/editorialDirection.js";
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
      res.json({ editorialDirection: approved.direction, project: approved.project });
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

  return router;
}
