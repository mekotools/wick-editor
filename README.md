# wick-editor — MekoTools-Auslieferung

Bau- und Auslieferungs-Repository für **Wick Editor** im
[MekoTools-Katalog](https://mekotools.de). Der Katalogeintrag selbst (Metadaten,
Anleitung, Didaktik, Unterrichtsentwurf) liegt unter
`git.n0ne.de/mekotools/mekotools-wick-editor`.

Wick Editor ist ein freies Werkzeug, mit dem sich Animationen und kleine Spiele
im Browser bauen lassen (GPL-3.0). Quelltext:
[Wicklets/wick-editor](https://github.com/Wicklets/wick-editor),
Projektseite: [wickeditor.com](https://www.wickeditor.com/).

## Es wird nichts selbst übersetzt

Geholt wird der amtliche Bau des Projekts — der Zweig `gh-pages` des
Quelltext-Repos, den die Entwickler selbst veröffentlichen — auf einen
festgenagelten Commit. Der Ablauf `.github/workflows/bau.yml` macht daraus ein
Abbild:

1. Zweig `gh-pages` auf den angegebenen Commit holen.
2. **Einziger Eingriff:** die Zeile mit `plausible.io` aus `index.html`
   entfernen. Das ist die Analyse-Datei des Projekts; MekoTools-Werkzeuge rufen
   im Betrieb keinen fremden Server auf.
3. `docker build` (nginx:1.27-alpine) und Ablegen nach
   `ghcr.io/mekotools/wick-editor`.

Der Bau prüft sich selbst: fehlt `index.html` oder `static/`, oder steckt die
Analyse-Zeile noch in der Datei, entsteht kein Abbild.

## Betrieb

Ausgeliefert wird über nginx auf `https://wick.mekotools.de`. Es gibt keinen
Anwendungsteil auf einem Server: Projekte liegen im Speicher des Browsers bzw.
werden als Datei heruntergeladen. Deshalb genügt ein statischer Dienst ohne
Datenbank und ohne Anmeldung.
