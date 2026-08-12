// Empty by default: same-origin relative requests, correct for the hosted
// single-service deployment (client and API share one origin). Local dev
// sets VITE_API_BASE_URL explicitly (see .env.example) because the Vite
// dev server and the API run on different ports.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

export interface Author {
  id: string;
  email: string;
}

export type ProjectStage =
  | "source_intake"
  | "editorial_direction"
  | "editorial_plan"
  | "draft";

export interface EditorialProject {
  id: string;
  title: string;
  stage: ProjectStage;
  status: "active";
  createdAt: string;
  updatedAt: string;
}

export type EditorialDirectionStatus = "proposed" | "approved" | "rejected";

export interface EditorialDirection {
  id: string;
  sourceUnderstanding: string;
  audience: string;
  objective: string;
  publicationLanguage: string;
  primaryAngle: string;
  supportingLenses: string[];
  editorialThesis: string;
  status: EditorialDirectionStatus;
  rejectFeedback: string | null;
}

export interface Source {
  id: string;
  rawReference: string;
  retrievalStatus: "pending" | "succeeded" | "failed";
  retrievalError: string | null;
}

export type EditorialPlanStatus = "proposed" | "approved" | "revision_requested";

export interface EditorialPlan {
  id: string;
  headline: string;
  hook: string;
  keyInsights: string[];
  practicalTakeaway: string;
  ctaDirection: string;
  status: EditorialPlanStatus;
}

export interface SourceAttribution {
  citation: string;
}

export interface Article {
  id: string;
  headline: string;
  hook: string;
  keyInsights: string[];
  practicalTakeaway: string;
  cta: string;
  articleMarkdown: string;
  sourceAttributions: SourceAttribution[];
}

export interface ProjectView {
  project: EditorialProject;
  source: Source | null;
  editorialDirection: EditorialDirection | null;
  editorialPlan: EditorialPlan | null;
  article: Article | null;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    let message = `Request failed (${response.status}).`;
    try {
      const body = await response.json();
      if (body?.error) message = body.error;
    } catch {
      // response had no JSON body - keep the generic message.
    }
    throw new ApiError(message, response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export const api = {
  requestMagicLink: (email: string) =>
    request<{ status: string }>("/api/auth/request-link", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),

  completeMagicLink: (token: string) =>
    request<Author>("/api/auth/callback", {
      method: "POST",
      body: JSON.stringify({ token }),
    }),

  me: () => request<Author>("/api/auth/me"),

  logout: () => request<void>("/api/auth/logout", { method: "POST" }),

  listProjects: () => request<{ projects: EditorialProject[] }>("/api/projects"),

  createProject: () =>
    request<{ project: EditorialProject }>("/api/projects", { method: "POST" }),

  getProject: (id: string) => request<ProjectView>(`/api/projects/${id}`),

  submitSource: (id: string, url: string) =>
    request<{ editorialDirection: EditorialDirection }>(`/api/projects/${id}/source`, {
      method: "POST",
      body: JSON.stringify({ url }),
    }),

  approveDirection: (id: string) =>
    request<{
      editorialDirection: EditorialDirection;
      project: EditorialProject;
      editorialPlan: EditorialPlan | null;
      planError?: string;
    }>(`/api/projects/${id}/direction/approve`, { method: "POST" }),

  rejectDirection: (id: string, feedback: string) =>
    request<{ editorialDirection: EditorialDirection }>(
      `/api/projects/${id}/direction/reject`,
      { method: "POST", body: JSON.stringify({ feedback }) },
    ),

  approvePlan: (id: string) =>
    request<{
      editorialPlan: EditorialPlan;
      article: Article | null;
      project?: EditorialProject;
      draftError?: string;
    }>(`/api/projects/${id}/plan/approve`, { method: "POST" }),

  revisePlan: (id: string) =>
    request<{ editorialPlan: EditorialPlan; planError?: string }>(
      `/api/projects/${id}/plan/revise`,
      { method: "POST" },
    ),
};
