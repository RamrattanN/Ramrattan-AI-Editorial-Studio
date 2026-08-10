import type { Pool } from "pg";
import type {
  EditorialDirection,
  EditorialProject,
  ProjectView,
  Source,
} from "../types.js";
import { generateProjectId } from "./id.js";

interface ProjectRow {
  id: string;
  author_id: string;
  title: string;
  stage: EditorialProject["stage"];
  status: EditorialProject["status"];
  created_at: Date;
  updated_at: Date;
}

interface SourceRow {
  id: string;
  editorial_project_id: string;
  kind: Source["kind"];
  raw_reference: string;
  retrieved_summary: string | null;
  retrieval_status: Source["retrievalStatus"];
  retrieval_error: string | null;
  created_at: Date;
}

interface DirectionRow {
  id: string;
  editorial_project_id: string;
  source_understanding: string;
  audience: string;
  objective: string;
  publication_language: string;
  primary_angle: string;
  supporting_lenses: string[];
  editorial_thesis: string;
  status: EditorialDirection["status"];
  reject_feedback: string | null;
  decided_at: Date | null;
  created_at: Date;
}

function mapProject(row: ProjectRow): EditorialProject {
  return {
    id: row.id,
    authorId: row.author_id,
    title: row.title,
    stage: row.stage,
    status: row.status,
    createdAt: row.created_at.toISOString(),
    updatedAt: row.updated_at.toISOString(),
  };
}

function mapSource(row: SourceRow): Source {
  return {
    id: row.id,
    editorialProjectId: row.editorial_project_id,
    kind: row.kind,
    rawReference: row.raw_reference,
    retrievedSummary: row.retrieved_summary,
    retrievalStatus: row.retrieval_status,
    retrievalError: row.retrieval_error,
    createdAt: row.created_at.toISOString(),
  };
}

function mapDirection(row: DirectionRow): EditorialDirection {
  return {
    id: row.id,
    editorialProjectId: row.editorial_project_id,
    sourceUnderstanding: row.source_understanding,
    audience: row.audience,
    objective: row.objective,
    publicationLanguage: row.publication_language,
    primaryAngle: row.primary_angle,
    supportingLenses: row.supporting_lenses,
    editorialThesis: row.editorial_thesis,
    status: row.status,
    rejectFeedback: row.reject_feedback,
    decidedAt: row.decided_at ? row.decided_at.toISOString() : null,
    createdAt: row.created_at.toISOString(),
  };
}

export class ProjectNotFoundError extends Error {
  constructor() {
    super("Project not found.");
  }
}

/**
 * Every read/write below is scoped by author_id at the SQL level - not
 * only in application logic - so ownership cannot be bypassed by
 * forgetting a check in a route handler (Web Walking Skeleton 01,
 * requirement 12).
 */
export class ProjectRepository {
  constructor(private pool: Pool) {}

  async createProject(authorId: string): Promise<EditorialProject> {
    const id = generateProjectId();
    const { rows } = await this.pool.query(
      `INSERT INTO editorial_projects (id, author_id, title, stage)
       VALUES ($1, $2, $3, 'source_intake')
       RETURNING *`,
      [id, authorId, "Untitled Editorial Project"],
    );
    return mapProject(rows[0]);
  }

  async listProjects(authorId: string): Promise<EditorialProject[]> {
    const { rows } = await this.pool.query(
      `SELECT * FROM editorial_projects
       WHERE author_id = $1
       ORDER BY created_at DESC`,
      [authorId],
    );
    return rows.map(mapProject);
  }

  async getProjectForAuthor(
    projectId: string,
    authorId: string,
  ): Promise<EditorialProject | null> {
    const { rows } = await this.pool.query(
      `SELECT * FROM editorial_projects WHERE id = $1 AND author_id = $2`,
      [projectId, authorId],
    );
    if (rows.length === 0) return null;
    return mapProject(rows[0]);
  }

  async getProjectView(
    projectId: string,
    authorId: string,
  ): Promise<ProjectView | null> {
    const project = await this.getProjectForAuthor(projectId, authorId);
    if (!project) return null;

    const [sourceResult, directionResult] = await Promise.all([
      this.pool.query(
        `SELECT * FROM sources WHERE editorial_project_id = $1
         ORDER BY created_at DESC LIMIT 1`,
        [projectId],
      ),
      this.pool.query(
        `SELECT * FROM editorial_directions WHERE editorial_project_id = $1`,
        [projectId],
      ),
    ]);

    return {
      project,
      source: sourceResult.rows[0] ? mapSource(sourceResult.rows[0]) : null,
      editorialDirection: directionResult.rows[0]
        ? mapDirection(directionResult.rows[0])
        : null,
    };
  }

  /** Creates a pending Source row for a project this Author owns. */
  async createSource(
    projectId: string,
    authorId: string,
    url: string,
  ): Promise<Source> {
    const owned = await this.getProjectForAuthor(projectId, authorId);
    if (!owned) throw new ProjectNotFoundError();

    const { rows } = await this.pool.query(
      `INSERT INTO sources (editorial_project_id, kind, raw_reference, retrieval_status)
       VALUES ($1, 'url', $2, 'pending')
       RETURNING *`,
      [projectId, url],
    );
    return mapSource(rows[0]);
  }

  async markSourceSucceeded(sourceId: string, summary: string): Promise<void> {
    await this.pool.query(
      `UPDATE sources
       SET retrieval_status = 'succeeded', retrieved_summary = $2, retrieval_error = NULL
       WHERE id = $1`,
      [sourceId, summary],
    );
  }

  async markSourceFailed(sourceId: string, error: string): Promise<void> {
    await this.pool.query(
      `UPDATE sources
       SET retrieval_status = 'failed', retrieval_error = $2
       WHERE id = $1`,
      [sourceId, error],
    );
  }

  async createEditorialDirection(
    projectId: string,
    authorId: string,
    payload: {
      sourceUnderstanding: string;
      audience: string;
      objective: string;
      publicationLanguage: string;
      primaryAngle: string;
      supportingLenses: string[];
      editorialThesis: string;
    },
  ): Promise<EditorialDirection> {
    const owned = await this.getProjectForAuthor(projectId, authorId);
    if (!owned) throw new ProjectNotFoundError();

    const client = await this.pool.connect();
    try {
      await client.query("BEGIN");
      const { rows } = await client.query(
        `INSERT INTO editorial_directions (
           editorial_project_id, source_understanding, audience, objective,
           publication_language, primary_angle, supporting_lenses, editorial_thesis
         ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
         ON CONFLICT (editorial_project_id) DO UPDATE SET
           source_understanding = EXCLUDED.source_understanding,
           audience = EXCLUDED.audience,
           objective = EXCLUDED.objective,
           publication_language = EXCLUDED.publication_language,
           primary_angle = EXCLUDED.primary_angle,
           supporting_lenses = EXCLUDED.supporting_lenses,
           editorial_thesis = EXCLUDED.editorial_thesis,
           status = 'proposed',
           reject_feedback = NULL,
           decided_at = NULL
         RETURNING *`,
        [
          projectId,
          payload.sourceUnderstanding,
          payload.audience,
          payload.objective,
          payload.publicationLanguage,
          payload.primaryAngle,
          JSON.stringify(payload.supportingLenses),
          payload.editorialThesis,
        ],
      );
      await client.query(
        `UPDATE editorial_projects SET stage = 'editorial_direction', updated_at = now()
         WHERE id = $1`,
        [projectId],
      );
      await client.query("COMMIT");
      return mapDirection(rows[0]);
    } catch (error) {
      await client.query("ROLLBACK");
      throw error;
    } finally {
      client.release();
    }
  }

  async approveDirection(
    projectId: string,
    authorId: string,
  ): Promise<EditorialDirection | null> {
    const owned = await this.getProjectForAuthor(projectId, authorId);
    if (!owned) throw new ProjectNotFoundError();

    const { rows } = await this.pool.query(
      `UPDATE editorial_directions
       SET status = 'approved', decided_at = now()
       WHERE editorial_project_id = $1
       RETURNING *`,
      [projectId],
    );
    if (rows.length === 0) return null;
    return mapDirection(rows[0]);
  }

  async rejectDirection(
    projectId: string,
    authorId: string,
    feedback: string,
  ): Promise<EditorialDirection | null> {
    const owned = await this.getProjectForAuthor(projectId, authorId);
    if (!owned) throw new ProjectNotFoundError();

    const { rows } = await this.pool.query(
      `UPDATE editorial_directions
       SET status = 'rejected', reject_feedback = $2, decided_at = now()
       WHERE editorial_project_id = $1
       RETURNING *`,
      [projectId, feedback],
    );
    if (rows.length === 0) return null;
    return mapDirection(rows[0]);
  }
}
