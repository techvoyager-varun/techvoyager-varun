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
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0b1428"/><stop offset="1" stop-color="#131b36"/></linearGradient></defs>
<rect x="1" y="1" width="998" height="{height - 2}" rx="20" fill="url(#bg)" stroke="#283651"/>
<g font-family="Segoe UI,Arial,sans-serif">{body}</g></svg>'''


def render(user, repos, prs, updated):
    values = [
        (user["public_repos"], "PUBLIC REPOSITORIES"),
        (sum(repo["stargazers_count"] for repo in repos if not repo["fork"]), "STARS ON ORIGINAL REPOS"),
        (user["followers"], "GITHUB FOLLOWERS"),
        (prs["total_count"], "MERGED EXTERNAL PRs"),
    ]
    body = '<text x="36" y="35" fill="#a9bad3" font-size="11" letter-spacing="2">PUBLIC GITHUB SNAPSHOT</text>'
    colors = ["#57e4cd", "#79bdff", "#b7a0ff", "#ffc37b"]
    for i, ((value, label), color) in enumerate(zip(values, colors)):
        x = 36 + i * 245
        body += f'<text x="{x}" y="98" font-size="45" font-weight="700" fill="{color}">{value:,}</text>'
        body += f'<text x="{x}" y="129" font-size="10" letter-spacing=".8" fill="#a9bad3">{label}</text>'
        if i < 3:
            body += f'<path d="M{x + 214} 58V138" stroke="#283651"/>'
    body += f'<text x="36" y="173" font-size="11" fill="#a9bad3">Updated {escape(updated)} · Public data only · Fork stars excluded</text>'
    files = {"assets/metrics.svg": frame(body, 198, "Public GitHub stats: " + ", ".join(f"{v} {label.lower()}" for v, label in values))}
    links = []
    for i, pr in enumerate(prs["items"]):
        repo = pr["repository_url"].removeprefix(f"{API}/repos/")
        title = pr["title"]
        lines = textwrap.wrap(title, width=86, max_lines=2, placeholder="…")
        body = f'<circle cx="35" cy="31" r="5" fill="#b7a0ff"/><text x="51" y="36" font-size="12" fill="#b7a0ff">{escape(repo)} · #{pr["number"]}</text>'
        body += '<rect x="865" y="17" width="105" height="27" rx="13" fill="#293049"/><text x="917" y="35" text-anchor="middle" font-size="11" fill="#d5c9ff">✓ MERGED</text>'
        for j, line in enumerate(lines):
            body += f'<text x="35" y="{72 + j * 24}" fill="#e8effa" font-size="18" font-weight="500">{escape(line)}</text>'
        path = f"assets/contribution-{i + 1}.svg"
        files[path] = frame(body, 122, f"Merged: {repo} #{pr['number']} — {title}")
        links.append(f'<a href="{escape(pr["html_url"], quote=True)}"><img src="{path}" width="100%" alt="{escape(repo + ': ' + title + ' (merged)', quote=True)}" /></a>')
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
    readme = replace_section(readme, "METRICS", '<img src="assets/metrics.svg" width="100%" alt="Public repositories, stars, followers and merged external pull requests. Updated daily from GitHub." />')
    for path, content in files.items():
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(f"Updated public metrics and {len(prs['items'])} merged contributions.")


if __name__ == "__main__":
    main()
