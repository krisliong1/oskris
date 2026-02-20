# OpenClaw Discord 配置指南

## 已配置的Discord Bots

### honorkingsellbot ✅ 已配置
- Application ID: 1474259579729739949
- Public Key: fcf36775dcc5f27d10e8931052aec7ba7a0bad276be589114377c5824456acbd
- Bot Token: 见Claude记忆
- 状态: 已连接OpenClaw

### kaijiepeiwanbot ⏳ 待配置
- Application ID: 1474253373380231372
- Public Key: e8c97df76b3d11e7916bf1493c676bb614c27b4f05acc2e66aa984277eee88ef
- 登录邮箱: kaijiepeiwan@gmail.com
- Bot Token: 待获取
- 状态: 待配置到OpenClaw

## Discord服务器
- 邀请链接: https://discord.gg/pk9HtCq9

## 配置步骤

### 1. 创建Discord Bot
1. 打开 https://discord.com/developers/applications
2. New Application → 命名
3. 左边 Bot → Reset Token → 复制Token
4. 打开 Message Content Intent / Server Members Intent / Presence Intent

### 2. 邀请Bot到服务器
```
https://discord.com/api/oauth2/authorize?client_id={APPLICATION_ID}&permissions=8&scope=bot
```

### 3. 写入OpenClaw配置
```bash
python3 -c "
import json
f='/Users/openclaw/.openclaw/openclaw.json'
c=json.load(open(f))
c['channels']['discord']={
  'enabled':True,
  'botToken':'YOUR_BOT_TOKEN',
  'dmPolicy':'owner',
  'commands':{'native':True,'nativeSkills':True},
  'actions':{'reactions':True,'sendMessage':True}
}
c.setdefault('plugins',{}).setdefault('entries',{})['discord']={'enabled':True}
json.dump(c,open(f,'w'),indent=2)
print('done')
"
```

### 4. 重启Gateway
```bash
openclaw gateway restart
```

## 常见问题

### pairedChats无效key错误
OpenClaw自我修复时可能添加无效配置key，手动删除：
```bash
python3 -c "
import json
f='/Users/openclaw/.openclaw/openclaw.json'
c=json.load(open(f))
if 'pairedChats' in c.get('channels',{}).get('telegram',{}):
    del c['channels']['telegram']['pairedChats']
json.dump(c,open(f,'w'),indent=2)
print('done')
"
```

### allowFrom缺失错误
dmPolicy="open"需要allowFrom包含"*"：
```bash
python3 -c "
import json
f='/Users/openclaw/.openclaw/openclaw.json'
c=json.load(open(f))
c['channels']['telegram']['allowFrom']=['*']
json.dump(c,open(f,'w'),indent=2)
print('done')
"
```

### gateway.mode未设置
```bash
openclaw config set gateway.mode local
```

### BlueBubbles duplicate plugin警告
可安全忽略。

## 浏览器偏好
- DuckDuckGo ✅ 换网络不需重新验证
- Opera ❌ 换网络自动退出（不推荐）

---
*最后更新: 2026-02-20*
