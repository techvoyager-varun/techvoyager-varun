# Profile maintenance

The profile README uses original SVG assets stored in `assets/`. The hero has a slow orbital animation and project cards have subtle moving indicators. Each asset has readable static artwork; the motion layers are hidden when the browser honors `prefers-reduced-motion` for SVG images. GitHub image caching can delay visible updates.

`scripts/refresh_profile.py` uses Python's standard library to collect public GitHub data. It updates four metrics and the six most recently updated merged pull requests authored by techvoyager-varun in other owners' public repositories. Stars count original public repositories only. It does not read or publish private repositories, private contribution counts or credentials.

The workflow runs daily at 02:17 UTC (07:47 India time), on relevant changes to `main`, and on manual dispatch. It uses the built-in `GITHUB_TOKEN`; no personal access token or third-party statistics service is needed. API errors fail the run before changing the last snapshot. Scheduled runs can be delayed or disabled by GitHub after extended repository inactivity; check the linked Actions status if data looks stale.

Run manually from the repository root:

```sh
python scripts/refresh_profile.py
```

Optional: set `GH_TOKEN` in your environment to use authenticated API limits. Never commit a token. The Actions workflow needs `contents: write` to commit generated snapshots.

The bio, contact links, toolkit, featured project selection and their descriptions are curated. Update them when those details change; automation cannot verify education, availability or skill proficiency. Project cards link to public source repositories, not unverified deployment URLs. The original root SVG files remain available but are no longer embedded in the README.
