---
name: vps-manager
description: >-
  Manage and monitor VPS server operations. Use when user says "check server",
  "server status", "VPS health", "restart service", "install package",
  "server maintenance", "disk space", "memory usage", "update server",
  or needs any server administration task on the Hostinger VPS (76.13.191.45).
  Handles monitoring, maintenance, security, and service management.
---

# VPS Manager

Automated server management for Oskris VPS (76.13.191.45, Ubuntu, 2-core, 8GB RAM).

## Quick Commands

### Health Check
When asked for server status, check ALL of these:
```bash
# System info
uname -a && uptime

# Resource usage
free -h && df -h

# CPU load
top -bn1 | head -20

# Running services
systemctl list-units --type=service --state=running | head -20

# Network
ss -tulnp | head -20

# Recent errors
journalctl --since "1 hour ago" --priority=err --no-pager | tail -20
```

Report format:
```
🖥️ VPS Health Report
━━━━━━━━━━━━━━━━━━
💻 OS: [version]
⏱️ Uptime: [days/hours]
🔄 CPU: [load average]
💾 RAM: [used/total] ([%])
💿 Disk: [used/total] ([%])
🌐 Network: [active connections]
🔧 Services: [running count]
⚠️ Alerts: [issues or "None"]
```

### Service Management
Common services to manage:
- `nginx` — Web server
- `pm2` — Node.js process manager
- `oskris-agent` — Telegram bot service
- `mysql` or `mariadb` — Database
- `fail2ban` — Security
- `certbot` — SSL certificates

### Security Checklist
Periodic security review:
- [ ] System updates available? → `apt update && apt list --upgradable`
- [ ] Fail2ban active? → `systemctl status fail2ban`
- [ ] SSH key-only auth? → Check `/etc/ssh/sshd_config`
- [ ] Firewall rules correct? → `ufw status verbose`
- [ ] No unauthorized users? → `cat /etc/passwd | grep -v nologin`
- [ ] SSL certificates valid? → `certbot certificates`
- [ ] Disk usage under 80%? → `df -h`
- [ ] No suspicious processes? → `ps aux --sort=-%cpu | head -10`

### Automated Maintenance Tasks
When user says "maintain server":
1. Update system packages
2. Clean old logs and caches
3. Check disk space
4. Verify all services running
5. Check SSL expiry dates
6. Review fail2ban blocked IPs
7. Report summary

## Connection Info
- SSH: `ssh root@76.13.191.45` (password in credentials)
- Hosting: `ssh -p 65002 u212717065@76.13.178.156`

## Alert Thresholds
- 🟢 Normal: CPU <70%, RAM <70%, Disk <70%
- 🟡 Warning: CPU 70-85%, RAM 70-85%, Disk 70-85%
- 🔴 Critical: CPU >85%, RAM >85%, Disk >85%

## Troubleshooting
### Website Down
1. Check nginx: `systemctl status nginx`
2. Check DNS: `dig [domain]`
3. Check application: `pm2 status` or check logs
4. Check resources: `free -h && df -h`
5. Check firewall: `ufw status`

### High Resource Usage
1. Find culprit: `top -bn1 | head -20`
2. Check for attacks: `fail2ban-client status`
3. Review access logs: `tail -100 /var/log/nginx/access.log`
4. Clear caches if needed
