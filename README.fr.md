# HOFISH Maternity & Baby

[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md)

Un guide multilingue du site public HOFISH Maternity & Baby. Le projet reprend la structure du site avec l’accueil, les collections, les fiches produits, les articles du blog et les pages consacrées à la marque, à l’assistance et aux conditions de vente. Chaque fiche propose une description rédigée pour ce projet et un lien vers sa source. Le recensement repose sur 59 adresses du [plan de site XML officiel](https://www.hofish.com/sitemap.xml), complétées par des pages accessibles depuis la navigation.

Le compte client, le suivi des commandes, les formulaires de contact et les achats sont accessibles sur le [site HOFISH](https://www.hofish.com/). Le guide se consulte en lecture seule et se compose de fichiers statiques. Il ne contient ni scripts de la boutique ni formulaires intégrés.

## Lancer en local

Python 3.9 ou une version ultérieure suffit. Aucun paquet Python supplémentaire n’est requis.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

- [English](http://localhost:8000/)
- [Deutsch](http://localhost:8000/de/)
- [Français](http://localhost:8000/fr/)

## Mettre à jour le contenu

Modifiez les fichiers JSON dans [`content/`](content/). Conservez le même identifiant et la même URL source pour une page dans les trois langues. Régénérez le site et exécutez les vérifications avant d’ouvrir une pull request. Git ignore le répertoire généré `dist/`.

## Licences

Le code du projet est distribué sous [licence MIT](LICENSE). Les textes rédigés pour ce projet sont distribués sous [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Les marques HOFISH, les contenus officiels et les éléments tiers sont exclus de ces deux licences. Pour les contenus sources, consultez les [conditions d’utilisation de HOFISH](https://www.hofish.com/pages/terms-of-use).
