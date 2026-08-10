import ConnectPgSimple from "connect-pg-simple";
import session, { type SessionOptions } from "express-session";
import type { Pool } from "pg";

declare module "express-session" {
  interface SessionData {
    authorId?: string;
    email?: string;
  }
}

/**
 * Server-side sessions backed by Postgres (connect-pg-simple). The session
 * id is the only thing stored in the browser cookie, signed with
 * SESSION_SECRET; all session state lives server-side, matching the
 * security minimum in Web_Product_Foundation_v1.md Section 11.
 */
export function createSessionMiddleware(pool: Pool) {
  const secret = process.env.SESSION_SECRET;
  if (!secret) {
    throw new Error("SESSION_SECRET is required but was not set.");
  }

  const PgSession = ConnectPgSimple(session);
  const options: SessionOptions = {
    store: new PgSession({ pool, createTableIfMissing: true }),
    secret,
    name: "ramrattan.sid",
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production",
      maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
    },
  };

  return session(options);
}
