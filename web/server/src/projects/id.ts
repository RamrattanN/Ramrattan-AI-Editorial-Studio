import { randomBytes } from "node:crypto";

/**
 * Generates a project id in the REP-[A-F0-9]{8} shape already established
 * by studio/portable_editorial_project.py, so the web product and the
 * Portable Editorial Project file format share one identity scheme
 * (per docs/product/version2/Web_Product_Foundation_v1.md Section 2/6).
 */
export function generateProjectId(): string {
  const hex = randomBytes(4).toString("hex").toUpperCase();
  return `REP-${hex}`;
}

const PROJECT_ID_RE = /^REP-[A-F0-9]{8}$/;

export function isValidProjectId(id: string): boolean {
  return PROJECT_ID_RE.test(id);
}
