from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
ARTICLE_SECTIONS = {"skincare", "hair-care", "body-care", "guides"}
REQUIRED_FIELDS = ("title", "description", "date", "draft")


def front_matter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) == 3 else ""


def field_value(front: str, field: str) -> str:
    match = re.search(rf"(?m)^{re.escape(field)}:\s*(.*)$", front)
    return match.group(1).strip().strip("'\"") if match else ""


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    published_articles = 0

    for path in sorted(CONTENT.rglob("*.md")):
        if path.name == "_index.md":
            continue
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8-sig")
        front = front_matter(text)
        if not front:
            errors.append(f"{relative}: 缺少 YAML front matter")
            continue

        section = path.relative_to(CONTENT).parts[0]
        if section in ARTICLE_SECTIONS:
            for field in REQUIRED_FIELDS:
                if not field_value(front, field):
                    errors.append(f"{relative}: 缺少字段 {field}")
            description = field_value(front, "description")
            if description and not 70 <= len(description) <= 170:
                warnings.append(f"{relative}: description 建议控制在 70–170 个英文字符")
            if field_value(front, "draft").lower() == "false":
                published_articles += 1

        uses_amazon = "{{< amazon-link" in text or "{{< product-card" in text
        affiliate = field_value(front, "affiliate").lower() == "true"
        if uses_amazon and not affiliate:
            errors.append(f"{relative}: 使用 Amazon 短代码时必须设置 affiliate: true")
        if re.search(r"https?://(?:(?:www\.)?amazon\.(?:com|ca)|amzn\.to)", text) and not uses_amazon:
            warnings.append(f"{relative}: 发现直接 Amazon 链接，建议改用 amazon-link 短代码")

    print(f"Published article count: {published_articles}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if published_articles < 10:
        print("NOTICE: Amazon 审核前建议至少准备 10 篇公开原创文章。")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
