#!/usr/bin/env python3
"""The old Smith Foundation site's text, read from its WordPress export (outside Git; see
proposals/smith-foundation-site.md, "Sources"). Everything the store gets is taken from here by post
and block number, so no text is typed again: content.py says which blocks go where.

  python3 source.py blocks <export.xml> <post id> [...]   each block of a post, numbered, with its tag

A block is a heading or a paragraph. The export's text is WordPress's own: paragraphs are blank
lines or <p>, and page-builder shortcodes ([fusion_...]) wrap them. The shortcodes are dropped and
their text kept. Italics, bold and links stay; pasted styles and wrappers don't (TYPE-03).
"""
import html
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

NS = {"wp": "http://wordpress.org/export/1.2/", "content": "http://purl.org/rss/1.0/modules/content/"}
DEFAULT_EXPORT = pathlib.Path.home() / "Downloads" / "gordonandmarionsmithfoundationforyoungartists.WordPress.2026-09-28.xml"


def load(export=None):
    """{post id: {"title", "type", "content"}} from the export. It starts with blank lines, which the
    XML parser refuses, so they're skipped."""
    raw = pathlib.Path(export or DEFAULT_EXPORT).read_bytes().lstrip()
    channel = ET.fromstring(raw).find("channel")
    posts = {}
    for item in channel.findall("item"):
        posts[item.findtext("wp:post_id", namespaces=NS)] = {
            "title": item.findtext("title") or "",
            "type": item.findtext("wp:post_type", namespaces=NS),
            "content": item.findtext("content:encoded", namespaces=NS) or "",
        }
    return posts


class Blocks(HTMLParser):
    """Headings and paragraphs, each a list of Shopify rich text nodes (text, with bold and italic;
    links). A <br> ends a paragraph, as a line in the old editor did."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.nodes, self.marks, self.tag = [], [], [], "p"
        self.href, self.link_nodes = None, None

    def flush(self):
        nodes = self.nodes
        while nodes and nodes[0]["type"] == "text" and not nodes[0]["value"].strip():
            nodes.pop(0)
        while nodes and nodes[-1]["type"] == "text" and not nodes[-1]["value"].strip():
            nodes.pop()
        if nodes:
            if nodes[0]["type"] == "text":
                nodes[0]["value"] = nodes[0]["value"].lstrip()
            if nodes[-1]["type"] == "text":
                nodes[-1]["value"] = nodes[-1]["value"].rstrip()
            self.blocks.append((self.tag, [n for n in nodes if n["type"] != "text" or n["value"]]))
        self.nodes, self.tag = [], "p"

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "div", "li", "br", "ul", "ol", "img", "iframe"):
            self.flush()
        elif re.fullmatch(r"h[1-6]", tag):
            self.flush()
            self.tag = tag
        elif tag in ("em", "i"):
            self.marks.append("italic")
        elif tag in ("strong", "b"):
            self.marks.append("bold")
        elif tag == "a":
            self.href = dict(attrs).get("href")
            self.link_nodes = []

    def handle_endtag(self, tag):
        if tag in ("em", "i") and "italic" in self.marks:
            self.marks.remove("italic")
        elif tag in ("strong", "b") and "bold" in self.marks:
            self.marks.remove("bold")
        elif tag == "a" and self.link_nodes is not None:
            if self.link_nodes:
                self.nodes.append({"type": "link", "url": self.href, "children": self.link_nodes})
            self.href, self.link_nodes = None, None
        elif tag in ("p", "div", "li") or re.fullmatch(r"h[1-6]", tag):
            self.flush()

    def handle_data(self, data):
        value = re.sub(r"\s+", " ", data.replace("\xa0", " "))
        if not value.strip() and not self.nodes:
            return
        node = {"type": "text", "value": value}
        for m in sorted(set(self.marks)):
            node[m] = True
        target = self.link_nodes if self.link_nodes is not None else self.nodes
        prev = target[-1] if target else None
        if prev and prev["type"] == "text" and {k for k in prev if k not in ("type", "value")} == {k for k in node if k not in ("type", "value")}:
            prev["value"] += value
        else:
            target.append(node)


def blocks(content):
    """[(tag, nodes)] for a post's content."""
    text = re.sub(r"\[/?[a-z_]+(?:\s[^\]]*)?\]", "\n\n", content)  # shortcodes: dropped, their text kept
    text = re.sub(r"\n[ \t]*\n+", "<p>", text)  # a blank line is a paragraph break
    text = text.replace("\n", "<br>")  # a single line break too, as the old editor showed it
    parser = Blocks()
    parser.feed(text)
    parser.flush()
    return parser.blocks


def plain(nodes):
    out = ""
    for n in nodes:
        out += n["value"] if n["type"] == "text" else plain(n["children"])
    return re.sub(r"\s+", " ", out).strip()


def to_html(nodes):
    """Rich text nodes as the HTML staged page text uses."""
    out = ""
    for n in nodes:
        if n["type"] == "link":
            out += f'<a href="{html.escape(n["url"] or "")}">{to_html(n["children"])}</a>'
            continue
        v = html.escape(n["value"], quote=False)
        if n.get("bold"):
            v = f"<strong>{v}</strong>"
        if n.get("italic"):
            v = f"<em>{v}</em>"
        out += v
    return out.replace("</em><em>", "").replace("</strong><strong>", "")


if __name__ == "__main__":
    if sys.argv[1] == "blocks":
        posts = load(sys.argv[2])
        for pid in sys.argv[3:]:
            post = posts[pid]
            print(f"\n==== {pid} {post['title']} ({post['type']})")
            for n, (tag, nodes) in enumerate(blocks(post["content"])):
                print(f"{n:3} {tag:3} {plain(nodes)[:160]}")
