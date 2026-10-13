# RN BüroPilot – geplanter interner Bereich

Dieses Verzeichnis ist eine **öffentliche, rein statische Einstiegsvorschau** unter `/bueropilot/`. Es enthält absichtlich **keine Betriebsdaten**, keine Anmeldemaske und keine API-Schlüssel.

## Bestehende Homepage
- Die RN-Kundenseite bleibt unverändert.
- GitHub Actions veröffentlicht `main` automatisch auf GitHub Pages.
- Änderungen in `feature/bueropilot-zugang` werden noch **nicht live veröffentlicht**.
- Nach einem Merge wäre `https://rn-transporte.de/bueropilot/` öffentlich erreichbar. `noindex` verhindert **keinen** Zugriff.

## Zielarchitektur für echten Betrieb
1. Die bestehende GitHub-Pages-Seite bleibt öffentlich.
2. Die eigentliche BüroPilot-Anwendung läuft auf einem gesondert gehosteten HTTPS-Dienst, bevorzugt `app.rn-transporte.de`, alternativ nach einer Hosting-Umstellung unter `/bueropilot/`.
3. Der App-Server prüft Anmeldung, Rollen und Berechtigungen bei **jeder** Anfrage. Ein bloßer Login-Button im statischen HTML ist keine Sicherheit.
4. Eine serverseitige PostgreSQL-Datenbank speichert Aufträge, Kunden, Maschinen, Änderungen und Dokumentmetadaten; Backups und Löschkonzept sind erforderlich. SQLite in einer kurzlebigen Serverless-Funktion wäre hierfür nicht ausreichend.
5. Der KI-Agent darf Daten nur über begrenzte serverseitige Funktionen lesen oder ändern. Dispositionsänderungen und Preise sind auf dem Server zu validieren. Schreibzugriffe nur nach eindeutiger Auftragszuordnung und Bestätigung; alle Vorgänge werden protokolliert.
6. ElevenLabs-API-Schlüssel und KI-Schlüssel bleiben ausschließlich in Server-Umgebungsvariablen, niemals in GitHub Pages, JavaScript oder im Git-Repository.
7. Sprache benötigt HTTPS, Mikrofonberechtigung, sicheren Upload beziehungsweise Streaming und Fehlerbehandlung. Ein laufender Browser-Sprachdialog ist nicht in allen Browsern garantiert.
8. Bevor echte Betriebsdaten verwendet werden: Zugangsschutz, Datenschutz/AV-Verträge, Rollen, Protokollierung, Backups, Testfälle und gesicherte Betriebsfreigabe umsetzen.

## Nächste technische Arbeiten
- Aktuelle V21-Python-Testversion für eine passende Laufzeit bereitstellen oder in eine Vercel-kompatible API migrieren.
- Gehostete Benutzerverwaltung und Produktionsdatenbank auswählen.
- Autorisierte API-Routen für Disposition, Kunden, Angebote, Gespräch und ElevenLabs-Sprachausgabe bauen.
- Erst dann die interne App freischalten und von der RN-Unterseite auf den geschützten Dienst verlinken.

**Wichtig:** Die bisherige lokale V21-Demo darf nicht unverändert in GitHub Pages veröffentlicht werden. Das Repository ist öffentlich.
