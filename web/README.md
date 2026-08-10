# Ramrattan AI Editorial Studio — Web (Walking Skeleton 01)

The first browser-usable vertical slice of the Editorial Studio: Sign In →
Create Editorial Project → Paste URL → server-side source retrieval →
server-side OpenAI request → Consolidated Editorial Direction → native
Approve/Reject → persisted decision → refresh-safe rehydration.

This document covers only what's needed to run this app locally. Product
and architecture decisions live in
[`docs/product/version2/Web_Product_Foundation_v1.md`](../docs/product/version2/Web_Product_Foundation_v1.md)
— do not duplicate them here.

## Architecture

- **`server/`** — Node.js/TypeScript, Express 4, REST API. Sessions are
  server-side (`express-session` + `connect-pg-simple`), stored in
  Postgres. Raw SQL migrations, no ORM.
- **`client/`** — React 18 + Vite + React Router, plain CSS (no UI
  framework). Talks to the server only via `fetch` (`credentials:
  "include"`).
- **Database** — PostgreSQL. Tables: `authors`, `magic_link_tokens`,
  `editorial_projects`, `sources`, `editorial_directions`, plus the
  `connect-pg-simple` session table.
- **Auth** — email magic link only (no passwords). A single-use, hashed,
  15-minute-TTL token is emailed via a pluggable `EmailProvider`. Set
  `EMAIL_PROVIDER=console` for local development (the link is written to
  the server log instead of sent) or `EMAIL_PROVIDER=smtp` with `SMTP_*`
  for real delivery.
- **OpenAI** — called server-side only, via the `openai` SDK, using
  Structured Outputs against a bounded JSON schema. Never called from, or
  exposed to, the browser.

## Prerequisites

- Node.js 20+
- PostgreSQL running locally, with a database created for this app:
  ```
  createdb ramrattan_web_dev
  ```

## Setup

```
cd web
npm install
cp .env.example server/.env
```

Edit `web/server/.env`:

- `DATABASE_URL` — point at your local Postgres (`ramrattan_web_dev`).
- `SESSION_SECRET` — generate with
  `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`.
- `EMAIL_PROVIDER=console` for local development.
- `OPENAI_API_KEY` — required for the real Editorial Direction step; leave
  empty and the app runs fully except for that one step, which fails with
  an explicit, honest server error (never a fabricated result).

Create `web/client/.env`:

```
VITE_API_BASE_URL=http://localhost:4000
```

Run migrations:

```
npm run migrate
```

## Running locally

In two terminals:

```
npm run dev:server   # http://localhost:4000
npm run dev:client   # http://localhost:5173
```

Open `http://localhost:5173`. Sign in with any email address; with
`EMAIL_PROVIDER=console` the magic link is printed to the `dev:server`
terminal log — copy it into the browser to complete sign-in.

## Tests

```
npm test
```

Server tests run against a real local Postgres database (see
`server/tests/helpers/testDb.ts`); `DATABASE_URL` (or its test-specific
override) must point at a reachable Postgres instance. OpenAI and email
delivery are mocked in automated tests, per the project's testing
standard — the OpenAI integration itself is exercised for real only in
manual/development acceptance.

Other checks:

```
npm run typecheck
npm run lint
npm run build
```

## Deploying to a development environment

`npm run build` produces `server/dist` (Node.js server, migrations
copied alongside) and `client/dist` (static SPA build). Deployment beyond
a local machine requires a chosen hosting platform and account, which is
outside what this repository can provision on its own — see the delivery
report for the exact external dependency.

## Deferred scope

Editorial Plan generation, article drafting, Editorial Audit, Hero Visual
generation, LinkedIn publishing, Reader Engagement, and all
billing/org/analytics features are intentionally out of scope for this
walking skeleton.
