export interface Author {
  id: string;
  email: string;
  createdAt: string;
}

export type ProjectStage =
  | "source_intake"
  | "editorial_direction"
  | "editorial_plan"
  | "draft";

export interface EditorialProject {
  id: string;
  authorId: string;
  title: string;
  stage: ProjectStage;
  status: "active";
  createdAt: string;
  updatedAt: string;
}

export type SourceRetrievalStatus = "pending" | "succeeded" | "failed";

export interface Source {
  id: string;
  editorialProjectId: string;
  kind: "url";
  rawReference: string;
  retrievedSummary: string | null;
  retrievalStatus: SourceRetrievalStatus;
  retrievalError: string | null;
  createdAt: string;
}

export type EditorialDirectionStatus = "proposed" | "approved" | "rejected";

export interface EditorialDirection {
  id: string;
  editorialProjectId: string;
  sourceUnderstanding: string;
  audience: string;
  objective: string;
  publicationLanguage: string;
  primaryAngle: string;
  supportingLenses: string[];
  editorialThesis: string;
  status: EditorialDirectionStatus;
  rejectFeedback: string | null;
  decidedAt: string | null;
  createdAt: string;
}

export type EditorialPlanStatus = "proposed" | "approved" | "revision_requested";

export interface EditorialPlan {
  id: string;
  editorialProjectId: string;
  headline: string;
  hook: string;
  keyInsights: string[];
  practicalTakeaway: string;
  ctaDirection: string;
  status: EditorialPlanStatus;
  decidedAt: string | null;
  createdAt: string;
}

export interface SourceAttribution {
  citation: string;
}

export interface Article {
  id: string;
  editorialProjectId: string;
  headline: string;
  hook: string;
  keyInsights: string[];
  practicalTakeaway: string;
  cta: string;
  articleMarkdown: string;
  sourceAttributions: SourceAttribution[];
  createdAt: string;
}

export interface ProjectView {
  project: EditorialProject;
  source: Source | null;
  editorialDirection: EditorialDirection | null;
  editorialPlan: EditorialPlan | null;
  article: Article | null;
}
