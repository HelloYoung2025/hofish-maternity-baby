"""Build the three static HOFISH reference editions from the content snapshot."""
import argparse
from html import escape
import json
from pathlib import Path
from posixpath import dirname, relpath
import shutil
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://www.hofish.com"
REPOSITORY = "https://github.com/HelloYoung2025/hofish-maternity-baby"
LANGUAGES = ("en", "de", "fr")
CONTENT_FILES = ("catalog", "products", "blog", "pages")
MEDIA = {"image", "video"}
ARTICLE_INDEX = "/blogs/news"
SHOP_INDEX = "/collections/all"


def load(name):
    return json.loads((ROOT / "content" / f"{name}.json").read_text(encoding="utf-8"))


def path_for(route, language):
    segments = unquote(route).strip("/").split("/") if route != "/" else []
    if any(part in {"", ".", ".."} or "\\" in part for part in segments):
        raise ValueError(f"Invalid route: {route}")
    prefix = [] if language == "en" else [language]
    return "/".join([*prefix, *segments, "index.html"])


def link(url, label, css=""):
    class_attr = f' class="{css}"' if css else ""
    return f'<a{class_attr} href="{escape(url, quote=True)}">{escape(label)}</a>'


def external(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError(f"Expected a public HTTPS URL, received {url!r}")
    return url


def blocks(sections, anchored=False):
    result = []
    for index, section in enumerate(sections, start=1):
        anchor = f' id="section-{index}"' if anchored else ""
        items = "".join(f"<li>{escape(item)}</li>" for item in section["items"])
        result.append(f'<section class="prose"{anchor}><h2>{escape(section["title"])}</h2><ul>{items}</ul></section>')
    return "".join(result)


def contents_links(sections, ui):
    if len(sections) < 4:
        return ""
    links = "".join(
        f'<li>{link(f"#section-{index}", section["title"])}</li>'
        for index, section in enumerate(sections, start=1)
    )
    return f'<nav class="contents" aria-label="{escape(ui["contents"])}"><h2>{escape(ui["contents"])}</h2><ul>{links}</ul></nav>'


def options_table(options, ui):
    if not options:
        return ""
    rows = []
    for option in options:
        name = ui.get(option["name"].lower(), option["name"])
        rows.append(f'<dt>{escape(name)}</dt><dd>{escape(" · ".join(option["values"]))}</dd>')
    return (
        f'<section class="prose"><h2>{escape(ui["options"])}</h2><dl>{"".join(rows)}</dl>'
        f'<p class="small">{escape(ui["options_note"])}</p></section>'
    )


def variant_price(cents, language):
    separator = "." if language == "en" else ","
    dollars, remainder = divmod(cents, 100)
    return f"{dollars}{separator}{remainder:02} USD"


def variant_rows(variants, language, ui):
    return [
        (variant["label"], variant_price(variant["usd_cents"], language),
         ui["available"] if variant["available"] else ui["unavailable"])
        for variant in variants
    ]


def variants_table(variants, language, ui, snapshot):
    if not variants:
        return ""
    title = escape(ui["variants"])
    headers = "".join(f'<th scope="col">{escape(ui[key])}</th>' for key in ("variant", "price", "availability"))
    rows = "".join(
        f'<tr><th scope="row">{escape(label)}</th><td>{price}</td><td>{escape(availability)}</td></tr>'
        for label, price, availability in variant_rows(variants, language, ui)
    )
    return (
        f'<section class="prose"><details><summary>{title} ({len(variants)})</summary>'
        f'<p class="small">{escape(ui["snapshot"])} · {escape(snapshot)}. {escape(ui["variant_note"])}</p>'
        f'<table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></details></section>'
    )


def reference_links(metadata, language, ui):
    media, related = [], []
    for item in metadata.get("links", []):
        kind = item.get("kind", "reference")
        gallery = kind in MEDIA
        bucket = media if gallery else related
        label = item.get("title") or ui.get(kind, ui["reference"])
        if isinstance(label, dict):
            label = label[language]
        if gallery:
            label = f'{ui.get(kind, ui["image"])} {len(bucket) + 1}'
        bucket.append((external(item["url"]), label))
    return related, media


def related_sources(metadata, language, ui):
    related, media = reference_links(metadata, language, ui)
    visual = ""
    if media:
        media_links = "".join(f"<li>{link(url, label)}</li>" for url, label in media)
        visual = f'<details><summary>{escape(ui["media"])} ({len(media)})</summary><ul>{media_links}</ul></details>'
    references = "".join(f"<li>{link(url, label)}</li>" for url, label in related)
    references = f"<ul>{references}</ul>" if references else ""
    return f'<section class="prose"><h2>{escape(ui["sources"])}</h2>{references}{visual}</section>' if related or media else ""


class Edition:
    def __init__(self, language, data, sources, interface):
        self.language = language
        self.data = data
        self.sources = sources
        self.ui = interface[language]
        self.interface = interface
        self.collections = self.routes("collection")
        self.articles = self.routes("article")
        self.tags = self.routes("tag")
        self.pages = self.routes("page")

    def routes(self, kind):
        return [route for route, page in self.sources["pages"].items() if page["type"] == kind]

    def link_groups(self, route, meta):
        ui = self.ui
        kind = meta["type"]
        groups = []
        if kind == "collection":
            groups.append((ui["products"], meta["products"], True))
            if route == SHOP_INDEX:
                groups.append((ui["collections"], [item for item in self.collections if item != route], False))
        if kind == "blog":
            groups.extend([(ui["posts"], self.articles, True), (ui["tags"], self.tags, False)])
        if kind == "tag":
            groups.append((ui["posts"], meta["articles"], True))
        if kind == "article":
            groups.append((ui["tags"], meta.get("tags", []), False))
        if kind == "product":
            memberships = [
                item for item in self.collections if item != SHOP_INDEX
                and route in self.sources["pages"][item]["products"]
            ]
            groups.append((ui["collections"], memberships, False))
        if meta.get("related"):
            groups.append((ui["related_pages"], meta["related"], False))
        return groups

    def relative(self, current, target):
        return quote(relpath(target, dirname(path_for(current, self.language)) or "."))

    def href(self, current, target, language=None):
        destination = path_for(target, language or self.language)
        relative = self.relative(current, destination)
        if relative == "index.html":
            return "./"
        return relative.removesuffix("index.html")

    def internal(self, current, target, label=None, css=""):
        return link(self.href(current, target), label or self.data[target][self.language]["title"], css)

    def cards(self, current, routes, title="", descriptions=False):
        if not routes:
            return ""
        items = []
        for route in routes:
            content = self.data[route][self.language]
            summary = f'<p>{escape(content["intro"])}</p>' if descriptions else ""
            items.append(f'<li><article>{self.internal(current, route)}{summary}</article></li>')
        heading = f"<h2>{escape(title)}</h2>" if title else ""
        return f'<section class="card-section">{heading}<ul class="cards">{"".join(items)}</ul></section>'

    def source_line(self, route):
        ui = self.ui
        return (
            f'<p class="source"><span>{escape(ui["source"])}</span>'
            f'{link(SOURCE + route, ui["original"] + " ↗")}</p>'
        )

    def home(self, route, record, meta):
        ui = self.ui
        groups = meta["groups"]
        overview, *editorial_sections = record["sections"]
        primary = self.internal(route, SHOP_INDEX, ui["browse"], "button")
        secondary = self.internal(route, ARTICLE_INDEX, ui["journal"] + " →")
        hero = (
            f'<section class="hero"><div><p class="eyebrow">{escape(ui["edition"])}</p>'
            f'<h1>{escape(record["title"])}</h1><p>{escape(record["intro"])}</p>'
            f'<div class="actions">{primary}{secondary}</div></div>'
            '<div class="illustration" aria-hidden="true"><span></span><span></span><span></span></div>'
            '</section>'
        )
        highlights = "".join(
            self.cards(route, groups.get(group, []), ui[heading], descriptions=group == "featured")
            for group, heading in (("featured", "featured"), ("nursing", "nursing"), ("pants", "pants"))
        )
        return (
            hero + blocks([overview]) + highlights + blocks(editorial_sections)
            + self.cards(route, self.articles, ui["journal"])
            + self.cards(route, self.pages, ui["help"])
            + related_sources(meta, self.language, ui)
            + self.source_line(route)
        )

    def search(self, route):
        ui = self.ui
        search_intro = escape(ui["search_intro"])
        return (
            f'<h1>{escape(ui["search"])}</h1><p class="lede">{search_intro}</p>'
            f'<div class="search" hidden><label for="filter">{escape(ui["search_label"])}</label>'
            '<input id="filter" type="search" autocomplete="off" aria-controls="results">'
            f'<p id="no-results" role="status" hidden>{escape(ui["search_empty"])}</p></div>'
            f'<div id="results">{self.cards(route, list(self.data), descriptions=True)}</div>'
            f'<script src="{self.relative(route, "assets/search.js")}" defer></script>'
        )

    def content(self, route):
        ui = self.ui
        if route == "/search":
            return ui["search"], ui["search_intro"], self.search(route)
        if route == "/pages":
            title, intro = ui["help"], ui["support_intro"]
            return title, intro, (
                f'<h1>{escape(title)}</h1><p class="lede">{escape(intro)}</p>'
                + self.cards(route, self.pages, descriptions=True)
            )
        record = self.data[route][self.language]
        meta = self.sources["pages"][route]
        kind = meta["type"]
        title, intro = record["title"], record["intro"]
        if kind == "home":
            return title, intro, self.home(route, record, meta)

        breadcrumb = {
            "collection": (SHOP_INDEX, ui["shop"]),
            "product": (SHOP_INDEX, ui["shop"]),
            "article": (ARTICLE_INDEX, ui["journal"]),
            "tag": (ARTICLE_INDEX, ui["journal"]),
            "page": ("/pages", ui["help"]),
        }.get(kind)
        parent = ""
        if breadcrumb and breadcrumb[0] != route:
            parent = f'<p class="breadcrumb">{self.internal(route, *breadcrumb)} <span aria-hidden="true">/</span></p>'
        body = (
            f'{parent}<h1>{escape(title)}</h1><p class="lede">{escape(intro)}</p>'
            + contents_links(record["sections"], ui)
            + blocks(record["sections"], anchored=True) + options_table(meta.get("options"), ui)
            + variants_table(meta.get("variants"), self.language, ui, self.sources["snapshot"])
        )
        if kind == "collection" and not meta["products"]:
            body += f'<p class="notice">{escape(ui["empty"])}</p>'
        body += "".join(
            self.cards(route, targets, heading, descriptions)
            for heading, targets, descriptions in self.link_groups(route, meta)
        )
        if kind == "collection" and route != SHOP_INDEX:
            body += f'<p>{self.internal(route, SHOP_INDEX, ui["more"] + " →")}</p>'
        return title, intro, body + related_sources(meta, self.language, ui) + self.source_line(route)

    def render(self, route):
        title, description, body = self.content(route)
        ui = self.ui
        title = title if route == "/" else f"{title} | HOFISH Maternity & Baby"
        nav = []
        for target, label in (
            ("/", "home"), (SHOP_INDEX, "shop"), (ARTICLE_INDEX, "journal"), ("/pages", "help"),
        ):
            current = ' aria-current="page"' if route == target else ""
            nav.append(f'<a href="{self.href(route, target)}"{current}>{escape(ui[label])}</a>')
        languages = []
        for language in LANGUAGES:
            label = escape(self.interface[language]["label"])
            active = ' aria-current="page"' if language == self.language else ""
            languages.append(
                f'<a href="{self.href(route, route, language)}" lang="{language}" hreflang="{language}"{active}>{label}</a>'
            )
        brand = self.internal(route, "/", "HOFISH", "brand")
        search = self.internal(route, "/search", ui["search"], "search-link")
        css = self.relative(route, "assets/site.css")
        return f"""<!doctype html>
<html lang="{self.language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="referrer" content="no-referrer">
  <meta name="description" content="{escape(description, quote=True)}">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="{css}">
</head>
<body>
  {link("#main", ui["skip"], "skip")}
  <header class="top"><div class="container top-inner">
    {brand}
    <nav class="menu" aria-label="{escape(ui["navigation"])}">{"".join(nav)}{search}</nav>
    <nav class="language" aria-label="{escape(ui["language"])}">{"".join(languages)}</nav>
  </div></header>
  <main id="main" class="container{' home' if route == '/' else ''}">{body}</main>
  <footer class="container footer">
    <p>{escape(ui["footer"])} <span>{escape(ui["snapshot"])} · {escape(self.sources["snapshot"])}</span></p>
    <div>{link(REPOSITORY, "GitHub ↗")} {link(SOURCE + "/", ui["source_site"] + " ↗")}</div>
  </footer>
</body>
</html>
"""


def load_snapshot():
    data = {}
    for file in CONTENT_FILES:
        entries = load(file)
        if overlap := data.keys() & entries.keys():
            raise ValueError(f"Duplicate translations: {sorted(overlap)}")
        data.update(entries)
    sources = load("sources")
    interface = load("interface")
    if data.keys() != sources["pages"].keys():
        raise ValueError(
            f'Missing translations: {sorted(sources["pages"].keys() - data.keys())}; '
            f'extra translations: {sorted(data.keys() - sources["pages"].keys())}'
        )
    for path, texts in data.items():
        if set(texts) != set(LANGUAGES):
            raise ValueError(f"Missing language or unexpected language at {path}")
    return data, sources, interface


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    data, sources, interface = load_snapshot()
    for language in LANGUAGES:
        edition = Edition(language, data, sources, interface)
        for route in [*data, "/pages", "/search"]:
            file = args.output / path_for(route, language)
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(edition.render(route), encoding="utf-8")
    shutil.copytree(ROOT / "assets", args.output / "assets", dirs_exist_ok=True)
    print(f"Built {len(data)} source pages and 2 navigation views per language.")


if __name__ == "__main__":
    main()
