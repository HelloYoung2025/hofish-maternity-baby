# HOFISH Maternity & Baby

[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md)

Ein mehrsprachiges Nachschlagewerk zur öffentlichen Website von HOFISH Maternity & Baby. Die Gliederung folgt der Website mit Startseite, Kollektionen, Produktseiten, Blogbeiträgen sowie Seiten zur Marke, zum Kundenservice und zu den Geschäftsbedingungen. Jeder Eintrag enthält eine eigenständig formulierte Beschreibung und einen Link zur Quelle. Die Erfassung basiert auf 59 URLs der [offiziellen XML-Sitemap](https://www.hofish.com/sitemap.xml) und weiteren Seiten aus der Navigation.

Konto, Sendungsverfolgung, Kontaktformulare und Einkauf sind auf der [HOFISH-Website](https://www.hofish.com/) verfügbar. Das Nachschlagewerk besteht aus statischen Dateien und ist zum Lesen bestimmt. Es enthält keine Shop-Skripte oder eingebetteten Formulare.

## Lokal starten

Voraussetzung ist Python 3.9 oder neuer. Zusätzliche Python-Pakete sind nicht erforderlich.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

- [English](http://localhost:8000/)
- [Deutsch](http://localhost:8000/de/)
- [Français](http://localhost:8000/fr/)

## Inhalte aktualisieren

Bearbeite die JSON-Dateien in [`content/`](content/). Verwende für dieselbe Seite in allen drei Sprachen dieselbe Kennung und Quellen-URL. Erzeuge die Website erneut und führe die Prüfungen aus, bevor du einen Pull Request öffnest. Das erzeugte Verzeichnis `dist/` wird von Git ignoriert.

## Lizenzen

Der Projektcode steht unter der [MIT-Lizenz](LICENSE). Die eigens für dieses Projekt verfassten Texte stehen unter [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). HOFISH-Marken, offizielle Quellmaterialien und Inhalte Dritter sind von beiden Lizenzen ausgenommen. Für die Quellmaterialien gelten die [HOFISH-Nutzungsbedingungen](https://www.hofish.com/pages/terms-of-use).
