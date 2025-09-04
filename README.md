# Plant Based University (PBU) — Starter Repo

This is a minimal scaffold to deploy PBU v1.0:
- **Vercel**: Next.js Student Portal + public site (`apps/web`)
- **Render**: FastAPI API (`apps/api`) and RQ Worker (`apps/worker`)
- **Supabase**: Postgres + Auth + Storage
- **Twilio**: SMS webhook for Garvey
- **Printful**: Mockup generator (varsity jacket overlay)

## Quick Start
1. Create a GitHub repo and push this folder.
2. Configure Supabase project (URL/keys), Twilio number, and Printful API key.
3. In Render: New → Blueprint → select `infra/render.yaml` (adds web, api, worker, db, redis).
4. Add env vars from `.env.example` to Render services.
5. Deploy. Then set Twilio Messaging webhook to: `https://<pbu-api-url>/webhooks/twilio/sms`.

## Folders
- `apps/web`  – Next.js app (App Router)
- `apps/api`  – FastAPI service
- `apps/worker` – RQ background worker
- `infra`     – Render blueprint & local docker-compose
- `shared`    – Common utilities (S3, Printful client stubs)
