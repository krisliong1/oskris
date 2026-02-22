---
name: site-deployer
description: >-
  Deploy websites to VPS or Hostinger hosting. Use when user says "deploy site",
  "launch website", "upload to server", "go live", "publish website", "DNS setup",
  "SSL setup", "configure domain", or needs to deploy any web project to production.
  Handles file upload, nginx config, DNS, SSL certificates, and post-launch checks.
  Supports both VPS (76.13.191.45) and shared hosting (76.13.178.156).
---

# Site Deployer

One-click website deployment pipeline for Oskris projects.

## Deployment Targets

### Target A: VPS (76.13.191.45)
- Full control, custom nginx config
- Best for: Node.js apps, custom setups, multiple sites
- SSH: `root@76.13.191.45`

### Target B: Shared Hosting (76.13.178.156)
- Hostinger shared hosting with cPanel
- Best for: Static sites, WordPress, simple PHP
- SSH: `ssh -p 65002 u212717065@76.13.178.156`

## Deployment Workflow

### Step 1: Pre-Deploy Checks
Before deploying, verify:
- [ ] All pages working locally
- [ ] Images optimized (WebP, compressed)
- [ ] Links not broken
- [ ] Meta tags set for all pages
- [ ] favicon.ico present
- [ ] robots.txt configured
- [ ] sitemap.xml generated
- [ ] Mobile responsive tested
- [ ] Forms working
- [ ] Analytics code added

### Step 2: File Upload
**To VPS:**
```bash
# Create site directory
ssh root@76.13.191.45 "mkdir -p /var/www/[domain]"

# Upload via SCP or rsync
rsync -avz --delete ./build/ root@76.13.191.45:/var/www/[domain]/

# Or via Git
ssh root@76.13.191.45 "cd /var/www/[domain] && git pull"
```

**To Shared Hosting:**
```bash
scp -P 65002 -r ./build/* u212717065@76.13.178.156:~/domains/[domain]/public_html/
```

### Step 3: Nginx Configuration (VPS only)
Generate nginx config for the site:
```nginx
server {
    listen 80;
    server_name [domain] www.[domain];
    root /var/www/[domain];
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Caching
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
}
```

### Step 4: SSL Certificate
```bash
# Install certbot if not present
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d [domain] -d www.[domain] --non-interactive --agree-tos -m official@oskris.com

# Verify auto-renewal
certbot renew --dry-run
```

### Step 5: DNS Configuration
Via Hostinger API or panel:
- A record: `[domain]` → VPS IP (76.13.191.45)
- A record: `www.[domain]` → VPS IP
- Wait for propagation (5-30 minutes)

Check: `dig [domain] +short`

### Step 6: Post-Launch Verification
After deployment, check:
- [ ] Site accessible via domain
- [ ] HTTPS working (redirect HTTP → HTTPS)
- [ ] All pages loading correctly
- [ ] Forms submitting properly
- [ ] Mobile version working
- [ ] Speed test (Google PageSpeed)
- [ ] SSL grade (ssllabs.com)

Report format:
```
🚀 Deployment Complete!
━━━━━━━━━━━━━━━━━━
🌐 URL: https://[domain]
🔒 SSL: ✅ Active
📱 Mobile: ✅ Responsive
⚡ Speed: [PageSpeed score]/100
📊 Status: LIVE
```

## Rollback Plan
If issues found after deployment:
1. Keep previous version backup
2. Quick rollback: `mv /var/www/[domain] /var/www/[domain].broken && mv /var/www/[domain].backup /var/www/[domain]`
3. Investigate issue
4. Fix and redeploy
