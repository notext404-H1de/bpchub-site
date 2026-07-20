from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"a", "link"} and values.get("href"):
            self.urls.append(values["href"] or "")
        if tag in {"img", "script", "source"} and values.get("src"):
            self.urls.append(values["src"] or "")


def target_for(build_dir: Path, html_path: Path, url: str, base_path: str) -> Path | None:
    if not url or url.startswith(("#", "mailto:", "tel:", "data:", "//")):
        return None
    parsed = urlsplit(url)
    if parsed.scheme:
        return None

    path = unquote(parsed.path)
    if not path:
        return None
    if base_path != "/" and path.startswith(base_path):
        path = "/" + path[len(base_path) :].lstrip("/")
    if path.startswith("/"):
        target = build_dir / path.lstrip("/")
    else:
        target = html_path.parent / path

    if path.endswith("/"):
        target /= "index.html"
    elif not target.suffix:
        target /= "index.html"
    return target


def main() -> int:
    build_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    errors: list[str] = []
    html_files = sorted(build_dir.rglob("*.html"))
    redirect_count = 0

    if not html_files:
        print(f"ERROR: no HTML files found in {build_dir}")
        return 1

    home_text = (build_dir / "index.html").read_text(encoding="utf-8")
    canonical_match = re.search(
        r'<link\s+rel=["\']?canonical["\']?\s+href=(["\']?)([^\s>"\']+)\1',
        home_text,
        re.I,
    )
    base_path = urlsplit(canonical_match.group(2)).path if canonical_match else "/"
    if not base_path.endswith("/"):
        base_path += "/"

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(build_dir)
        parser = LinkParser()
        try:
            parser.feed(text)
        except Exception as exc:  # HTMLParser is tolerant; this catches true parser failures.
            errors.append(f"{relative}: HTML parse failed: {exc}")
            continue

        is_redirect = bool(re.search(r'<meta\s+http-equiv=["\']?refresh', text, re.I))
        if is_redirect:
            redirect_count += 1
        elif text.count(DISCLOSURE) < 1:
            errors.append(f"{relative}: site-wide Amazon disclosure is missing")
        if not re.search(r'<link\s+rel=["\']?canonical["\']?\s+href=', text, re.I):
            errors.append(f"{relative}: canonical link is missing")

        for url in parser.urls:
            target = target_for(build_dir, path, url, base_path)
            if target is not None and not target.exists():
                errors.append(f"{relative}: missing internal target {url}")

    cname = build_dir / "CNAME"
    if not cname.exists() or cname.read_text(encoding="utf-8").strip() != "blog.bpchub.com":
        errors.append("CNAME: expected blog.bpchub.com")
    for required in ("sitemap.xml", "robots.txt", "index.xml", "images/og-default.png"):
        if not (build_dir / required).exists():
            errors.append(f"missing generated file: {required}")

    print(
        f"Generated HTML count: {len(html_files)} "
        f"({redirect_count} redirect aliases, base path {base_path})"
    )
    for error in sorted(set(errors)):
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
