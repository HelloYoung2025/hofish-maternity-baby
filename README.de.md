# HOFISH Maternity & Baby

[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md)

Ein mehrsprachiges Nachschlagewerk zur öffentlichen Website von HOFISH Maternity & Baby. Die Gliederung folgt der Website mit Startseite, Kollektionen, Produktseiten, Blogbeiträgen sowie Seiten zur Marke, zum Kundenservice und zu den Geschäftsbedingungen. Jeder Eintrag enthält eine eigenständig formulierte Beschreibung und einen Link zur Quelle. Die Erfassung basiert auf 59 URLs der [offiziellen XML-Sitemap](https://www.hofish.com/sitemap.xml) und weiteren Seiten aus der Navigation.

**Alle 64 Seiten auf GitHub lesen** · [English](docs/en/README.md) · [Deutsch](docs/de/README.md) · [Français](docs/fr/README.md)

## Das Sortiment von HOFISH

- **Still-BHs** gibt es als nahtlose, bügellose Modelle für Alltag und Sport. Ausgewählte Modelle haben herunterklappbare Cups und sind als Mehrfachpack erhältlich.
- **Abpump-BHs** halten die Brusthauben mit überlappenden Stofflagen oder Reißverschlussöffnungen in Position, damit die Hände frei bleiben. Mehrere Modelle lassen sich auch zum Stillen öffnen.
- **Stilltops und Umstandsslips** umfassen elastische Tops mit integriertem Halt und Clips zum Öffnen sowie nahtlose Slips mit hohem Bund.
- **Umstandsleggings, Jeans und Shorts** haben einen dehnbaren Bund oder Einsatz über dem Bauch. Dazu gehören auch Radlershorts mit Seitentaschen.

Modelle und aktuelle Verfügbarkeit finden Sie im [offiziellen HOFISH-Katalog](https://www.hofish.com/collections/all).

Konto, Sendungsverfolgung, Kontaktformulare und Einkauf sind auf der [HOFISH-Website](https://www.hofish.com/) verfügbar. Das Nachschlagewerk besteht aus statischen Dateien und ist zum Lesen bestimmt. Es enthält keine Shop-Skripte oder eingebetteten Formulare.

## Lokal starten

Voraussetzung ist Python 3.9 oder neuer. Zusätzliche Python-Pakete sind nicht erforderlich.

```sh
python3 scripts/build.py
python3 scripts/github_docs.py
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

- [English](http://localhost:8000/)
- [Deutsch](http://localhost:8000/de/)
- [Français](http://localhost:8000/fr/)

## Inhalte aktualisieren

Bearbeite die JSON-Dateien in [`content/`](content/). Verwende für dieselbe Seite in allen drei Sprachen dieselbe Kennung und Quellen-URL. Erzeuge beide Formate erneut und führe die Prüfungen aus, bevor du einen Pull Request öffnest. Committe die erzeugten Markdown-Dateien in [`docs/`](docs/) mit den Datenänderungen. Git ignoriert die HTML-Dateien in `dist/`.

## Lizenzen

Der Projektcode steht unter der [MIT-Lizenz](LICENSE). Die eigens für dieses Projekt verfassten Texte stehen unter [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). HOFISH-Marken, offizielle Quellmaterialien und Inhalte Dritter sind von beiden Lizenzen ausgenommen. Für die Quellmaterialien gelten die [HOFISH-Nutzungsbedingungen](https://www.hofish.com/pages/terms-of-use).
