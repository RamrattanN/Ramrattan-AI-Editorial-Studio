import "dotenv/config";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createApp } from "./app.js";
import { createEmailProvider } from "./auth/emailProvider.js";
import { runMigrations } from "./db/migrate.js";
import { getPool } from "./db/pool.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
// web/server/dist/index.js -> web/client/dist. Only exists in the hosted
// single-service build (render.yaml); absent in local dev, where the Vite
// dev server serves the client separately.
const CLIENT_DIST_DIR = join(__dirname, "../../client/dist");

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
    clientDistDir: CLIENT_DIST_DIR,
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
