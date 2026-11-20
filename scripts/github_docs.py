"""Render each reference page as Markdown for browsing directly on GitHub."""
import re
from html import escape
from posixpath import dirname, relpath
from urllib.parse import quote

from build import (
    ARTICLE_INDEX, LANGUAGES, ROOT, SHOP_INDEX, SOURCE, Edition,
    load_snapshot, path_for, reference_links, variant_rows,
)

DOCS = ROOT / "docs"


def doc_path(route, language):
    return language + "/" + path_for(route, "en").removesuffix("index.html") + "README.md"


def text(value):
    return re.sub(r"([\\`*_\[\]|])", r"\\\1", escape(value, quote=False))


def md_link(url, label):
    return f"[{text(label)}](<{url}>)"


def internal(route, target, language, label, other_language=None):
    here = doc_path(route, language)
    there = doc_path(target, other_language or language)
    return md_link(quote(relpath(there, dirname(here))), label)


def linked_list(heading, items):
    return [f"## {text(heading)}", "", *("- " + item for item in items), ""] if items else []


def render(edition, route):
    language, ui = edition.language, edition.ui
    record = edition.data[route][language]
    meta = edition.sources["pages"][route]
    snapshot = edition.sources["snapshot"]
    lines = [f'# {text(record["title"])}', ""]
    lines.append(" · ".join(
        internal(route, route, language, edition.interface[lang]["label"], other_language=lang)
        for lang in LANGUAGES
    ))
    lines.append("")
    if route != "/":
        lines.extend([internal(route, "/", language, ui["home"]), ""])
    lines.extend([
        text(record["intro"]), "",
        md_link(SOURCE + route, ui["original"]) + f' · {text(ui["snapshot"])} {snapshot}', "",
    ])
    if route == "/":
        lines.extend([
            " · ".join(internal(route, target, language, ui[key]) for target, key in (
                (SHOP_INDEX, "browse"), (ARTICLE_INDEX, "journal"),
            )),
            "",
        ])
    for section in record["sections"]:
        lines.extend(linked_list(section["title"], list(map(text, section["items"]))))
    if meta.get("options"):
        lines.extend(linked_list(ui["options"], [
            f'**{text(ui.get(option["name"].lower(), option["name"]))}** · '
            + " · ".join(map(text, option["values"]))
            for option in meta["options"]
        ]))
    if meta.get("variants"):
        lines.extend([
            f'## {text(ui["variants"])}', "", text(ui["variant_note"]), "",
            "| " + " | ".join(text(ui[key]) for key in ("variant", "price", "availability")) + " |",
            "| --- | --- | --- |",
        ])
        lines.extend(
            "| " + " | ".join(map(text, row)) + " |"
            for row in variant_rows(meta["variants"], language, ui)
        )
        lines.append("")
    if meta["type"] == "collection" and not meta["products"]:
        lines.extend([f'> {text(ui["empty"])}', ""])
    groups = edition.link_groups(route, meta)
    if route == "/":
        groups = [
            (ui[group], meta["groups"][group], False) for group in ("featured", "nursing", "pants")
        ] + [(ui["help"], edition.pages, False)]
    for heading, targets, descriptions in groups:
        items = []
        for target in targets:
            target_data = edition.data[target][language]
            item = internal(route, target, language, target_data["title"])
            if descriptions:
                item += " — " + text(target_data["intro"])
            items.append(item)
        lines.extend(linked_list(heading, items))
    related, media = reference_links(meta, language, ui)
    for heading, links in ((ui["sources"], related), (ui["media"], media)):
        lines.extend(linked_list(heading, [md_link(url, label) for url, label in links]))
    return "\n".join(lines).rstrip() + "\n"


def documents(data, sources, interface):
    for language in LANGUAGES:
        edition = Edition(language, data, sources, interface)
        for route in data:
            yield doc_path(route, language), render(edition, route)


def main():
    pages = dict(documents(*load_snapshot()))
    for path, prose in pages.items():
        file = DOCS / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(prose, encoding="utf-8")
    print(f"Wrote {len(pages)} GitHub Markdown pages.")


if __name__ == "__main__":
    main()
