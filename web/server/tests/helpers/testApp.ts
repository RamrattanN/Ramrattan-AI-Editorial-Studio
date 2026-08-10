import type { Express } from "express";
import type { Pool } from "pg";
import supertest, { type Agent } from "supertest";
import { createApp } from "../../src/app.js";
import type { EmailProvider } from "../../src/auth/emailProvider.js";

export class CapturingEmailProvider implements EmailProvider {
  public sent: { email: string; link: string }[] = [];

  async sendMagicLink(email: string, link: string): Promise<void> {
    this.sent.push({ email, link });
  }

  lastToken(): string {
    const last = this.sent[this.sent.length - 1];
    if (!last) throw new Error("No magic link was sent.");
    const url = new URL(last.link);
    const token = url.searchParams.get("token");
    if (!token) throw new Error("Magic link had no token.");
    return token;
  }
}

export function buildTestApp(pool: Pool): {
  app: Express;
  emailProvider: CapturingEmailProvider;
} {
  process.env.SESSION_SECRET = "test-session-secret-not-for-production";
  const emailProvider = new CapturingEmailProvider();
  const app = createApp({
    pool,
    emailProvider,
    clientOrigin: "http://localhost:5173",
  });
  return { app, emailProvider };
}

/** Completes a real magic-link sign-in and returns a session-cookied agent. */
export async function signInAgent(
  app: Express,
  emailProvider: CapturingEmailProvider,
  email: string,
): Promise<Agent> {
  const agent = supertest.agent(app);
  await agent.post("/api/auth/request-link").send({ email });
  const token = emailProvider.lastToken();
  await agent.post("/api/auth/callback").send({ token });
  return agent;
}
