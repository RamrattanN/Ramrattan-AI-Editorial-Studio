import { createHash, randomBytes } from "node:crypto";
import type { Pool } from "pg";
import type { EmailProvider } from "./emailProvider.js";

const TOKEN_TTL_MS = 15 * 60 * 1000;

function hashToken(token: string): string {
  return createHash("sha256").update(token).digest("hex");
}

/**
 * Creates a one-time login token for the given email and sends it via the
 * configured EmailProvider. Only the token's hash is persisted; the raw
 * token exists solely in the link that is sent/logged.
 */
export async function requestMagicLink(
  pool: Pool,
  emailProvider: EmailProvider,
  email: string,
  clientOrigin: string,
): Promise<void> {
  const normalizedEmail = email.trim().toLowerCase();
  const token = randomBytes(32).toString("hex");
  const tokenHash = hashToken(token);
  const expiresAt = new Date(Date.now() + TOKEN_TTL_MS);

  await pool.query(
    `INSERT INTO login_tokens (email, token_hash, expires_at)
     VALUES ($1, $2, $3)`,
    [normalizedEmail, tokenHash, expiresAt],
  );

  const link = `${clientOrigin}/auth/callback?token=${token}`;
  await emailProvider.sendMagicLink(normalizedEmail, link);
}

export type MagicLinkOutcome =
  | { ok: true; authorId: string; email: string }
  | { ok: false; reason: "invalid_or_expired" };

/**
 * Verifies a magic-link token, marks it used, and returns (creating if
 * necessary) the Author it authenticates. Tokens are single-use and
 * time-limited; an already-used or expired token fails closed.
 */
export async function verifyMagicLink(
  pool: Pool,
  token: string,
): Promise<MagicLinkOutcome> {
  const tokenHash = hashToken(token);
  const client = await pool.connect();
  try {
    await client.query("BEGIN");

    const { rows } = await client.query(
      `SELECT id, email, expires_at, used_at
       FROM login_tokens
       WHERE token_hash = $1
       FOR UPDATE`,
      [tokenHash],
    );

    if (rows.length === 0) {
      await client.query("ROLLBACK");
      return { ok: false, reason: "invalid_or_expired" };
    }

    const row = rows[0];
    const expired = new Date(row.expires_at).getTime() < Date.now();
    if (row.used_at || expired) {
      await client.query("ROLLBACK");
      return { ok: false, reason: "invalid_or_expired" };
    }

    await client.query(
      "UPDATE login_tokens SET used_at = now() WHERE id = $1",
      [row.id],
    );

    const authorResult = await client.query(
      `INSERT INTO authors (email)
       VALUES ($1)
       ON CONFLICT (email) DO UPDATE SET email = EXCLUDED.email
       RETURNING id, email`,
      [row.email],
    );

    await client.query("COMMIT");
    return {
      ok: true,
      authorId: authorResult.rows[0].id,
      email: authorResult.rows[0].email,
    };
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    client.release();
  }
}
