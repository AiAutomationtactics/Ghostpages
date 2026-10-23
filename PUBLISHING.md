# Editorial publishing policy

This educational website must serve human readers first. Publishing 1,200 thin, mechanically generated articles can violate Google's scaled content abuse policy. The schedule is therefore a *maximum*, not a promise. If the generator cannot make five genuinely different, complete, useful pages, it stops without publishing.

- Schedule: every 2 hours UTC, for at most 20 days after the recorded project start.
- Maximum: 240 batches × 5 = 1,200 pages, including the five starter pages.
- An optional paid OpenAI API key is required for ongoing original content drafting. GitHub Actions does not provide unlimited free AI generation.
- Generated articles have unique topic/intent combinations, a practical worked example, a checklist, a comparison or decision framework, and non-duplicative descriptions.
- No keyword stuffing, invented income claims, fabricated testimonials, guaranteed earnings, fake reviews, or misleading attribution.
- Affiliate links are disclosed and `rel="sponsored noopener noreferrer"` is used.
- Pages include titles, descriptions, semantic HTML, canonical URLs, structured Article JSON-LD, internal navigation and a sitemap.
- Human fact review is still needed, especially when platforms change rules or fees. The workflow performs basic automated quality checks but cannot certify Google's assessment or truth of generated claims.
- GitHub Pages: Settings → Pages → Deploy from branch `main` / `/docs`. The configured base URL is `https://aiautomationtactics.github.io/Ghostpages/`.

**Activation:** Add repository secret `OPENAI_API_KEY`, then optionally run the workflow manually. The script will not auto-publish if missing the key or if validation fails. You can disable the schedule by deleting the workflow. GitHub scheduled jobs can run late or be skipped.
