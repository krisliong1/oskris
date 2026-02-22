---
name: seo-optimizer
description: >-
  Perform SEO audits and optimization for websites. Use when user says
  "SEO audit", "check SEO", "optimize for search", "improve Google ranking",
  "SEO report", "meta tags", "keyword research", or needs to analyze and
  improve any website's search engine performance. Generates actionable
  SEO reports with specific fixes. Focused on Malaysian market SEO.
---

# SEO Optimizer

Comprehensive SEO audit and optimization guidance for Oskris client websites.

## SEO Audit Workflow

### Step 1: Technical SEO Check
Run these checks (using bash/web tools):
- [ ] Page load speed (target <3s)
- [ ] Mobile-friendly (responsive test)
- [ ] HTTPS enabled
- [ ] XML sitemap exists and submitted
- [ ] robots.txt properly configured
- [ ] No broken links (404s)
- [ ] Proper URL structure (clean, readable)
- [ ] Schema markup (LocalBusiness for Malaysian businesses)
- [ ] Core Web Vitals (LCP <2.5s, FID <100ms, CLS <0.1)

### Step 2: On-Page SEO Audit
For each page check:
- [ ] Title tag (50-60 chars, includes primary keyword)
- [ ] Meta description (150-160 chars, compelling, includes CTA)
- [ ] H1 tag (one per page, includes keyword)
- [ ] H2-H3 hierarchy (logical structure)
- [ ] Image alt tags (descriptive, include keywords)
- [ ] Internal linking (3-5 links per page)
- [ ] Content length (minimum 300 words for key pages)
- [ ] Keyword density (1-2%, not stuffed)

### Step 3: Local SEO (Critical for Malaysian businesses)
- [ ] Google Business Profile claimed and optimized
- [ ] NAP consistency (Name, Address, Phone across web)
- [ ] Local keywords (city + service, e.g., "web design Kuala Lumpur")
- [ ] Malaysian directory listings (Malaysia Business Directory, etc.)
- [ ] Reviews strategy (Google Reviews, Facebook Reviews)

### Step 4: Content Strategy
- Keyword research for client's industry
- Content gap analysis vs. competitors
- Blog post recommendations (topics + target keywords)
- FAQ section suggestions (for featured snippets)

## SEO Report Format

```markdown
# SEO Audit Report — [Client Website]
Date: [Date]
Audited by: Oskris Web Design

## Overall Score: [X]/100

## Critical Issues (Fix Immediately)
🔴 [Issue] — [How to fix] — [Impact: High]

## Warnings (Fix Soon)
🟡 [Issue] — [How to fix] — [Impact: Medium]

## Passed ✅
🟢 [What's working well]

## Recommendations
1. [Priority action with expected result]
2. [Next action]
3. [...]

## Keyword Opportunities
| Keyword | Monthly Searches | Difficulty | Current Rank |
|---------|-----------------|------------|-------------|
| [keyword] | [volume] | [easy/med/hard] | [rank or N/A] |
```

## Malaysian SEO Specifics
- Target bilingual keywords (EN + BM)
- Example: "web design Malaysia" AND "reka bentuk laman web Malaysia"
- Google.com.my specific optimizations
- Malaysian hosting = faster load times for local visitors
- Include Malaysian phone format (+60) in structured data
- Hreflang tags for multilingual sites

## Quick SEO Fix Scripts

### Generate Meta Tags
For any page, generate optimized:
```html
<title>[Primary Keyword] | [Brand] — [Value Proposition]</title>
<meta name="description" content="[Compelling 155-char description with CTA]">
<meta name="keywords" content="[5-8 relevant keywords]">
<link rel="canonical" href="[URL]">
```

### Generate Schema Markup
For local businesses:
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Business Name]",
  "address": { "@type": "PostalAddress", "addressLocality": "[City]", "addressCountry": "MY" },
  "telephone": "+60[number]",
  "url": "[website]"
}
```

## Competitor Analysis
When requested, analyze 3-5 competitor websites:
- Domain authority comparison
- Keyword overlap and gaps
- Backlink profile summary
- Content strategy differences
- Technical SEO comparison
