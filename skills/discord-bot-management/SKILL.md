# Discord Bot Management

**Skill Level**: Intermediate  
**Category**: Communication / API Integration  
**Maintained by**: Discord Research Specialist

---

## Overview

Comprehensive guide for managing Discord bots in OpenClaw, covering OAuth2 authorization, security, configuration, and troubleshooting.

## Quick Reference

### Key Concepts

**Client ID** (Public)
- Unique identifier for your Discord application
- Safe to share in OAuth URLs
- Format: 18-19 digit snowflake (e.g., `1474259579729739949`)

**Bot Token** (Secret!)
- Format: `BASE64(client_id).TIMESTAMP.HMAC`
- Never commit to Git or share publicly
- Full access to Discord API with bot's permissions

**Client Secret** (Secret!)
- Used for OAuth2 flows
- Required for token exchange
- Different from Bot Token

### Configuration Locations

```bash
# OpenClaw config
~/.openclaw/openclaw.json

# Discord Developer Portal
https://discord.com/developers/applications

# OpenClaw docs
/opt/homebrew/lib/node_modules/openclaw/docs/channels/discord.md
```

---

## Discord Bot Setup

### 1. Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**
3. Name your application
4. Navigate to **Bot** tab
5. Click **Add Bot**
6. Copy **Bot Token** (you'll only see it once!)

### 2. Enable Required Intents

In Developer Portal → **Bot** → **Privileged Gateway Intents**:

**Required**:
- ✅ **Message Content Intent** - Read message content
- ✅ **Server Members Intent** - User/member resolution

**Optional**:
- ⚪ **Presence Intent** - Only if you need presence updates

⚠️ **Restart gateway after changing intents!**

### 3. Generate OAuth2 URL

**For Bot Authorization** (add to servers):

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=PERMISSIONS_INTEGER
```

**Permission Calculator**: https://discordapi.com/permissions.html

**Common Permissions**:
- `2048` - Send Messages
- `3072` - Send Messages + Embed Links
- `68608` - Send Messages + Embed Links + Attach Files + Read Message History

**For User OAuth** (login/data access):

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=ENCODED_REDIRECT_URI&response_type=code&scope=identify%20email
```

---

## OpenClaw Configuration

### Basic Setup

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN"
    }
  }
}
```

**Environment Variable Alternative**:

```bash
export DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN"
```

### Access Control

**Open Policy** (anyone can message):

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "...",
      "groupPolicy": "open",
      "allowFrom": ["*"]
    }
  }
}
```

**Allowlist Policy** (specific guilds/users):

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "...",
      "groupPolicy": "allowlist",
      "guilds": {
        "GUILD_ID": {
          "requireMention": true,
          "users": ["USER_ID_1", "USER_ID_2"],
          "roles": ["ROLE_ID"],
          "channels": {
            "CHANNEL_ID": { "allow": true },
            "general": { "allow": true, "requireMention": false }
          }
        }
      }
    }
  }
}
```

**DM Policy**:

```json
{
  "channels": {
    "discord": {
      "dmPolicy": "pairing",  // pairing, allowlist, open, disabled
      "dmHistoryLimit": 20
    }
  }
}
```

### Advanced Features

**Reply Threading**:

```json
{
  "channels": {
    "discord": {
      "replyToMode": "first"  // off, first, all
    }
  }
}
```

**Presence/Status**:

```json
{
  "channels": {
    "discord": {
      "status": "online",  // online, idle, dnd, invisible
      "activity": "with AI",
      "activityType": 0  // 0=Playing, 1=Streaming, 2=Listening, 3=Watching, 4=Custom
    }
  }
}
```

**Exec Approvals**:

```json
{
  "channels": {
    "discord": {
      "execApprovals": {
        "enabled": true,
        "approvers": ["USER_ID"],
        "target": "dm"  // dm, channel, both
      }
    }
  }
}
```

---

## OAuth2 Authorization Flows

### 1. Bot Authorization Flow

**Simplest method for adding bots to servers.**

**URL Template**:
```
https://discord.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=PERMISSIONS&guild_id=GUILD_ID&disable_guild_select=false
```

**Parameters**:
- `client_id` - Your application's client ID
- `scope` - Must include `bot`
- `permissions` - Integer from permission calculator
- `guild_id` (optional) - Pre-select a server
- `disable_guild_select` (optional) - Lock to pre-selected server

**Flow**:
1. User clicks authorization URL
2. User selects server (if they have admin perms)
3. User approves permissions
4. Bot is added to server
5. ✅ Done! No token exchange needed

### 2. Authorization Code Grant

**Full OAuth2 flow for user data access.**

**Step 1: Authorization URL**:
```
https://discord.com/oauth2/authorize?response_type=code&client_id=CLIENT_ID&scope=identify%20guilds&redirect_uri=REDIRECT_URI&state=RANDOM_STATE
```

**Step 2: User Approves** → Redirected to:
```
https://yourapp.com/callback?code=AUTHORIZATION_CODE&state=RANDOM_STATE
```

**Step 3: Exchange Code for Token**:
```bash
curl -X POST https://discord.com/api/v10/oauth2/token \
  -u "CLIENT_ID:CLIENT_SECRET" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=CODE&redirect_uri=REDIRECT_URI"
```

**Response**:
```json
{
  "access_token": "ACCESS_TOKEN",
  "token_type": "Bearer",
  "expires_in": 604800,
  "refresh_token": "REFRESH_TOKEN",
  "scope": "identify guilds"
}
```

**Step 4: Use Access Token**:
```bash
curl https://discord.com/api/v10/users/@me \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### 3. Implicit Grant

**Browser-only flow (no server-side code).**

**URL**:
```
https://discord.com/oauth2/authorize?response_type=token&client_id=CLIENT_ID&scope=identify&redirect_uri=REDIRECT_URI
```

**Redirect** (note the `#` fragment):
```
https://yourapp.com/#access_token=TOKEN&token_type=Bearer&expires_in=604800&scope=identify
```

⚠️ **Limitations**:
- No refresh token
- Token in URL fragment (less secure)
- User must re-authorize when token expires

### 4. Client Credentials Grant

**Bot owner testing only.**

```bash
curl -X POST https://discord.com/api/v10/oauth2/token \
  -u "CLIENT_ID:CLIENT_SECRET" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&scope=identify"
```

---

## Event Webhooks Configuration

### What Are Event Webhooks?

Discord Event Webhooks are **HTTP endpoints** that receive Discord events (messages, joins, etc.) via POST requests, as an alternative to the Gateway WebSocket connection.

**Key Differences**:

| Feature | Gateway (OpenClaw) | Event Webhooks |
|---------|-------------------|----------------|
| Protocol | WebSocket | HTTP POST |
| Connection | Persistent | Per-event push |
| Use Case | Real-time bot interaction | Event forwarding to services |
| Required | For bot functionality | Optional |

⚠️ **Important**: Event Webhooks are **not required** for OpenClaw to work. OpenClaw uses Gateway connections.

### When to Use Event Webhooks

**Use When**:
- ✅ Forwarding Discord events to external services (logging, analytics)
- ✅ Distributed architecture (multiple services processing different events)
- ✅ Backup event stream
- ✅ Integration with non-bot systems

**Don't Use When**:
- ❌ Just want your bot to receive/send messages (Gateway is enough)
- ❌ Uncertain why you need it (you probably don't)
- ❌ First time setting up a Discord bot

### Configuration Steps

#### 1. Create Webhook Endpoint

**Quick Test with Webhook.site** (temporary):

```bash
# 1. Visit https://webhook.site
# 2. Copy the generated URL (e.g., https://webhook.site/abc-123)
# 3. Use this URL in Discord Developer Portal
# 4. Webhook.site auto-responds to Discord's verification
```

**Production Setup** (Node.js + Express):

```javascript
// webhook-server.js
const express = require('express');
const nacl = require('tweetnacl');

const app = express();
const PORT = 3010;

// Get from Discord Developer Portal → General Information → PUBLIC KEY
const PUBLIC_KEY = process.env.DISCORD_PUBLIC_KEY;

// Parse raw body for signature verification
app.use(express.json({
  verify: (req, res, buf) => {
    req.rawBody = buf.toString('utf-8');
  }
}));

// Verify Discord request signature
function verifyDiscordRequest(req) {
  const signature = req.get('X-Signature-Ed25519');
  const timestamp = req.get('X-Signature-Timestamp');
  const body = req.rawBody;

  if (!signature || !timestamp || !body) {
    return false;
  }

  // Check timestamp (prevent replay attacks)
  const requestTime = parseInt(timestamp) * 1000;
  const now = Date.now();
  if (Math.abs(now - requestTime) > 5 * 60 * 1000) { // 5 minutes
    console.error('Request timestamp too old');
    return false;
  }

  // Verify Ed25519 signature
  try {
    const isValid = nacl.sign.detached.verify(
      Buffer.from(timestamp + body),
      Buffer.from(signature, 'hex'),
      Buffer.from(PUBLIC_KEY, 'hex')
    );
    return isValid;
  } catch (err) {
    console.error('Signature verification failed:', err);
    return false;
  }
}

// Webhook endpoint
app.post('/discord/webhook', (req, res) => {
  // Verify request is from Discord
  if (!verifyDiscordRequest(req)) {
    console.error('❌ Invalid signature from:', req.ip);
    return res.status(401).send('Invalid signature');
  }

  const { type, data } = req.body;

  // Type 0 = PING (verification request)
  if (type === 0) {
    console.log('✅ Discord verification PING received');
    return res.json({ type: 1 }); // Return PONG
  }

  // Handle other event types
  console.log('📩 Discord event:', { type, data });
  
  // Process event asynchronously (respond quickly)
  res.status(200).send();
  
  setImmediate(() => {
    // Your event handling logic here
    processDiscordEvent(type, data);
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Discord webhook server running on port ${PORT}`);
});

async function processDiscordEvent(type, data) {
  // TODO: Implement your event handling
  console.log('Processing event:', type);
}
```

**Install Dependencies**:
```bash
npm install express tweetnacl
```

**Run with PM2**:
```bash
pm2 start webhook-server.js --name discord-webhook
pm2 save
pm2 startup
```

#### 2. Configure Nginx (if using reverse proxy)

```nginx
# /etc/nginx/sites-available/your-domain.com

location /discord/webhook {
    proxy_pass http://localhost:3010;
    proxy_http_version 1.1;
    
    # Preserve headers for signature verification
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Host $host;
    proxy_pass_request_headers on;
    
    # Timeout settings
    proxy_connect_timeout 3s;
    proxy_send_timeout 3s;
    proxy_read_timeout 3s;
}
```

```bash
sudo nginx -t
sudo systemctl reload nginx
```

#### 3. Configure in Discord Developer Portal

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Navigate to **General Information** or **Event Subscriptions**
4. Find **Event Webhooks URL** field
5. Enter your endpoint: `https://your-domain.com/discord/webhook`
6. Click **Save Changes**
7. Discord will send a verification request
8. If your endpoint responds correctly, you'll see ✅ "Verified"

#### 4. Get Public Key

**Location**: Developer Portal → General Information → **PUBLIC KEY**

**Add to Environment**:
```bash
export DISCORD_PUBLIC_KEY="your_public_key_here"

# Or in .env file:
echo "DISCORD_PUBLIC_KEY=your_public_key_here" >> .env
```

### Common Errors

#### "无法验证指定的活动webhook 网址"

**Possible Causes**:

1. **Endpoint Not Accessible**
   ```bash
   # Test accessibility
   curl -I https://your-domain.com/discord/webhook
   # Should return 405 or 401 (not 404)
   ```

2. **No PONG Response**
   ```javascript
   // Must respond to type 0 with type 1
   if (req.body.type === 0) {
     return res.json({ type: 1 });
   }
   ```

3. **Timeout (>3 seconds)**
   ```javascript
   // Respond immediately, process later
   res.status(200).send();
   setImmediate(() => processEvent(req.body));
   ```

4. **SSL Certificate Issues**
   ```bash
   # Check certificate
   openssl s_client -connect your-domain.com:443 -servername your-domain.com
   ```

5. **Wrong Signature Verification**
   ```javascript
   // Must use raw body string, not parsed JSON
   req.rawBody = buf.toString('utf-8');
   ```

### Security Requirements

**Always Verify Signatures**:

```javascript
// ❌ DANGEROUS - No verification
app.post('/webhook', (req, res) => {
  processEvent(req.body);
});

// ✅ SAFE - Verify first
app.post('/webhook', (req, res) => {
  if (!verifyDiscordRequest(req)) {
    return res.status(401).send('Unauthorized');
  }
  processEvent(req.body);
});
```

**Best Practices**:
- ✅ Use HTTPS (required by Discord)
- ✅ Verify Ed25519 signature
- ✅ Check timestamp (prevent replay)
- ✅ Respond within 3 seconds
- ✅ Store PUBLIC_KEY in environment variables
- ✅ Log suspicious requests
- ✅ Rate limit the endpoint

**See Also**: `~/.openclaw/ai-team/discord-research/security-guide.md` for full security guide.

### Testing Your Webhook

**Test 1: Manual PING**
```bash
# This will fail (no valid signature) but tests connectivity
curl -X POST https://your-domain.com/discord/webhook \
  -H "Content-Type: application/json" \
  -d '{"type":0}'
  
# Expected: 401 Unauthorized (signature missing)
```

**Test 2: Discord Verification**
```bash
# Watch server logs while saving in Developer Portal
pm2 logs discord-webhook --lines 50

# You should see:
# ✅ Discord verification PING received
```

**Test 3: Check Logs**
```bash
# Server logs
pm2 logs discord-webhook

# Nginx access logs
sudo tail -f /var/log/nginx/access.log | grep webhook

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Does It Affect OpenClaw?

**No.** Event Webhooks and OpenClaw Gateway are **completely independent**:

```
┌─────────────────┐
│  Discord API    │
└────────┬────────┘
         │
    ┌────┴──────┐
    │           │
    ▼           ▼
┌────────┐  ┌──────────┐
│Gateway │  │ Webhooks │
│(WS)    │  │ (HTTP)   │
└───┬────┘  └────┬─────┘
    │            │
    ▼            ▼
┌─────────┐  ┌──────────┐
│OpenClaw │  │Your      │
│         │  │Services  │
└─────────┘  └──────────┘
```

- OpenClaw continues using Gateway (WebSocket)
- Webhooks send the same events to your HTTP endpoint
- Both can run simultaneously
- Disabling webhooks doesn't affect OpenClaw

### Should You Use Event Webhooks?

**Use Webhooks If**:
- You need to forward Discord events to external systems
- Building event-driven microservices
- Want to log all Discord activity
- Need events in multiple services

**Don't Use Webhooks If**:
- You only need OpenClaw to respond to messages (Gateway is enough)
- You're not sure why you need them
- You don't have infrastructure to receive HTTP webhooks

**Most users don't need Event Webhooks.** OpenClaw's Gateway connection handles all bot functionality.

---

## Security Best Practices

### ✅ Safe to Share (Public Info)

- Client ID
- OAuth authorization URLs
- Bot username/avatar
- Application name

### 🔒 Never Share (Secrets)

- **Bot Token** (`MTQ...pE`)
- **Client Secret**
- **OAuth access/refresh tokens**
- **User data from API**

### Protection Checklist

**Environment Variables**:
```bash
# .env file (add to .gitignore!)
DISCORD_BOT_TOKEN=MTQ...
DISCORD_CLIENT_SECRET=abc...
```

**Git Ignore**:
```gitignore
# .gitignore
.env
openclaw.json
config/credentials.json
```

**OpenClaw Config**:
```json
// Use env fallback instead of hardcoding
{
  "channels": {
    "discord": {
      "enabled": true
      // token auto-loads from DISCORD_BOT_TOKEN env var
    }
  }
}
```

**Minimum Permissions**:
```
# Don't use Administrator (8) unless absolutely necessary
# Use specific permissions:
permissions=2048  # Send Messages
permissions=3072  # + Embed Links
permissions=68608 # + Attach Files + Read History
```

**2FA Required**:
- Enable on Discord account
- Enable on Developer Portal
- Enable on servers with elevated bot permissions

---

## Troubleshooting

### Bot Not Receiving Messages

**Check Intents**:
```bash
# Verify in Developer Portal:
# Bot → Privileged Gateway Intents → Message Content Intent ✅
```

**Check Policy**:
```bash
openclaw channels status --probe

# Look for:
# - groupPolicy: allowlist vs open
# - requireMention: true/false
# - guilds allowlist
```

**Restart Gateway**:
```bash
openclaw gateway restart
```

### Permission Errors

**Check Bot Permissions in Server**:
1. Server Settings → Roles
2. Find your bot's role
3. Verify permissions match OAuth URL

**Check Channel Permissions**:
1. Channel Settings → Permissions
2. Check bot/role overrides

**Permission Integer Mismatch**:
```bash
# Current permissions
curl -H "Authorization: Bot TOKEN" \
  https://discord.com/api/v10/guilds/GUILD_ID/members/@me

# Compare with OAuth URL permissions parameter
```

### OAuth Flow Issues

**"Invalid OAuth2 redirect_uri"**:
```json
// In Developer Portal → OAuth2 → Redirects:
// Add your exact redirect URI (including protocol)
https://yourapp.com/callback  ✅
http://localhost:3000/auth    ✅
yourapp.com/callback          ❌ (missing protocol)
```

**"Missing Scopes"**:
```
# Bot authorization requires 'bot' scope
scope=bot  ✅
scope=identify  ❌ (not enough for bot)

# User auth requires at least 'identify'
scope=identify  ✅
scope=bot  ❌ (can't get user data)
```

**State Parameter Mismatch**:
```javascript
// Generate random state
const state = crypto.randomBytes(16).toString('hex');

// Store in session
req.session.oauthState = state;

// Verify on callback
if (req.query.state !== req.session.oauthState) {
  throw new Error('CSRF detected');
}
```

### Gateway Connection Issues

**Check Logs**:
```bash
openclaw logs --follow
# Look for Discord connection errors
```

**Test Token**:
```bash
curl https://discord.com/api/v10/users/@me \
  -H "Authorization: Bot YOUR_BOT_TOKEN"
  
# Should return bot user object
```

**Network Issues**:
```json
// If behind proxy:
{
  "channels": {
    "discord": {
      "proxy": "http://proxy.example:8080"
    }
  }
}
```

### Pairing Issues

**List Pending Pairings**:
```bash
openclaw pairing list discord
```

**Approve**:
```bash
openclaw pairing approve discord CODE
```

**DM Policy**:
```json
{
  "channels": {
    "discord": {
      "dmPolicy": "pairing"  // Not "disabled"
    }
  }
}
```

---

## Common Commands

### OpenClaw CLI

```bash
# Status
openclaw channels status
openclaw channels status --probe  # Check permissions

# Gateway
openclaw gateway start
openclaw gateway stop
openclaw gateway restart

# Pairing
openclaw pairing list discord
openclaw pairing approve discord CODE

# Logs
openclaw logs
openclaw logs --follow
openclaw logs --level debug

# Doctor
openclaw doctor  # Health check
```

### Discord API (curl)

```bash
# Get bot user info
curl -H "Authorization: Bot TOKEN" \
  https://discord.com/api/v10/users/@me

# Get guilds bot is in
curl -H "Authorization: Bot TOKEN" \
  https://discord.com/api/v10/users/@me/guilds

# Get application info
curl -H "Authorization: Bot TOKEN" \
  https://discord.com/api/v10/oauth2/applications/@me
```

---

## Reference Links

### Official Documentation
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord OAuth2 Docs](https://discord.com/developers/docs/topics/oauth2)
- [Discord Permissions](https://discord.com/developers/docs/topics/permissions)
- [Discord Gateway Intents](https://discord.com/developers/docs/topics/gateway#gateway-intents)

### OpenClaw
- [Channel Configuration](file:///opt/homebrew/lib/node_modules/openclaw/docs/channels/discord.md)
- [Pairing Guide](https://docs.openclaw.ai/channels/pairing)
- [Slash Commands](https://docs.openclaw.ai/tools/slash-commands)

### Tools
- [Permission Calculator](https://discordapi.com/permissions.html)
- [Snowflake Decoder](https://snowsta.mp/)
- [Discord API Explorer](https://discord.com/developers/docs/intro)

---

## Skill Maintenance

**Last Updated**: 2026-02-22  
**Maintained By**: Discord Research Specialist  
**Version**: 1.1  
**Status**: Active

### Changelog

**2026-02-22 - v1.1**
- ✨ Added Event Webhooks configuration section
- 📝 Webhook verification implementation (Node.js)
- 🔒 Security guide for webhook signature validation
- 🐛 Common webhook errors and solutions
- 📚 Webhook vs Gateway comparison

**2026-02-22 - v1.0**
- Initial skill creation
- OAuth2 security research
- Configuration templates
- Troubleshooting guide
