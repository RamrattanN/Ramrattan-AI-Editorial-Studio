import { Pool } from "pg";
import { runMigrations } from "../../src/db/migrate.js";

const TEST_DATABASE_URL =
  process.env.TEST_DATABASE_URL ?? "postgresql://localhost:5432/ramrattan_web_test";

let pool: Pool | undefined;

/** Real local Postgres, not a mock - see Web Walking Skeleton 01 testing scope. */
export async function setupTestDb(): Promise<Pool> {
  process.env.DATABASE_URL = TEST_DATABASE_URL;
  if (!pool) {
    pool = new Pool({ connectionString: TEST_DATABASE_URL });
  }
  await runMigrations();
  return pool;
}

const APP_TABLES = [
  "editorial_directions",
  "sources",
  "editorial_projects",
  "login_tokens",
  "session",
  "authors",
];

export async function truncateAll(db: Pool): Promise<void> {
  for (const table of APP_TABLES) {
    await db.query(`DELETE FROM ${table}`).catch(() => undefined);
  }
}

export async function closeTestDb(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = undefined;
  }
}
