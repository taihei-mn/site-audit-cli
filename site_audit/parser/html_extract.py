from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


@dataclass(frozen=True)
class LinkRef:
    file: Path
    href: str
    target: str | None
    rel: str | None


@dataclass(frozen=True)
class ImageRef:
    file: Path
    alt: str | None


class _Extractor(HTMLParser):
    def __init__(self, file: Path) -> None:
        super().__init__(convert_charrefs=True)
        self._file = file
        self.links: list[LinkRef] = []
        self.images: list[ImageRef] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            d = {k.lower(): v for k, v in attrs}
            href = d.get("href")
            if href is None:
                return
            self.links.append(
                LinkRef(
                    file=self._file,
                    href=href,
                    target=d.get("target"),
                    rel=d.get("rel"),
                )
            )
        elif tag == "img":
            d = {k.lower(): v for k, v in attrs}
            self.images.append(ImageRef(file=self._file, alt=d.get("alt")))


def extract_from_html_file(path: Path) -> tuple[list[LinkRef], list[ImageRef]]:
    """Extract link and image references from a single HTML file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    ex = _Extractor(file=path.resolve())
    ex.feed(text)
    ex.close()
    return ex.links, ex.images
