# MekoTools — Auslieferung von Wick Editor (Bau-Zweig des Projekts)
#
# Hier wird NICHTS selbst uebersetzt. Genommen wird genau der Bau, den das
# Projekt Wicklets/wick-editor veroeffentlicht: der Zweig `gh-pages`
# (GPL-3.0). Der Workflow holt ihn auf einen festgenagelten Commit und legt ihn
# als `seite/` neben diese Datei.
#
# Eine einzige Aenderung gegenueber dem amtlichen Bau: in `index.html` wird die
# Zeile mit `plausible.io` entfernt. Das ist die Analyse-Datei des Projekts, die
# sonst bei jedem Aufruf einen fremden Server kontaktiert. MekoTools-Werkzeuge
# rufen im Betrieb nichts Fremdes ab.
FROM nginx:1.27-alpine

LABEL org.opencontainers.image.title="Wick Editor (MekoTools-Auslieferung)"
LABEL org.opencontainers.image.description="Statische Auslieferung des amtlichen Baus (Zweig gh-pages), Fremdaufruf entfernt."
LABEL org.opencontainers.image.source="https://github.com/Wicklets/wick-editor"
LABEL org.opencontainers.image.licenses="GPL-3.0"

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY seite/ /usr/share/nginx/html/

# Der Bau muss wirklich angekommen sein, sonst soll das Abbild nicht entstehen.
RUN test -f /usr/share/nginx/html/index.html \
 && test -d /usr/share/nginx/html/static \
 && ! grep -q "plausible" /usr/share/nginx/html/index.html
