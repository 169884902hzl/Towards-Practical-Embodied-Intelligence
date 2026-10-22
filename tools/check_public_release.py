"""Focused offline public-release checks. Stdlib only; no writes."""
import ast
import hashlib
import html
import re
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = [ROOT / n for n in ("README.md", "README_zh.md", "CONTRIBUTING.md", "labs/README.md")] + sorted((ROOT / "docs").glob("*.md"))


def slug(value):
    value = re.sub(r'<[^>]+>', '', value).replace('`', '').replace('*', '')
    return ''.join(c for c in html.unescape(value).lower() if c in ' -_' or c.isalnum() or
                   ord(c) > 127 and not unicodedata.category(c).startswith(('P', 'S'))).replace(' ', '-')


def main():
    errors = []
    used = set()
    sources = DOCS + [ROOT / "index.html"]
    for path in DOCS:
        contents = path.read_text(encoding="utf-8")
        opened = None
        ids = set()
        counts = {}
        links = []
        for number, line in enumerate(contents.splitlines(), 1):
            fence = re.match(r'^\s*(`{3,}|~{3,})', line)
            if fence:
                mark = fence[1]
                if opened is None:
                    opened = (mark, number)
                elif mark[0] == opened[0][0] and len(mark) >= len(opened[0]):
                    opened = None
                continue
            if opened:
                continue
            heading = re.match(r'^#{1,6}\s+(.+)', line)
            if heading:
                name = slug(heading[1]); n = counts.get(name, 0); counts[name] = n + 1
                ids.add(name + (f'-{n}' if n else ''))
            links += [(number, u) for u in re.findall(r'\]\((#[^ )]+)\)', line)]
        if opened:
            errors.append(f"{path.name}:{opened[1]} unclosed code fence")
        for number, link in links:
            if unquote(link[1:]) not in ids:
                errors.append(f"{path.name}:{number} missing anchor {link}")
    for path in sources:
        contents = path.read_text(encoding="utf-8")
        for name in re.findall(r'assets/ei_tutorial/([A-Za-z0-9_.-]+\.(?:svg|jpg|png))', contents):
            target = ROOT / "assets" / "ei_tutorial" / name
            used.add(name)
            if not target.exists() or target.stat().st_size == 0:
                errors.append(f"{path.name}: missing/empty asset {name}")
        if re.search(r'(?i)\b[A-Z]:[\\/]|obsidian://', contents):
            errors.append(f"{path.name}: machine-specific path or URI")
    for path in (ROOT / "assets/ei_tutorial").glob("*.svg"):
        ET.parse(path)
    actual = {p.name for p in (ROOT / "assets/ei_tutorial").iterdir() if p.is_file()}
    if actual != used:
        errors.append(f"Unreferenced assets: {sorted(actual-used)}")
    for path in (ROOT / "labs").glob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    # Whole-token and two-token phrase hashes avoid republishing restricted project names in the guard.
    blocked_hashes = {
        'a93077598e3d8e6977d6620ba32fcc82e3a01e0d25b2e0465a095c8fe8ed3476',
        '46bd7a5ae06f9d65ac11eef479efe60050d8bd4e3b04b874cc116d2ef4cc2756',
        '1aab57bd8a77a470c0e770c01a17ea2d2af6ce037cc4786dee47fff0b2af057e',
        'c2297af8db2e824420ac2014a3c1cdcdf2f06ad9de057ee22263ac731dbd80ee',
        '7270e89961b0d9ad37e6c997e0ff4a0e5c6a1696d22b531f224e4de128ac5e72',
        'c8ed8ba117f4b72b0b2089e4d90e83a4ddd5815aa4a7a1b6fc9a718cb34c65c6',
        '53e0614c4b1a9500a315d959219fa3fee59872982c7de3e619c2bc12b1ff4eaf',
        '8830bb9c7e35f88344c9d87483d445b8c8675cdce4b3f045849972aeec00e9aa',
        '5bc0f7ac83be96ac8d0ddde109f293b30defb6f18e58fc50a93a1a395817a3ae',
        'ca6b5cb80440aeac998eb8ffa84fedd6fd60ba7aac5cc7607503fa3b12e1a745',
    }
    for path in sources + list((ROOT / "labs").glob("*.py")) + list((ROOT / "assets/ei_tutorial").glob("*.svg")):
        tokens = re.findall(r'[A-Za-z][A-Za-z0-9_-]*', path.read_text(encoding="utf-8").lower())
        bigrams = [f"{a} {b}" for a, b in zip(tokens, tokens[1:])]
        for candidate in tokens + bigrams:
            if hashlib.sha256(candidate.encode()).hexdigest() in blocked_hashes:
                errors.append(f"{path.name}: restricted token hash matched")
                break
    chapter = (ROOT / "docs/06_Glossary_Templates_and_Checklists.md").read_text(encoding="utf-8")
    for path in sorted((ROOT / "labs").glob("*.py")):
        if path.read_text(encoding="utf-8").strip() not in chapter:
            errors.append(f"Embedded lab is stale: {path.name}")
    monolith = (ROOT / "docs/Full_Tutorial_CN.md").read_text(encoding="utf-8")
    for path in sorted((ROOT / "docs").glob("0[0-6]*.md")):
        raw = path.read_text(encoding="utf-8").split('</p>', 1)[1].lstrip('\n')
        if raw.startswith('---'):
            raw = raw[3:].lstrip('\n')
        if path.name.startswith("01_"):
            preface, stage1 = raw.split("## 具身智能入门：阶段 1 基础框架", 1)
            segments = [preface.strip(), ("## 具身智能入门：阶段 1 基础框架" + stage1).strip()]
        else:
            segments = [raw.strip()]
        if any(seg not in monolith for seg in segments):
            errors.append(f"Monolith is stale: {path.name}")
    page = (ROOT / "index.html").read_text(encoding="utf-8")
    for name in ("katex.min.css", "katex.min.js", "auto-render.min.js"):
        rel = "assets/katex/" + name
        if rel not in page or not (ROOT / rel).exists():
            errors.append("Missing local math resource: " + rel)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f"Verified {len(DOCS)} Markdown documents, {len(used)} figures, embedded labs and monolith (offline).")


if __name__ == "__main__":
    main()
