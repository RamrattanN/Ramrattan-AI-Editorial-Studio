import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { type EditorialProject, api, ApiError } from "../api.js";

export function Home() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<EditorialProject[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);

  const load = useCallback(async () => {
    try {
      const { projects } = await api.listProjects();
      setProjects(projects);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not load projects.");
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function handleCreate() {
    setCreating(true);
    setError(null);
    try {
      const { project } = await api.createProject();
      navigate(`/projects/${project.id}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not create project.");
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="page">
      {error && <div className="error-banner">{error}</div>}
      <div className="card">
        <button className="button-primary" onClick={handleCreate} disabled={creating}>
          {creating ? "Creating…" : "New Editorial Project"}
        </button>
      </div>

      <div className="card">
        <h2>Your Editorial Projects</h2>
        {projects === null && <p className="status-line">Loading…</p>}
        {projects !== null && projects.length === 0 && (
          <p className="status-line">
            No projects yet. Start one above to turn a URL into a
            publish-ready LinkedIn article.
          </p>
        )}
        {projects !== null && projects.length > 0 && (
          <ul className="project-list">
            {projects.map((project) => (
              <li key={project.id}>
                <a href={`/projects/${project.id}`}>{project.title}</a>
                <div className="status-line">
                  {project.id} · {project.stage.replace("_", " ")}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
