"""Check source coverage, locale parity and links in the generated reference."""
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from build import CONTENT_FILES, LANGUAGES, ROOT, SHOP_INDEX, SOURCE, external, load, path_for


class Page(HTMLParser):
    def __init__(self, file):
        super().__init__()
        self.language = ""
        self.headings = 0
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


def main():
    output = ROOT / "dist"
    sources = load("sources")["pages"]
    content = {route: record for name in CONTENT_FILES for route, record in load(name).items()}
    assert sources.keys() == content.keys(), "Content and source routes differ"
    for route, texts in content.items():
        assert set(texts) == set(LANGUAGES), route
        for language, record in texts.items():
            assert record["title"].strip() and record["intro"].strip(), (route, language)
            for section in record["sections"]:
                assert section["title"].strip() and all(item.strip() for item in section["items"]), (route, language)

    products = {route for route, source in sources.items() if source["type"] == "product"}
    assert products == set(sources[SHOP_INDEX]["products"]), "All-products membership differs from the index"
    for route, source in sources.items():
        for key, kind in (("products", "product"), ("articles", "article"), ("tags", "tag")):
            for target in source.get(key, []):
                assert sources[target]["type"] == kind, (route, target, kind)

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


if __name__ == "__main__":
    main()
