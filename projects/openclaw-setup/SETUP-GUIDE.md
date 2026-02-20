# OpenClaw 一次性配置操作手册

> 回家后照着这个一步步做，全部完成大约15分钟
> 做完后 gateway 就不会再乱断连了

---

## 第0步：准备工作（确认状态）

```bash
su - openclaw
openclaw gateway status
openclaw doctor
cat ~/.openclaw/openclaw.json
```

把当前 `openclaw.json` 的内容记下来或截图，等下要在这基础上改。

---

## 第1步：停掉 gateway（先别让它乱动）

```bash
openclaw gateway stop
```

---

## 第2步：备份当前配置

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d_%H%M%S)
```

---

## 第3步：修改 openclaw.json

用 nano 打开：
```bash
nano ~/.openclaw/openclaw.json
```

在现有配置基础上，**确保包含以下内容**（如果已有某个字段就修改值，没有就添加）：

```json5
{
  // === 你的现有配置保持不变 ===
  // identity, agents, auth 等原来有什么就留什么

  // === 加入Telegram channel ===
  channels: {
    // 保留你原来已有的channel（比如discord）不要删
    
    telegram: {
      botToken: "[见Claude记忆]",
      dmPolicy: "allowlist",
      allowFrom: ["[见Claude记忆]"]
    }
  },

  // === 加入工具限制（防止AI乱改文件）===
  tools: {
    exec: {
      approvals: "always"
    }
  },

  // === session稳定性设置 ===
  session: {
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 120
    }
  }
}
```

**重要提醒：**
- JSON5格式，可以有注释和尾逗号
- 不要删掉你原来已有的配置（identity、auth、discord等）
- 只是在原有基础上添加/修改上面这些字段
- `allowFrom` 里的 `[见Claude记忆]` 是你的Telegram ID

保存退出 nano：`Ctrl+X` → `Y` → `Enter`

---

## 第4步：验证配置是否正确

```bash
openclaw doctor
```

如果有错误，它会告诉你哪里不对。修到没有error为止。

---

## 第5步：更新 SOUL.md（加保护规则）

```bash
nano ~/.openclaw/workspace/SOUL.md
```

在文件**最前面**加入以下内容（不要删原来的内容）：

```markdown
## 绝对禁止（最高优先级规则）

1. 永远不要修改 ~/.openclaw/openclaw.json
2. 永远不要修改 ~/.openclaw/ 目录下的任何系统配置文件
3. 永远不要执行 openclaw config set 命令
4. 永远不要自己重启 gateway（不要执行 openclaw gateway restart）
5. 如果需要修改任何配置，只能告诉用户具体的操作步骤，自己不动手

## 错误处理规则

1. exec命令失败后，不要连续重试超过2次
2. 失败2次后直接告诉用户问题在哪，不要继续尝试
3. 每次犯错后必须记录到 .learnings/ERRORS.md
4. 执行任何操作前先检查 .learnings/ 里有没有相关的历史错误记录
5. 修改任何文件前，先告诉用户要改什么，不要直接改

## 文件操作规则

1. 不要直接覆盖原始文件，先备份再改
2. 配置类文件（.json, .yaml, .toml, .config）一律不准自己改
3. 只能在 workspace 目录内创建和修改文件
```

保存退出。

---

## 第6步：安装 self-improvement skill

```bash
cd ~/.openclaw/skills
git clone https://github.com/peterskoett/self-improving-agent.git self-improving-agent
```

如果 skills 目录不存在：
```bash
mkdir -p ~/.openclaw/skills
cd ~/.openclaw/skills
git clone https://github.com/peterskoett/self-improving-agent.git self-improving-agent
```

创建 learnings 目录：
```bash
mkdir -p ~/.openclaw/workspace/.learnings
touch ~/.openclaw/workspace/.learnings/LEARNINGS.md
touch ~/.openclaw/workspace/.learnings/ERRORS.md
touch ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md
```

---

## 第7步：启动 gateway

```bash
openclaw gateway start
```

---

## 第8步：验证一切正常

```bash
openclaw gateway status
openclaw doctor
openclaw models status
```

全部正常后，测试Telegram：打开Telegram给你的bot发一条消息，看看能不能回复。

---

## 第9步：锁住配置文件（最关键！）

**确认一切正常后**再执行这步：

```bash
chmod 444 ~/.openclaw/openclaw.json
```

验证已锁住：
```bash
ls -la ~/.openclaw/openclaw.json
```

应该显示 `-r--r--r--`，表示只读。

---

## 以后要改配置怎么办？

```bash
su - openclaw
openclaw gateway stop
chmod 644 ~/.openclaw/openclaw.json
nano ~/.openclaw/openclaw.json
# 改完后
chmod 444 ~/.openclaw/openclaw.json
openclaw gateway start
```

---

## 故障排除

### gateway启动失败
```bash
chmod 644 ~/.openclaw/openclaw.json
openclaw doctor
# 根据提示修复
chmod 444 ~/.openclaw/openclaw.json
openclaw gateway start
```

### Telegram收不到消息
```bash
openclaw doctor
# 检查 botToken 是否正确
# 检查 allowFrom 里的ID是否正确
```

### token过期
```bash
# 在 user:oskris 终端
claude setup-token
# 复制token

# 切到 user:openclaw
su - openclaw
openclaw models auth paste-token --provider anthropic
openclaw gateway restart
```

---

*创建时间: 2026-02-20*
*配合文件: soul-protection-rules.md, openclaw-config-template.json5*
