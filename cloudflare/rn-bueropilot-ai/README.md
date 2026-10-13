# Cloudflare Workers AI – Willi ohne laufenden PC

Kosten: **Workers Free**. Modell \`@cf/zai-org/glm-4.7-flash\`, nur im Free-Tarif.
Im Freikontingent stehen derzeit 10.000 Neurons/Tag bereit. Bei Limit wird ein Fehler gemeldet; **niemals zu Workers Paid wechseln**.

## Einrichtung über Cloudflare Dashboard (keine ZIP, kein Windows-Server)

1. In Cloudflare anmelden: https://dash.cloudflare.com/
2. **Workers & Pages → Create application → Create Worker**. Name: \`rn-bueropilot-ai\`. Im kostenlosen Tarif bleiben.
3. **Edit Code**: Inhalt aus [worker.js](./worker.js) einsetzen und **Deploy**.
4. **Settings → Bindings → Add binding → Workers AI** und den Namen \`AI\` verwenden. Speichern / Deploy.
5. Auf der bereitgestellten \`https://rn-bueropilot-ai.<dein-subdomain>.workers.dev/health\` den Status prüfen. Bei erfolgreicher Bindung sollte \`"ai":true\` stehen.
6. Die genaue Worker-Adresse (keine API-Schlüssel!) im BüroPilot-Client unter \`bueropilot/config.js\` als \`cloudflareWorkerUrl\` hinterlegen. Dann erst Live-Veröffentlichung prüfen.
7. Login unter Supabase einrichten und Staff-Whitelist freigeben. **Ohne einen gültigen RN-Mitarbeiter-JWT antwortet Worker /chat mit 403**.
8. End-to-End-Test durchführen, kein produktiver Einsatz vor dem Test.

Der öffentliche Supabase-Publishable-Key im Worker ist **kein Geheimnis**. Es ist kein service_role-Key integriert. \`GET /auth/v1/user\` validiert das echte Login und \`rn_staff\` ist durch RLS geschützt.

Das Modell hat **noch keine Schreibrechte oder Auftragsdaten**. Der Worker kann nicht buchen; Dialoge sind real, Buchungen werden nicht vorgetäuscht. Die bestehende RN-Webseite, die Kunden und der kostenlose Tarif bleiben unberührt.

Es gibt keine dauerhaft kostenlosen unbegrenzten AI-Anfragen. Cloudflare Free und Supabase Free sind abhängig von deren Nutzungsgrenzen.
