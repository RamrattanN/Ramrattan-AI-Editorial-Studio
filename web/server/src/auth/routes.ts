import { Router } from "express";
import type { Pool } from "pg";
import { z } from "zod";
import type { EmailProvider } from "./emailProvider.js";
import { requestMagicLink, verifyMagicLink } from "./magicLink.js";

const requestLinkSchema = z.object({
  email: z.string().trim().email(),
});

const callbackSchema = z.object({
  token: z.string().min(1),
});

export function createAuthRouter(
  pool: Pool,
  emailProvider: EmailProvider,
  clientOrigin: string,
): Router {
  const router = Router();

  router.post("/request-link", async (req, res) => {
    const parsed = requestLinkSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: "A valid email address is required." });
      return;
    }

    await requestMagicLink(pool, emailProvider, parsed.data.email, clientOrigin);

    // Deliberately do not reveal whether the email is new or returning.
    res.status(200).json({ status: "sent" });
  });

  router.post("/callback", async (req, res) => {
    const parsed = callbackSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: "A token is required." });
      return;
    }

    const outcome = await verifyMagicLink(pool, parsed.data.token);
    if (!outcome.ok) {
      res.status(401).json({ error: "This sign-in link is invalid or has expired." });
      return;
    }

    req.session.authorId = outcome.authorId;
    req.session.email = outcome.email;
    res.status(200).json({ id: outcome.authorId, email: outcome.email });
  });

  router.post("/logout", (req, res) => {
    req.session.destroy((err) => {
      if (err) {
        res.status(500).json({ error: "Could not sign out." });
        return;
      }
      res.clearCookie("ramrattan.sid");
      res.status(204).end();
    });
  });

  router.get("/me", (req, res) => {
    if (!req.session?.authorId) {
      res.status(401).json({ error: "Authentication required." });
      return;
    }
    res.json({ id: req.session.authorId, email: req.session.email });
  });

  return router;
}
