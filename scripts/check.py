"""Check source coverage, locale parity and links in the generated reference."""
from collections import Counter
from html.parser import HTMLParser
import re
from urllib.parse import unquote, urlsplit

from build import LANGUAGES, ROOT, SHOP_INDEX, SOURCE, external, load_snapshot, path_for
from github_docs import DOCS, doc_path, documents


class Page(HTMLParser):
    def __init__(self, file):
        super().__init__()
        self.language = ""
        self.headings = 0
        self.table_rows = 0
        self.links = []
        self.assets = []
        self.ids = set()
        self.feed(file.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f'Duplicate HTML id {attrs["id"]}'
            self.ids.add(attrs["id"])
        if tag == "html":
            self.language = attrs["lang"]
        if tag == "h1":
            self.headings += 1
        if tag == "tr":
            self.table_rows += 1
        if tag == "a":
            self.links.append((attrs["href"], attrs.get("hreflang")))
        if tag in {"link", "script"}:
            self.assets.append(attrs["href" if tag == "link" else "src"])
        assert tag not in {"form", "iframe"}, f"Unexpected element: {tag}"


def destination(file, url):
    path = unquote(urlsplit(url).path)
    if not path:
        return file
    result = (file.parent / path).resolve()
    return result / "index.html" if result.is_dir() else result


def check_github_docs(content, manifest, interface):
    expected = {DOCS / path: prose for path, prose in documents(content, manifest, interface)}
    assert set(DOCS.rglob("*.md")) == expected.keys(), "Missing or stale GitHub pages"
    linked = {}
    for file, prose in expected.items():
        assert file.read_text(encoding="utf-8") == prose, f"Regenerate {file}"
        linked[file] = set()
        for url in re.findall(r"\]\(<([^>]+)>\)", prose):
            if urlsplit(url).scheme:
                external(url)
            else:
                target = destination(file, url)
                assert target in expected, (file, url, target)
                linked[file].add(target)
    for language in LANGUAGES:
        pending = [DOCS / doc_path("/", language)]
        visited = set()
        while pending:
            file = pending.pop()
            if file in visited:
                continue
            visited.add(file)
            pending.extend(target for target in linked[file] if target.is_relative_to(DOCS / language))
        assert visited == {file for file in expected if file.is_relative_to(DOCS / language)}, language
    print(f"Verified {len(expected)} GitHub pages are current, linked and reachable by language.")


def main():
    output = ROOT / "dist"
    content, manifest, interface = load_snapshot()
    sources = manifest["pages"]
    for route, texts in content.items():
        english_items = [len(section["items"]) for section in texts["en"]["sections"]]
        assert english_items and all(english_items), route
        for language, record in texts.items():
            assert record["title"].strip() and record["intro"].strip(), (route, language)
            assert [len(section["items"]) for section in record["sections"]] == english_items, (route, language)
            for section in record["sections"]:
                assert section["title"].strip() and all(item.strip() for item in section["items"]), (route, language)

    products = {route for route, source in sources.items() if source["type"] == "product"}
    assert products == set(sources[SHOP_INDEX]["products"]), "All-products membership differs from the index"
    for route, source in sources.items():
        for key, kind in (("products", "product"), ("articles", "article"), ("tags", "tag")):
            for target in source.get(key, []):
                assert sources[target]["type"] == kind, (route, target, kind)
        if route in products:
            variants = source["variants"]
            assert variants and len({row["label"] for row in variants}) == len(variants), route
            for variant in variants:
                assert isinstance(variant["available"], bool) and variant["usd_cents"] > 0, route
        assert all(target in sources and target != route for target in source.get("related", [])), route

    expected = {
        (output / path_for(route, language)): (route, language)
        for route in [*sources, "/pages", "/search"]
        for language in LANGUAGES
    }
    assert len(expected) == (len(sources) + 2) * len(LANGUAGES), "Local route collision"
    assert set(output.rglob("index.html")) == expected.keys(), "Missing or stale built pages"
    checked_links = 0
    for file, (route, language) in expected.items():
        page = Page(file)
        assert page.language == language and page.headings == 1, file
        alternates = {lang: destination(file, url) for url, lang in page.links if lang}
        assert alternates == {lang: output / path_for(route, lang) for lang in LANGUAGES}, file
        if route in sources:
            assert (SOURCE + route, None) in page.links, file
        if route in products:
            assert page.table_rows == len(sources[route]["variants"]) + 1, file
        for asset in page.assets:
            assert not urlsplit(asset).netloc and destination(file, asset).is_file(), (file, asset)
        for url, _ in page.links:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                external(url)
            else:
                target = destination(file, url)
                assert target in expected, (file, url, target)
                if parts.fragment:
                    assert parts.fragment in (page if target == file else Page(target)).ids, (file, url)
                checked_links += 1
    counts = Counter(page["type"] for page in sources.values())
    indexed = sum(page["indexed"] for page in sources.values())
    print(f"Verified {len(expected)} pages, {checked_links} internal links, {indexed} indexed and "
          f"{len(sources) - indexed} supplemental source routes.")
    print(", ".join(f"{kind}: {count}" for kind, count in sorted(counts.items())))
    check_github_docs(content, manifest, interface)


if __name__ == "__main__":
    main()
