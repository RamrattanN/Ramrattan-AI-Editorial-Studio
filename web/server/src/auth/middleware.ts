import type { NextFunction, Request, Response } from "express";

/**
 * Rejects any request without a valid server-side session. Unauthenticated
 * Authors must never reach a project route (Web Walking Skeleton 01,
 * requirement 1 and 12).
 */
export function requireAuth(
  req: Request,
  res: Response,
  next: NextFunction,
): void {
  if (!req.session?.authorId) {
    res.status(401).json({ error: "Authentication required." });
    return;
  }
  next();
}

/**
 * Reads the authenticated Author id from the session. Only valid after
 * requireAuth has already run for the current request - route handlers
 * mounted behind requireAuth may call this directly.
 */
export function getAuthorId(req: Request): string {
  const authorId = req.session?.authorId;
  if (!authorId) {
    throw new Error("getAuthorId called on a request without a session.");
  }
  return authorId;
}
