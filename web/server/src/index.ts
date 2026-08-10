import "dotenv/config";
import { createApp } from "./app.js";
import { createEmailProvider } from "./auth/emailProvider.js";
import { runMigrations } from "./db/migrate.js";
import { getPool } from "./db/pool.js";

async function main() {
  const pool = getPool();
  const applied = await runMigrations();
  if (applied.length > 0) {
    console.log(`Applied migrations: ${applied.join(", ")}`);
  }

  const clientOrigin = process.env.CLIENT_ORIGIN ?? "http://localhost:5173";
  const app = createApp({
    pool,
    emailProvider: createEmailProvider(),
    clientOrigin,
  });

  const port = Number(process.env.PORT ?? "4000");
  app.listen(port, () => {
    console.log(`Ramrattan web server listening on http://localhost:${port}`);
  });
}

main().catch((error) => {
  console.error("Failed to start server:", error);
  process.exit(1);
});
