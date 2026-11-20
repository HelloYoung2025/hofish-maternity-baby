# HOFISH Maternity & Baby

[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md)

A multilingual reference to the public HOFISH Maternity & Baby website. The project follows the source site's structure across home, collections, product pages, blog posts, and brand, support, and policy pages. Each entry has an independently written description and links to its source. The initial inventory starts with 59 URLs from the [official XML sitemap](https://www.hofish.com/sitemap.xml), supplemented by routes found in site navigation.

**Browse all 64 pages on GitHub** · [English](docs/en/README.md) · [Deutsch](docs/de/README.md) · [Français](docs/fr/README.md)

## What HOFISH sells

- **Nursing bras** include seamless, wire-free everyday and sports styles. Selected models have drop-down cups and come in multipacks.
- **Hands-free pumping bras** use layered fabric or zip openings to hold pump flanges. Several models also open for direct nursing.
- **Nursing camisoles and maternity briefs** include stretchy tops with built-in support and clip-down access, and seamless briefs with a high waistband.
- **Maternity leggings, jeans and shorts** feature stretchy over-bump waistbands or panels. The range includes biker shorts with side pockets.

See styles and current availability in the [official HOFISH catalog](https://www.hofish.com/collections/all).

Account access, order tracking, support forms, and purchases are available through the [HOFISH website](https://www.hofish.com/). The generated reference is read-only and uses static files. It contains no store scripts or embedded forms.

## Run locally

Requires Python 3.9 or later. No Python packages are required.

```sh
python3 scripts/build.py
python3 scripts/github_docs.py
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

- [English](http://localhost:8000/)
- [Deutsch](http://localhost:8000/de/)
- [Français](http://localhost:8000/fr/)

## Update the content

Edit the JSON files in [`content/`](content/). Keep the source URL and page identity consistent across English, German, and French. Rebuild both formats and run the checks before opening a pull request. Commit the generated Markdown in [`docs/`](docs/) with the data changes. The HTML build in `dist/` is excluded from Git.

## Licensing

Project code is licensed under the [MIT License](LICENSE). Original text written for this project is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). HOFISH marks, official source materials, and third-party assets are excluded from both grants. For the source materials, see the [HOFISH Terms of Use](https://www.hofish.com/pages/terms-of-use).
