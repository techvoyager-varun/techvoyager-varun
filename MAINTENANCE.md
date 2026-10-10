# Profile maintenance

The profile README uses original editorial SVG assets stored in `assets/`: warm paper, vermilion, charcoal and ochre; oversized typography; square project spreads. Only Filmory and CodeCollab are featured. The hero has a slowly moving dotted rosette, Filmory has a moving film-reel ring, and CodeCollab has a blinking cursor. Static artwork remains visible with reduced motion. GitHub image caching can delay updates.

Regenerate curated artwork with `python scripts/build_artwork.py`, then refresh public data with `python scripts/refresh_profile.py`.

Design research: [Awesome GitHub Profile README](https://github.com/abhisheknaiidu/awesome-github-profile-readme), [Creative Profile README](https://github.com/coderjojo/creative-profile-readme), [Caneco](https://github.com/caneco) and [Pouya Saadeghi](https://github.com/saadeghi/saadeghi). These informed the emphasis on individual identity and readable hierarchy; no third-party artwork or template was copied. Project artwork is illustrative, not a screenshot of the applications.

`scripts/refresh_profile.py` uses Python's standard library to collect public GitHub data. It updates four metrics and the six most recently updated merged pull requests authored by techvoyager-varun in other owners' public repositories. Stars count original public repositories only. It does not read or publish private repositories, private contribution counts or credentials.

The workflow runs daily at 02:17 UTC (07:47 India time), on relevant changes to `main`, and on manual dispatch. It uses the built-in `GITHUB_TOKEN`; no personal access token or third-party statistics service is needed. API errors fail the run before changing the last snapshot. Scheduled runs can be delayed or disabled by GitHub after extended repository inactivity; check the linked Actions status if data looks stale.

Run manually from the repository root:

```sh
python scripts/refresh_profile.py
```

Optional: set `GH_TOKEN` in your environment to use authenticated API limits. Never commit a token. The Actions workflow needs `contents: write` to commit generated snapshots.

The bio, contact links, toolkit, featured project selection and their descriptions are curated. Update them when those details change; automation cannot verify education, availability or skill proficiency. Project cards link to public source repositories, not unverified deployment URLs. The original root SVG files remain available but are no longer embedded in the README.
