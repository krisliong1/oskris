---
name: site-health-agent
description: >-
  Comprehensive website health monitoring agent. Use when user says "check website",
  "site health", "website audit", "is [site] working", "performance check",
  "security scan", "monitor sites", or needs a full health assessment of any website.
  Coordinates vps-manager, seo-optimizer, and site-deployer skills to perform
  complete website health checks including uptime, performance, SEO, security,
  and content freshness. Can check any URL, with focus on Oskris client websites.
---

# Site Health Agent — Website Monitoring Orchestrator

Coordinated health checks across multiple dimensions for any website.

## Agent Architecture

```
Site Health Agent (Coordinator)
    ├── Performance Check → [site-deployer] for infrastructure
    ├── SEO Health → [seo-optimizer] for search optimization
    ├── Server Health → [vps-manager] for server-side monitoring
    ├── Security Scan → Built-in security checks
    └── Content Review → Freshness and accuracy check
```

## Health Check Dimensions

### 1. Uptime & Availability
```bash
# Quick check
curl -o /dev/null -s -w "%{http_code} %{time_total}s" https://[domain]

# SSL check
echo | openssl s_client -servername [domain] -connect [domain]:443 2>/dev/null | openssl x509 -noout -dates

# DNS resolution
dig [domain] +short
```

### 2. Performance
Check via web tools:
- Page load time (target: <3s)
- First Contentful Paint (target: <1.8s)
- Largest Contentful Paint (target: <2.5s)
- Total page size (target: <3MB)
- Number of requests (target: <50)
- Image optimization (WebP usage)
- Caching headers set

### 3. SEO Health
Delegate to `seo-optimizer`:
- Meta tags present and optimized
- Sitemap.xml accessible
- robots.txt correct
- Mobile-friendly
- Schema markup
- No broken links

### 4. Security
- SSL certificate valid and not expiring soon
- Security headers present (HSTS, CSP, X-Frame-Options)
- No mixed content (HTTP resources on HTTPS page)
- Server software not exposed
- No sensitive files accessible (.env, .git, etc.)

### 5. Content Freshness
- Copyright year updated
- Contact info accurate
- Links still working
- No placeholder content
- Images loading correctly

## Health Report Format

```
🏥 Website Health Report
━━━━━━━━━━━━━━━━━━━━━
🌐 Site: [domain]
📅 Checked: [date/time]
⭐ Overall Score: [X]/100

📊 Performance: [score]/100
  ⚡ Load time: [X]s [✅/⚠️/🔴]
  📦 Page size: [X]MB [✅/⚠️/🔴]
  🖼️ Images optimized: [yes/no]

🔍 SEO: [score]/100
  📝 Meta tags: [✅/❌]
  🗺️ Sitemap: [✅/❌]
  📱 Mobile: [✅/❌]

🔒 Security: [score]/100
  🔐 SSL: [valid until date] [✅/⚠️]
  🛡️ Headers: [X/6 present]
  🚫 Vulnerabilities: [none/list]

📋 Content: [score]/100
  🔗 Broken links: [count]
  📅 Last updated: [date]
  ✏️ Issues: [list or "None"]

🔧 Action Items:
  1. [Most critical fix]
  2. [Second priority]
  3. [Third priority]
```

## Monitored Sites
Track health for all Oskris sites:
- oskris.com (main)
- websitedesign.oskris.com
- kkh.oskris.com
- Client sites (as added)

## Automated Alerts
Flag issues when:
- 🔴 Site returns non-200 status
- 🔴 SSL expires within 14 days
- 🟡 Load time > 5 seconds
- 🟡 Disk usage > 80% on VPS
- 🟡 New security vulnerability found
- 🟡 Broken links detected

## Quick Commands
- "Check all sites" → Run health check on all monitored sites
- "Check [domain]" → Full health check on specific site
- "Quick ping [domain]" → Just uptime + response time
- "SSL status" → Check all SSL certificates
- "What needs fixing?" → Show all sites with issues
