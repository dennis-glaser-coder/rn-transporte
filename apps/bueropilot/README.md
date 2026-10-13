# RN BüroPilot Web-App Pilot

Not production-ready. Existing RN customer website stays unchanged.

## Current features
- Next.js application with Supabase email magic link authentication.
- Every protected API request checks active Supabase user AND rn_staff.enabled.
- Tenant-scoped read-only job data from Supabase Postgres with row level security.
- Optional OpenAI-compatible AI chat over HTTPS. No AI tools, no writes.
- Optional ElevenLabs MP3 text-to-speech with server-only key; off by default.
- No speech recognition, always-on microphone, job editing, backups or invoicing yet.

## Local start
1. Open terminal in apps/bueropilot.
2. Run npm install and npm run dev.
3. Copy .env.example to .env.local and fill in settings.
4. Set up a separate Supabase project, run supabase/schema.sql in the SQL editor.
5. Configure Supabase Auth site URL and redirect URLs for localhost and the eventual app domain.
6. Assign approved users in rn_staff with enabled true and correct org_id using authorized SQL editor.
7. AI settings: RN_AI_CHAT_URL must be a complete HTTPS OpenAI-compatible chat completions URL, plus RN_AI_API_KEY and RN_AI_MODEL.
8. ElevenLabs: supply ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID, enable RN_VOICE_ENABLED only after checking account quota and data handling.

## Vercel
- Create a separate Vercel project linked to this same GitHub repository, root directory apps/bueropilot.
- Put secrets only in Vercel Environment Variables, never in a Git commit or NEXT_PUBLIC setting.
- Use a protected preview until login, RLS and authorization are tested.
- Bind app.rn-transporte.de only after Vercel project access and DNS ownership are verified.
- Current GitHub Pages site stays at rn-transporte.de, public /bueropilot page can later link to secured app.

## Do not use with real business data yet
- Supabase row policies need two-user / cross-org security tests before real use.
- API abuse prevention, audit logs, domain protections, backups, retention and GDPR review are pending.
- Chat is conversational only and cannot access or change bookings; never claim an action was saved.
- ElevenLabs will receive the requested speech text if turned on.
- SQLite-based V21 Windows demo is not suitable as a persistent serverless production database.
