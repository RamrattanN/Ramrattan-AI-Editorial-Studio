import "express-async-errors";
import cors from "cors";
import express, { type Express, type NextFunction, type Request, type Response } from "express";
import type { Pool } from "pg";
import { createSessionMiddleware } from "./auth/session.js";
import { createAuthRouter } from "./auth/routes.js";
import type { EmailProvider } from "./auth/emailProvider.js";
import { createProjectsRouter } from "./projects/routes.js";
import { ProjectRepository } from "./projects/repository.js";

export interface AppDependencies {
  pool: Pool;
  emailProvider: EmailProvider;
  clientOrigin: string;
}

/**
 * Builds the Express app from injected dependencies so tests can supply a
 * real test-database pool with a mocked EmailProvider, and production can
 * supply real dependencies - without duplicating route wiring.
 */
export function createApp({ pool, emailProvider, clientOrigin }: AppDependencies): Express {
  const app = express();

  app.set("trust proxy", 1);
  app.use(cors({ origin: clientOrigin, credentials: true }));
  app.use(express.json({ limit: "100kb" }));
  app.use(createSessionMiddleware(pool));

  app.get("/api/health", (_req, res) => {
    res.json({ status: "ok" });
  });

  app.use("/api/auth", createAuthRouter(pool, emailProvider, clientOrigin));

  const repository = new ProjectRepository(pool);
  app.use("/api/projects", createProjectsRouter(repository));

  // Centralized error handler: never leak secrets or stack traces to the
  // browser (Web Walking Skeleton 01 security minimum).
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  app.use((err: unknown, _req: Request, res: Response, _next: NextFunction) => {
    console.error(err);
    res.status(500).json({ error: "An unexpected error occurred." });
  });

  return app;
}
