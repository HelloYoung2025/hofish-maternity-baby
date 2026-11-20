# HOFISH Maternity & Baby

[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md)

Un guide multilingue du site public HOFISH Maternity & Baby. Le projet reprend la structure du site avec l’accueil, les collections, les fiches produits, les articles du blog et les pages consacrées à la marque, à l’assistance et aux conditions de vente. Chaque fiche propose une description rédigée pour ce projet et un lien vers sa source. Le recensement repose sur 59 adresses du [plan de site XML officiel](https://www.hofish.com/sitemap.xml), complétées par des pages accessibles depuis la navigation.

**Consulter les 64 pages sur GitHub** · [English](docs/en/README.md) · [Deutsch](docs/de/README.md) · [Français](docs/fr/README.md)

## La gamme HOFISH

- **Les soutiens-gorge d’allaitement** comprennent des modèles sans coutures et sans armatures pour le quotidien et le sport. Certains ont des bonnets rabattables et sont proposés en lots.
- **Les soutiens-gorge de tirage mains libres** maintiennent les téterelles entre des couches de tissu ou dans des ouvertures zippées. Plusieurs modèles s’ouvrent aussi pour allaiter directement.
- **Les débardeurs d’allaitement et les culottes de grossesse** comprennent des hauts extensibles avec maintien intégré et ouverture à clips, ainsi que des culottes sans coutures à taille haute.
- **Les leggings, jeans et shorts de grossesse** ont une ceinture ou un bandeau extensible qui couvre le ventre. La gamme comprend aussi des shorts cyclistes à poches latérales.

Retrouvez les modèles et leur disponibilité dans le [catalogue officiel HOFISH](https://www.hofish.com/collections/all).

Le compte client, le suivi des commandes, les formulaires de contact et les achats sont accessibles sur le [site HOFISH](https://www.hofish.com/). Le guide se consulte en lecture seule et se compose de fichiers statiques. Il ne contient ni scripts de la boutique ni formulaires intégrés.

## Lancer en local

Python 3.9 ou une version ultérieure suffit. Aucun paquet Python supplémentaire n’est requis.

```sh
python3 scripts/build.py
python3 scripts/github_docs.py
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

- [English](http://localhost:8000/)
- [Deutsch](http://localhost:8000/de/)
- [Français](http://localhost:8000/fr/)

## Mettre à jour le contenu

Modifiez les fichiers JSON dans [`content/`](content/). Conservez le même identifiant et la même URL source pour une page dans les trois langues. Régénérez les deux formats et exécutez les vérifications avant d’ouvrir une pull request. Incluez les fichiers Markdown générés dans [`docs/`](docs/) avec les changements de données. Git ignore les fichiers HTML dans `dist/`.

## Licences

Le code du projet est distribué sous [licence MIT](LICENSE). Les textes rédigés pour ce projet sont distribués sous [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Les marques HOFISH, les contenus officiels et les éléments tiers sont exclus de ces deux licences. Pour les contenus sources, consultez les [conditions d’utilisation de HOFISH](https://www.hofish.com/pages/terms-of-use).
