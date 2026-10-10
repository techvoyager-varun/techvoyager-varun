"""Build original editorial SVG artwork. No external fonts or image services."""

from html import escape
from math import cos, sin, pi
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
PAPER = '#f2ede3'
INK = '#23211e'
RED = '#e6492d'


def frame(body, height, title, color=PAPER):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" fill="{INK}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>
<style>text{{font-family:Arial,Helvetica,sans-serif}}.mono{{font-family:Consolas,monospace}}.serif{{font-family:Georgia,serif}}@media(prefers-reduced-motion:reduce){{.moving{{display:none}}}}</style>
<rect width="1000" height="{height}" fill="{color}"/>{body}</svg>'''


def save(name, body, height, title, color=PAPER):
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / f'{name}.svg').write_text(frame(body, height, title, color), encoding='utf-8')


def text(x, y, value, size=20, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" {extra}>{escape(value)}</text>'


def rosette(cx, cy, radius, count=12):
    points = []
    for i in range(360):
        theta = i * pi / 180
        r = radius * (.77 + .23 * cos(count * theta))
        points.append(f'{cx + r * cos(theta):.2f},{cy + r * sin(theta):.2f}')
    return '<polygon points="' + ' '.join(points) + f'" fill="{RED}"/>'


def main():
    body = text(40, 43, 'VARUN RAWAT / TECHVOYAGER', 17, 'class="mono" letter-spacing="1"')
    body += text(960, 43, 'JAIPUR, INDIA', 16, 'class="mono" text-anchor="end"')
    body += '<path d="M40 63H960" stroke="#23211e"/>'
    body += text(31, 224, 'VARUN', 155, 'font-weight="900" letter-spacing="-10"')
    body += text(31, 383, 'RAWAT', 155, 'font-weight="900" letter-spacing="-10"')
    body += rosette(789, 235, 150)
    body += '<circle cx="789" cy="235" r="57" fill="#f2ede3"/>'
    body += text(789, 246, '</>', 34, 'text-anchor="middle" class="mono" font-weight="700"')
    body += '<g class="moving"><animateTransform attributeName="transform" type="rotate" from="0 789 235" to="360 789 235" dur="45s" repeatCount="indefinite"/><circle cx="789" cy="235" r="94" stroke="#f2ede3" stroke-width="2" fill="none" stroke-dasharray="4 12"/></g>'
    body += text(646, 410, 'CODE. COLLABORATE. CREATE.', 15, 'class="mono"')
    body += '<path d="M40 438H960" stroke="#23211e"/>'
    body += text(40, 478, 'Full stack developer & open source contributor.', 26)
    body += text(40, 512, 'B.Tech Computer Science · LNMIIT, Jaipur', 22)
    body += text(960, 518, '↓', 40, 'text-anchor="end"')
    save('hero', body, 548, 'Varun Rawat — Full stack developer and open source contributor, B.Tech Computer Science at LNMIIT, Jaipur')

    for name, label, caption in [('projects-heading','SELECTED WORK','TWO PROJECTS. BUILT END TO END.'),('stack-heading','THE TOOLKIT','LANGUAGES / FRAMEWORKS / INFRASTRUCTURE'),('opensource-heading','IN THE OPEN','CONTRIBUTING BEYOND MY OWN REPOSITORIES'),('activity-heading','BY THE NUMBERS','PUBLIC GITHUB DATA / DAILY REFRESH')]:
        body = text(40, 61, label, 40, 'font-weight="900" letter-spacing="-1"')
        body += text(40, 92, caption, 15, 'class="mono"')
        body += '<path d="M40 112H960" stroke="#23211e" stroke-width="2"/>'
        save(name,body,130,label)

    # A cinema-inspired project poster, with an abstract four-stage motif.
    body = '<rect x="0" y="0" width="1000" height="412" fill="#211f1d"/>'
    body += '<g fill="#f2ede3" font-family="Arial,sans-serif"><text x="40" y="46" font-size="16" fill="#f2ede3" letter-spacing="2">01 / MACHINE LEARNING + MOVIE DISCOVERY</text><text x="37" y="155" font-size="104" font-weight="900" fill="#f2ede3" letter-spacing="-5">Filmory</text><text x="40" y="205" font-size="25" fill="#f2ede3">Better movies. Personal taste.</text></g>'
    # Frame silhouettes, warm film stock and oversized reel; no fake app screenshots.
    for i, color in enumerate(['#e6492d','#e89d48','#dfc8a7','#7c8b72']):
        x=42+i*119
        body+=f'<rect x="{x}" y="248" width="102" height="117" fill="{color}"/>'
        body+=f'<circle cx="{x+51}" cy="289" r="22" fill="#211f1d"/>'
        body+=f'<path d="M{x+16} 349Q{x+51} 296 {x+86} 349Z" fill="#211f1d"/>'
    body+='<circle cx="786" cy="222" r="157" fill="#e6492d"/>'
    for i in range(5):
        a=i*2*pi/5
        body+=f'<circle cx="{786+94*cos(a)}" cy="{222+94*sin(a)}" r="38" fill="#211f1d"/>'
    body+='<circle cx="786" cy="222" r="22" fill="#211f1d"/>'
    body+='<g class="moving"><animateTransform attributeName="transform" type="rotate" from="0 786 222" to="360 786 222" dur="26s" repeatCount="indefinite"/><circle cx="786" cy="222" r="143" fill="none" stroke="#f2ede3" stroke-width="1.5" stroke-dasharray="3 12"/></g>'
    body += text(40,458,'A recommendation system that learns how your taste changes.',26,'font-weight="700"')
    body += text(40,494,'Neural collaborative filtering, sequential transformers and adaptive ranking.',22)
    body += text(40,531,'Personalized discovery, watchlists and explainable recommendations.',22)
    body += '<path d="M40 561H960" stroke="#b3aa9a"/>'
    body += text(40,597,'REACT · TYPESCRIPT · FASTAPI · PYTORCH · POSTGRESQL',17,'class="mono"')
    body += text(40,640,'EXPLORE THE SOURCE',19,'font-weight="700" letter-spacing="1"')
    body += text(950,641,'↗',32,'text-anchor="end"')
    save('filmory',body,676,'Filmory — AI movie discovery with neural models, sequential transformers and adaptive ranking. React, TypeScript, FastAPI, PyTorch, PostgreSQL.')

    # A collaborative coding spread with a legible code motif and two contributor cursors.
    body='<rect width="1000" height="420" fill="#dfb741"/>'
    body+=text(40,46,'02 / REALTIME COLLABORATIVE DEVELOPMENT',16,'class="mono" letter-spacing="1"')
    body+=text(37,141,'CodeCollab',82,'font-weight="900" letter-spacing="-4"')
    body+=text(40,188,'Same room. Shared ideas. Better code.',26)
    body+='<rect x="40" y="225" width="920" height="157" fill="#23211e"/>'
    body+='<g font-family="Consolas,monospace" font-size="23"><text x="68" y="269" fill="#dfb741">const <tspan fill="#f2ede3">workspace = {</tspan></text><text x="104" y="308" fill="#f2ede3">code: <tspan fill="#dfb741">"together"</tspan>, ideas: <tspan fill="#dfb741">"shared"</tspan></text><text x="68" y="348" fill="#f2ede3">};</text></g>'
    body+='<path d="M675 302l0 28 9-8 7 14 8-4-7-14 12 0z" fill="#dfb741"/><rect x="718" y="317" width="116" height="31" fill="#dfb741"/>'
    body+=text(730,339,'you + me',17,'class="mono"')
    body+='<g class="moving"><rect x="844" y="249" width="3" height="25" fill="#f2ede3"><animate attributeName="opacity" values="1;1;0;0" dur="1.8s" repeatCount="indefinite"/></rect></g>'
    body+=text(40,466,'A browser workspace for building together, in real time.',26,'font-weight="700"')
    body+=text(40,502,'Shared Monaco editing, whiteboards, terminals and WebRTC communication.',22)
    body+=text(40,539,'Project-aware AI assistance with vector search and persistent state.',22)
    body+='<path d="M40 569H960" stroke="#b3aa9a"/>'
    body+=text(40,605,'NEXT.JS · SOCKET.IO · WEBRTC · PGVECTOR · REDIS',17,'class="mono"')
    body+=text(40,648,'EXPLORE THE SOURCE',19,'font-weight="700" letter-spacing="1"')
    body+=text(950,649,'↗',32,'text-anchor="end"')
    save('codecollab',body,684,'CodeCollab — realtime collaborative developer workspace. Shared editor, whiteboard, terminals, WebRTC and project-aware AI. Next.js, Socket.IO, pgvector, Redis.')

    body = text(40,50,'FROM INTERFACE TO INFRASTRUCTURE',16,'class="mono"')
    rows=[('Web','React · Next.js · Vue · TypeScript'),('Backend','Node.js · Express · Django · FastAPI'),('Data & ML','PostgreSQL · MongoDB · Redis · PyTorch'),('Tools','Git · Linux · Docker · Nginx')]
    for i,(label,tools) in enumerate(rows):
        y=110+i*64
        body+=text(40,y,label,23,'font-weight="700"')
        body+=text(252,y,tools,23)
        body+=f'<path d="M40 {y+21}H960" stroke="#c6bfb2"/>'
    body+=text(40,407,'Beyond the stack',22,'class="serif" font-style="italic"')
    body+=text(40,448,'Competitive programming · System design · Cloud architecture',23)
    body+=text(40,489,'Former DSA teaching assistant at LNMIIT (Jan–Apr 2026)',23)
    save('toolkit',body,525,'Toolkit and background: web development, backend services, data and ML, developer tools, competitive programming, system design, cloud architecture and former DSA teaching assistant at LNMIIT.')

    body='<rect width="1000" height="244" fill="#e6492d"/>'
    body+=text(40,46,'HAVE AN IDEA IN MIND?',16,'class="mono" letter-spacing="1"')
    body+=text(37,137,"Let's build it.",85,'font-weight="900" letter-spacing="-4"')
    body+=text(40,204,'varunrawat5758@gmail.com',25)
    body+=text(952,204,'↗',48,'text-anchor="end"')
    save('footer',body,244,'Have an idea in mind? Let us build it. Email varunrawat5758@gmail.com')

    for name,label in [('portfolio','PORTFOLIO'),('linkedin','LINKEDIN'),('email','EMAIL'),('codeforces','CODEFORCES'),('x','X / TWITTER')]:
        body=text(20,39,label,19,'font-weight="700" letter-spacing="1"')+text(219,40,'↗',24,'text-anchor="end"')+'<path d="M20 52H220" stroke="#23211e" stroke-width="2"/>'
        (ASSETS/f'link-{name}.svg').write_text(frame(body,68,label).replace('width="1000"','width="240"').replace('viewBox="0 0 1000 68"','viewBox="0 0 240 68"'),encoding='utf-8')


if __name__ == '__main__':
    main()
