from pathlib import Path
import hashlib
import re

ROOT = Path('public')
EXPECTED_HTML_COUNT = 18
FOOTER_RE = re.compile(r'<footer class="site-footer">.*?</footer>', re.S)


def split_footer(text: str, path: Path):
    matches = list(FOOTER_RE.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f'{path}: expected exactly one site-footer block, found {len(matches)}')
    m = matches[0]
    return text[:m.start()], m.group(0), text[m.end():]


about = ROOT / 'about.html'
about_text = about.read_text(encoding='utf-8')
_, canonical_footer, _ = split_footer(about_text, about)
canonical_sha = hashlib.sha256(canonical_footer.encode('utf-8')).hexdigest()

pages = sorted(ROOT.glob('*.html'))
if len(pages) != EXPECTED_HTML_COUNT:
    raise SystemExit(f'Expected {EXPECTED_HTML_COUNT} public HTML pages, found {len(pages)}: {[p.name for p in pages]}')

changed = []
for path in pages:
    original = path.read_text(encoding='utf-8')
    before, footer, after = split_footer(original, path)
    outside_sha_before = hashlib.sha256((before + after).encode('utf-8')).hexdigest()

    if footer != canonical_footer:
        updated = before + canonical_footer + after
        path.write_text(updated, encoding='utf-8')
        changed.append(path.name)

    verified = path.read_text(encoding='utf-8')
    v_before, v_footer, v_after = split_footer(verified, path)
    outside_sha_after = hashlib.sha256((v_before + v_after).encode('utf-8')).hexdigest()
    if v_footer != canonical_footer:
        raise SystemExit(f'{path}: footer verification failed')
    if outside_sha_after != outside_sha_before:
        raise SystemExit(f'{path}: non-footer content changed')

# Final site-wide identity check.
for path in pages:
    _, footer, _ = split_footer(path.read_text(encoding='utf-8'), path)
    if hashlib.sha256(footer.encode('utf-8')).hexdigest() != canonical_sha:
        raise SystemExit(f'{path}: canonical footer hash mismatch')

print(f'Canonical About footer SHA-256: {canonical_sha}')
print(f'HTML pages verified: {len(pages)}')
print(f'Pages changed: {len(changed)}')
for name in changed:
    print(f'  - {name}')
