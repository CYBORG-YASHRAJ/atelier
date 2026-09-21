---
name: web-quality
description: Audit public websites and documentation for technical SEO, semantics, accessibility, responsive behavior, performance, metadata, and crawlability before release.
---

# Web quality

Load for public pages, landing pages, documentation, or explicit SEO work. For
private authenticated app screens, apply accessibility and performance checks
but omit irrelevant crawl/index requirements.

## Build contract

- Give every indexable route a unique, descriptive title and meta description,
  canonical URL, robots policy, one meaningful H1, semantic landmarks, and
  useful internal links. Set document language and viewport.
- Add Open Graph and Twitter metadata with a real share image. Add accurate
  JSON-LD only for entities visibly supported by the page; never invent ratings,
  authors, dates, FAQs, or business data.
- Render primary content and links without requiring client JavaScript where
  the stack supports SSR/static output. Provide sitemap and robots files for
  multi-route public sites. Keep redirects intentional and avoid duplicate URLs.
- Write for humans: answer search intent early, use concrete headings, and keep
  claims supported. Do not keyword-stuff or generate near-duplicate route farms.
- Use responsive images with dimensions, lazy-load below the fold, preload only
  critical assets, keep fonts restrained, and protect Core Web Vitals. Preserve
  keyboard operation, visible focus, labels, contrast, reduced motion, and
  screen-reader structure.

## Verification

When the project contains Atelier's Playwright harness, run `npm run audit:site`.
Set `ATELIER_SITE_URL` to audit a running project; without it the repository's
reference fixture verifies that the harness itself works. Treat passing browser
checks as a floor. Also inspect rendered content, structured data accuracy,
robots/sitemap behavior, network errors, and project-specific performance.

Do not promise rankings. Report observed technical readiness, content gaps, and
measurements separately.
