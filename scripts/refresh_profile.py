"""Refresh public profile metrics and merged external PRs using only stdlib."""

import json
import os
import re
import textwrap
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "techvoyager-varun"
API = "https://api.github.com"


def fetch(path):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "techvoyager-profile-refresh",
    }
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(f"{API}{path}", headers=headers), timeout=30) as response:
        return json.load(response)


def collect():
    user = fetch(f"/users/{USERNAME}")
    repos = []
    page = 1
    while True:
        batch = fetch(f"/users/{USERNAME}/repos?per_page=100&type=owner&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    params = urlencode({
        "q": f"is:pr is:merged is:public author:{USERNAME} -user:{USERNAME}",
        "sort": "updated", "order": "desc", "per_page": 6,
    })
    prs = fetch(f"/search/issues?{params}")
    if prs.get("incomplete_results"):
        raise ValueError("GitHub returned incomplete PR search results; retaining previous data")
    return user, repos, prs


def frame(body, height, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<rect width="1000" height="{height}" fill="#f2ede3"/>
<g font-family="Arial,Helvetica,sans-serif">{body}</g></svg>'''


def render(user, repos, prs, updated):
    values = [
        (user["public_repos"], "PUBLIC REPOSITORIES"),
        (sum(repo["stargazers_count"] for repo in repos if not repo["fork"]), "STARS ON ORIGINAL REPOS"),
        (user["followers"], "GITHUB FOLLOWERS"),
        (prs["total_count"], "MERGED EXTERNAL PRs"),
    ]
    body = ''
    for i, (value, label) in enumerate(values):
        x = 40 + (i % 2) * 480
        y = 98 + (i // 2) * 165
        body += f'<text x="{x}" y="{y}" font-size="84" font-weight="900" fill="#e6492d" letter-spacing="-3">{value:,}</text>'
        body += f'<text x="{x}" y="{y + 37}" font-size="18" fill="#23211e">{label}</text>'
    body += '<path d="M40 156H960M40 321H960" stroke="#b3aa9a"/>'
    body += f'<text x="40" y="358" font-size="16" fill="#524d45">Updated {escape(updated)} · Public data · Fork stars excluded</text>'
    files = {"assets/metrics.svg": frame(body, 387, "Public GitHub stats: " + ", ".join(f"{v} {label.lower()}" for v, label in values))}
    mobile = ''
    for i, (value, label) in enumerate(values):
        x = 24 + (i % 2) * 288
        y = 84 + (i // 2) * 159
        mobile += f'<text x="{x}" y="{y}" font-size="70" font-weight="900" fill="#e6492d">{value:,}</text>'
        for j, line in enumerate(textwrap.wrap(label, width=23)):
            mobile += f'<text x="{x}" y="{y + 34 + j * 24}" font-size="19" fill="#23211e">{line}</text>'
    mobile += f'<text x="24" y="340" font-size="18" fill="#524d45">Updated {escape(updated)}</text><text x="24" y="369" font-size="18" fill="#524d45">Public data · Fork stars excluded</text>'
    files['assets/metrics-mobile.svg'] = frame(mobile, 395, 'Public GitHub metrics').replace('width="1000"', 'width="600"').replace('viewBox="0 0 1000 395"', 'viewBox="0 0 600 395"')
    links = []
    for i, pr in enumerate(prs["items"]):
        repo = pr["repository_url"].removeprefix(f"{API}/repos/")
        title = pr["title"]
        lines = textwrap.wrap(title, width=77, max_lines=2, placeholder="…")
        body = f'<text x="40" y="33" font-size="18" fill="#e6492d" font-weight="700">{escape(repo)} / #{pr["number"]}</text>'
        body += '<text x="960" y="33" text-anchor="end" font-size="16" fill="#524d45">MERGED ↗</text>'
        for j, line in enumerate(lines):
            body += f'<text x="40" y="{67 + j * 26}" fill="#23211e" font-size="22">{escape(line)}</text>'
        body += '<path d="M40 113H960" stroke="#c6bfb2"/>'
        path = f"assets/contribution-{i + 1}.svg"
        files[path] = frame(body, 122, f"Merged: {repo} #{pr['number']} — {title}")
        mobile_lines = textwrap.wrap(title, width=43, max_lines=4, placeholder='…')
        mobile = f'<text x="24" y="31" font-size="21" fill="#e6492d" font-weight="700">{escape(repo)} / #{pr["number"]}</text>'
        for j, line in enumerate(mobile_lines):
            mobile += f'<text x="24" y="{70 + j * 32}" font-size="25" fill="#23211e">{escape(line)}</text>'
        height = 115 + len(mobile_lines) * 32
        mobile += f'<text x="24" y="{height - 22}" font-size="18" fill="#524d45">MERGED ↗</text>'
        mobile_path = f'assets/contribution-{i + 1}-mobile.svg'
        files[mobile_path] = frame(mobile, height, title).replace('width="1000"', 'width="600"').replace(f'viewBox="0 0 1000 {height}"', f'viewBox="0 0 600 {height}"')
        links.append(f'<a href="{escape(pr["html_url"], quote=True)}"><picture><source media="(max-width: 600px)" srcset="{mobile_path}" /><img src="{path}" width="100%" alt="{escape(repo + ': ' + title + ' (merged)', quote=True)}" /></picture></a>')
    if not links:
        links = ["<p align=\"center\">New contributions will appear here after they are merged.</p>"]
    return files, "\n".join(links)


def replace_section(readme, marker, content):
    pattern = rf"<!-- {marker}:START -->.*?<!-- {marker}:END -->"
    replacement = f"<!-- {marker}:START -->\n{content}\n<!-- {marker}:END -->"
    result, count = re.subn(pattern, lambda _: replacement, readme, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"Expected exactly one {marker} section, found {count}")
    return result


def main():
    # Collect and render everything before writing, so API failures preserve the last snapshot.
    user, repos, prs = collect()
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d UTC")
    files, contributions = render(user, repos, prs, updated)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = replace_section(readme, "CONTRIBUTIONS", contributions)
    readme = replace_section(readme, "METRICS", '<picture><source media="(max-width: 600px)" srcset="assets/metrics-mobile.svg" /><img src="assets/metrics.svg" width="100%" alt="Public repositories, stars, followers and merged external pull requests. Updated daily from GitHub." /></picture>')
    for path, content in files.items():
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(f"Updated public metrics and {len(prs['items'])} merged contributions.")


if __name__ == "__main__":
    main()
