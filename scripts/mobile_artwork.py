"""Reflow editorial artwork for narrow GitHub profile viewports."""

import re
import textwrap
from pathlib import Path

from build_artwork import frame, text, INK

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'


def save(name, body, height, title):
    content = frame(body, height, title).replace('width="1000"', 'width="600"').replace(f'viewBox="0 0 1000 {height}"', f'viewBox="0 0 600 {height}"')
    (ASSETS / f'{name}-mobile.svg').write_text(content, encoding='utf-8')


def artwork(name):
    content = (ASSETS / f'{name}.svg').read_text(encoding='utf-8')
    return re.sub(r'^<rect[^>]+/>', '', content.split('</style>')[1].removesuffix('</svg>'))


def main():
    hero = artwork('hero').split('<path d="M40 438H960"')[0]
    body = f'<g transform="scale(.6)">{hero}</g>'
    body += '<path d="M24 271H576" stroke="#23211e"/>'
    body += text(24, 309, 'Full stack developer &', 27)
    body += text(24, 344, 'open source contributor.', 27)
    body += text(24, 387, 'B.Tech CSE · LNMIIT, Jaipur', 24)
    save('hero', body, 415, 'Varun Rawat, full stack developer and open source contributor at LNMIIT, Jaipur')

    projects = [
        ('filmory', 458, 412, ['A recommendation system that learns how your taste changes.', 'Neural collaborative filtering, sequential transformers and adaptive ranking.', 'Personalized discovery, watchlists and explainable recommendations.'], ['React · TypeScript · FastAPI', 'PyTorch · PostgreSQL']),
        ('codecollab', 466, 420, ['A browser workspace for building together, in real time.', 'Shared Monaco editing, whiteboards, terminals and WebRTC communication.', 'Project-aware AI assistance with vector search and persistent state.'], ['Next.js · Socket.IO · WebRTC', 'pgvector · Redis']),
    ]
    for name, cutoff, poster_height, paragraphs, stack in projects:
        poster = artwork(name).split(f'<text x="40" y="{cutoff}"')[0]
        body = f'<g transform="scale(.6)">{poster}</g>'
        y = int(poster_height*.6)+42
        for i, paragraph in enumerate(paragraphs):
            for line in textwrap.wrap(paragraph, width=41):
                body += text(24, y, line, 26, 'font-weight="700"' if i == 0 else '')
                y += 35
            y += 17
        body += f'<path d="M24 {y}H576" stroke="#b3aa9a"/>'
        y += 39
        for line in stack:
            body += text(24, y, line, 23)
            y += 33
        y += 22
        body += text(24, y, 'EXPLORE THE SOURCE ↗', 22, 'font-weight="700"')
        save(name, body, y+37, name.title() + ' — project overview and stack')

    body = ''
    rows = [('Web','React · Next.js · Vue · TypeScript'),('Backend','Node.js · Express · Django · FastAPI'),('Data & ML','PostgreSQL · MongoDB · Redis · PyTorch'),('Tools','Git · Linux · Docker · Nginx'),('Beyond the stack','Competitive programming · System design · Cloud architecture'),('Teaching','Former DSA teaching assistant at LNMIIT (Jan–Apr 2026)')]
    y = 35
    for label, values in rows:
        body += text(24,y,label,25,'font-weight="700"')
        y += 36
        for line in textwrap.wrap(values,width=40):
            body += text(24,y,line,24)
            y += 34
        body += f'<path d="M24 {y+4}H576" stroke="#c6bfb2"/>'
        y += 50
    save('toolkit',body,y,'Toolkit and background')

    readme = (ROOT/'README.md').read_text(encoding='utf-8')
    for name in ['hero','filmory','codecollab','toolkit']:
        if f'srcset="assets/{name}-mobile.svg"' in readme:
            continue
        pattern = rf'(<img src="assets/{name}\.svg"[^>]+/>)'
        readme = re.sub(pattern, rf'<picture><source media="(max-width: 600px)" srcset="assets/{name}-mobile.svg" />\1</picture>', readme)
    (ROOT/'README.md').write_text(readme,encoding='utf-8')


if __name__ == '__main__':
    main()
