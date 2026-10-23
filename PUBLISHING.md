# Editorial policy, schedule and link selection

Target: **five substantive, distinct reader-first guides per day for 20 days**, at most **100 articles** total (Oct 23–Nov 11, 2026, America/Vancouver). This is an editorial ceiling, **not** a spam-proof publishing rate or a promise of 100 indexed pages.

We began with five authored guides. A ChatGPT scheduled task has been set up for the 19 subsequent daily batches through the connected GitHub account, and requires GitHub access at run time. As an optional parallel fallback, the GitHub Action can draft articles if the owner adds a valid `OPENAI_API_KEY` Actions secret; that route incurs API costs. Either route must check the same state file and daily quota; future success is not guaranteed. GitHub Pages also needs to be enabled by the owner in repository Settings → Pages → Deploy from main /docs.

## Reader-first policy
- Each page has a distinct informational purpose; no audience-keyword-spun variants or doorway pages.
- Publish guides with a useful process, concrete example, six meaningful actions, and limitations. Code checks page length, section structure and repeated exact copy, but **automated checks cannot verify all facts, originality, helpfulness, or Google compliance**.
- No claims of guaranteed commissions, rankings, visits or earnings, invented statistics, or fabricated personal reviews.
- No scraping, spun content, link wheels, keyword-stuffing or fake urgency.
- Relevant external resources are optional, selectively chosen by article theme, and marked `rel="sponsored noopener noreferrer"` with a conspicuous affiliate disclosure. External links from memory are not presented as independently verified services.
- Semantic headings, unique descriptive titles, mobile-friendly layout, navigation, canonical URLs, robots.txt and XML sitemap.
- A human should periodically review generated pages, remove factual errors and consolidate articles that overlap before relying on them for search traffic.

## Scheduling and limits
GitHub Actions schedule: `17 9 * * *`, timezone `America/Vancouver`. The publisher calculates daily quota from October 23 and stops after November 11 or 100 total articles. Manual reruns cannot bypass the per-day cap. GitHub scheduled runs can be late or skipped.

Website: https://aiautomationtactics.github.io/Ghostpages/ — available after GitHub Pages is enabled.

Reference: https://developers.google.com/search/docs/essentials/spam-policies
