#!/usr/bin/env python3
"""Small helpers for generating Kadence block markup.

These helpers intentionally cover the fragile blocks used most often in MTI page
generation. Extend only after inspecting saved markup from the target site.
"""

from __future__ import annotations

import argparse
import html
import json
import secrets
import string
from typing import Iterable


def _json(attrs: dict) -> str:
    return json.dumps({k: v for k, v in attrs.items() if v is not None}, separators=(",", ":"))


def unique_id(prefix: str = "mti", length: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return prefix + "_" + "".join(secrets.choice(alphabet) for _ in range(length))


def advanced_heading(
    content: str,
    tag: str = "p",
    unique: str | None = None,
    class_name: str = "",
    href: str | None = None,
    attrs: dict | None = None,
) -> str:
    if tag not in {"p", "h1", "h2", "h3", "h4", "h5", "h6", "div", "span"}:
        raise ValueError(f"Unsupported advanced heading tag: {tag}")
    unique = unique or unique_id("kb")
    attrs = dict(attrs or {})
    attrs.setdefault("uniqueID", unique)
    attrs.setdefault("htmlTag", tag)
    if class_name:
        attrs.setdefault("className", class_name)

    escaped = html.escape(content, quote=False)
    if href:
        escaped = f'<a href="{html.escape(href, quote=True)}">{escaped}</a>'

    classes = " ".join(
        part
        for part in [
            f"kt-adv-heading{unique}",
            class_name,
            "wp-block-kadence-advancedheading",
        ]
        if part
    )
    return (
        f"<!-- wp:kadence/advancedheading {_json(attrs)} -->\n"
        f'<{tag} class="{html.escape(classes, quote=True)}" data-kb-block="kb-adv-heading{html.escape(unique, quote=True)}">{escaped}</{tag}>\n'
        "<!-- /wp:kadence/advancedheading -->"
    )


def image_block(
    attachment_id: int,
    url: str,
    alt: str = "",
    unique: str | None = None,
    class_name: str = "",
    width: int | None = None,
    height: int | None = None,
    size_slug: str = "full",
) -> str:
    unique = unique or unique_id("image")
    attrs = {"id": attachment_id, "sizeSlug": size_slug, "uniqueID": unique}
    if width:
        attrs["width"] = width
    if height:
        attrs["height"] = height
    if class_name:
        attrs["className"] = class_name
    resized = " is-resized" if width or height else ""
    classes = " ".join(
        part
        for part in ["wp-block-kadence-image", f"kb-image{unique}", f"size-{size_slug}{resized}", class_name]
        if part
    )
    wh = ""
    if width:
        wh += f' width="{int(width)}"'
    if height:
        wh += f' height="{int(height)}"'
    return (
        f"<!-- wp:kadence/image {_json(attrs)} -->\n"
        f'<figure class="{html.escape(classes, quote=True)}"><img src="{html.escape(url, quote=True)}" alt="{html.escape(alt, quote=True)}" class="kb-img wp-image-{int(attachment_id)}"{wh}/></figure>\n'
        "<!-- /wp:kadence/image -->"
    )


def column(inner: str, unique: str | None = None, class_name: str = "", index: int | None = None, attrs: dict | None = None) -> str:
    unique = unique or unique_id("col")
    attrs = dict(attrs or {})
    attrs.setdefault("uniqueID", unique)
    attrs.setdefault("kbVersion", 2)
    if class_name:
        attrs.setdefault("className", class_name)
    classes = " ".join(part for part in ["wp-block-kadence-column", f"kadence-column{unique}", class_name] if part)
    return (
        f"<!-- wp:kadence/column {_json(attrs)} -->\n"
        f'<div class="{html.escape(classes, quote=True)}"><div class="kt-inside-inner-col">'
        f"{inner}"
        "</div></div>\n"
        "<!-- /wp:kadence/column -->"
    )


def rowlayout(
    columns: Iterable[str],
    unique: str | None = None,
    class_name: str = "",
    column_count: int | None = None,
    col_layout: str = "equal",
    html_tag: str = "section",
    attrs: dict | None = None,
) -> str:
    unique = unique or unique_id("row")
    cols = list(columns)
    attrs = dict(attrs or {})
    attrs.setdefault("uniqueID", unique)
    attrs.setdefault("columns", column_count or len(cols))
    attrs.setdefault("colLayout", col_layout)
    attrs.setdefault("htmlTag", html_tag)
    attrs.setdefault("inheritMaxWidth", True)
    attrs.setdefault("kbVersion", 2)
    if class_name:
        attrs.setdefault("className", class_name)
    return (
        f"<!-- wp:kadence/rowlayout {_json(attrs)} -->\n"
        + "\n".join(cols)
        + "\n<!-- /wp:kadence/rowlayout -->"
    )


def single_button(text: str, link: str, unique: str | None = None, class_name: str = "", attrs: dict | None = None) -> str:
    unique = unique or unique_id("btn")
    attrs = dict(attrs or {})
    attrs.setdefault("uniqueID", unique)
    attrs.setdefault("text", text)
    attrs.setdefault("link", link)
    if class_name:
        attrs.setdefault("className", class_name)
    return f"<!-- wp:kadence/singlebtn {_json(attrs)} /-->"


def advanced_buttons(buttons: Iterable[str], unique: str | None = None, class_name: str = "", attrs: dict | None = None) -> str:
    unique = unique or unique_id("btns")
    btns = list(buttons)
    attrs = dict(attrs or {})
    attrs.setdefault("uniqueID", unique)
    attrs.setdefault("btnCount", len(btns))
    if class_name:
        attrs.setdefault("className", class_name)
    classes = " ".join(part for part in ["wp-block-kadence-advancedbtn", "kb-buttons-wrap", f"kb-btns{unique}", class_name] if part)
    return (
        f"<!-- wp:kadence/advancedbtn {_json(attrs)} -->\n"
        f'<div class="{html.escape(classes, quote=True)}">\n'
        + "\n".join(btns)
        + "\n</div>\n"
        "<!-- /wp:kadence/advancedbtn -->"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate small Kadence block snippets.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    h = sub.add_parser("heading")
    h.add_argument("content")
    h.add_argument("--tag", default="p")
    h.add_argument("--unique")
    h.add_argument("--class-name", default="")
    h.add_argument("--href")

    args = parser.parse_args()
    if args.cmd == "heading":
        print(advanced_heading(args.content, tag=args.tag, unique=args.unique, class_name=args.class_name, href=args.href))


if __name__ == "__main__":
    main()
