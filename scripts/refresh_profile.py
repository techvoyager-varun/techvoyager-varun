"""Refresh public profile metrics and merged external PRs using only stdlib."""

import json
import os
import re
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
        "sort": "updated", "order": "desc", "per_page": 100,
    })
    prs = fetch(f"/search/issues?{params}")
    if prs.get("incomplete_results"):
        raise ValueError("GitHub returned incomplete PR search results; retaining previous data")
    return user, repos, prs


def render(user, repos, prs, updated):
    groups = {}
    for pr in prs["items"]:
        repo = pr["repository_url"].removeprefix(f"{API}/repos/")
        groups.setdefault(repo, []).append(pr)
    lines = [f"**{prs['total_count']} merged pull requests** in other public repositories.", ""]
    for repo, items in groups.items():
        lines.append(f"### [{repo}](https://github.com/{repo})")
        lines.append("")
        for pr in items:
            title = escape(pr["title"])
            lines.append(f'<li><a href="{escape(pr["html_url"], quote=True)}">#{pr["number"]}</a> — {title}</li>')
        first = len(lines) - len(items)
        lines.insert(first, "<ul>")
        lines.extend(["</ul>", ""])
    stars = sum(repo["stargazers_count"] for repo in repos if not repo["fork"])
    metrics = f"**{user['public_repos']} public repositories** · **{stars} stars on original repositories** · **{user['followers']} followers** · **{prs['total_count']} merged external PRs**\n\n<sub>Public GitHub data · Updated {updated} · Fork stars excluded</sub>"
    return metrics, "\n".join(lines)


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
    metrics, contributions = render(user, repos, prs, updated)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = replace_section(readme, "CONTRIBUTIONS", contributions)
    readme = replace_section(readme, "METRICS", metrics)
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(f"Updated public metrics and {len(prs['items'])} merged contributions.")


if __name__ == "__main__":
    main()
