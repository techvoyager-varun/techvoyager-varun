# Profile maintenance

The profile uses native GitHub Markdown sections and flat square technology/social badges, inspired by https://github.com/apoorvdarshan. All biography and project descriptions belong to Varun; only Filmory and CodeCollab are featured.

The scheduled GitHub workflow runs daily at 02:17 UTC and can also be started manually. It updates public repository, original repository star, follower, and merged external pull request counts, plus the latest 100 merged external pull requests grouped by repository. Search excludes contributions to Varun's own repositories. API failures and incomplete results preserve the prior snapshot. Biography, technologies, and links are maintained manually.

Run `python scripts/refresh_profile.py` from the repository root. GH_TOKEN is optional locally and supplied by the workflow. No third-party stats service is needed. Shields.io serves the static badges; the small cursor animation is a repository SVG and respects reduced motion.
