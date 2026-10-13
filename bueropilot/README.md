# RN BüroPilot mit GitHub Pages + Supabase

Entwicklungszweig: feature/bueropilot-zugang. Die RN Kundenhomepage (main) bleibt unverändert.

## Stand
- bueropilot/index.html, app.css, app.js sind eine eigenständige statische, responsive Web-App für GitHub Pages.
- Die öffentliche Datei bueropilot/config.js enthält absichtlich leere Werte. Hier darf später nur die Supabase-Projekt-URL und der öffentliche Publishable/Anon-Key stehen.
- supabase/migrations/20261013_rn_pilot.sql enthält Tabellen und Row Level Security für freigegebene Mitarbeiter.
- supabase/functions/{rn-auth-check,rn-jobs-list,rn-willi-chat,rn-willi-voice}/index.ts enthalten vier serverseitige Edge Functions.
- Es gibt ausdrücklich **keine Schreibfunktion** für Aufträge.
- Login wird erst nach Projektkonfiguration aktiv. Nicht autorisierte Besucher erhalten keine echten Daten.

## Sobald Supabase verbunden ist
1. Ein eigenes RN-Projekt wählen oder erstellen (vorher Mandant und Datenhaltung prüfen).
2. Migration im SQL Editor anwenden; RLS und Rechte mit verschiedenen Testbenutzern kontrollieren.
3. Auth E-Mail Magic Link erlauben; Site URL und Redirect URLs wie https://rn-transporte.de/bueropilot/ hinterlegen.
4. Einladungen/Freigaben organisieren: in rn_staff muss für die entsprechende Auth-User-ID eine gültige org_id, role und enabled=true stehen. Keine öffentlichen Selbstregistrierungen als Mitarbeiter.
5. Edge Functions deployen. Die Auth-Prüfung verlangt ein echtes Nutzer-JWT und eine aktive rn_staff-Zuordnung. Supabase Function JWT Verification einschalten.
6. Supabase Function Secret RN_APP_ORIGIN=https://rn-transporte.de setzen. RN_AI_CHAT_URL, RN_AI_API_KEY, RN_AI_MODEL serverseitig konfigurieren, erst nach Kosten- und Datenschutzprüfung.
7. ElevenLabs: ELEVENLABS_API_KEY und ELEVENLABS_VOICE_ID als Supabase-Secrets eintragen. RN_VOICE_ENABLED bleibt zunächst false. Kein Schlüssel im GitHub Repo und kein Schlüssel im Browser.
8. In bueropilot/config.js öffentliche URL und Publishable/Anon Key eintragen; niemals service_role, KI-Key oder ElevenLabs-Key.
9. App- und API-Antworten mit verschiedenen Accounts und fremden org_ids testen, erst danach die Website-Unterseite veröffentlichen.

## Sicherheit / Funktionsgrenzen
- **Noch nicht live**: Branch ist nur ein PR-Entwurf; main nicht verändert.
- GitHub Pages macht alle veröffentlichten HTML/JS-Dateien öffentlich. Nur RLS und serverseitige Auth verhindern Datenzugriffe, nicht robots.txt/noindex oder versteckte Buttons.
- KI-Chat ist derzeit nur eine Frage-Antwort-Schnittstelle, keine echte Auftragsverwaltung oder Terminänderungslogik.
- SpeechRecognition im Browser kann blockiert sein und unterstützt nicht alle Browser; läuft nicht unbegrenzt stabil.
- Über ElevenLabs werden Textantworten an einen externen Dienst gesendet. Rechtliche Prüfung und AV-Verträge erforderlich.
- **Vor Produktionsbetrieb fehlen:** strikte KI-Dienst-URL-Allowlist statt frei konfigurierbarer Endpoint-URL, Missbrauchsschutz und Quoten, serverseitige Gesprächskontextverwaltung, belastbare Validierung und Buchungsbestätigungen, vollständige Audit-Logs, sichere Datenbank-Backups und Restore-Test, Rollenverwaltung, Datenschutzprüfung, Betriebsüberwachung, echte Geräte- und Mikrofontests.
- Supabase Edge Functions und gesicherter Datenbankzugriff sind erst nach Verbindung des Kontos und Deploy testbar. Noch keine Live-KI/ElevenLabs-Prüfung.

## Alte Next.js-Variante
apps/bueropilot ist ein früher Vercel-Ansatz und wird hier nicht verwendet. Für GitHub Pages gilt nur bueropilot/ plus supabase/.
