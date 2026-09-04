"""Make internal links repository-relative for GitHub Pages project sites."""
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit, urlunsplit
import re
import posixpath

ROOT = Path(__file__).resolve().parents[1]
ATTR = re.compile(r'\b(href|src)="([^"]+)"')

def normalize(page: Path, raw: str) -> str:
    if not raw or raw.startswith(('#', 'http:', 'https:', 'mailto:', 'tel:', 'data:', 'javascript:')):
        return raw
    parts = urlsplit(raw)
    if not parts.path:
        return raw
    page_parent = page.relative_to(ROOT).parent.as_posix()
    if parts.path.startswith('/'):
        target = parts.path.lstrip('/')
    else:
        target = posixpath.normpath(posixpath.join(page_parent, parts.path))
    relative = posixpath.relpath(target, page_parent or '.')
    return urlunsplit(('', '', relative, parts.query, parts.fragment))

count = 0
for page in ROOT.rglob('*.html'):
    if '.ipynb_checkpoints' in page.parts:
        continue
    text = page.read_text(encoding='utf-8')
    updated = ATTR.sub(lambda m: f'{m.group(1)}="{normalize(page, m.group(2))}"', text)
    if updated != text:
        page.write_text(updated, encoding='utf-8')
        count += 1
print(f'Normalized internal links in {count} HTML files.')
