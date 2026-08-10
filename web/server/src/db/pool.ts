import { Pool } from "pg";

let pool: Pool | undefined;

/**
 * Single shared connection pool. DATABASE_URL is read once at first use so
 * tests can override it via process.env before the pool is created.
 */
export function getPool(): Pool {
  if (!pool) {
    const connectionString = process.env.DATABASE_URL;
    if (!connectionString) {
      throw new Error("DATABASE_URL is required but was not set.");
    }
    pool = new Pool({ connectionString });
  }
  return pool;
}

export async function closePool(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = undefined;
  }
}
