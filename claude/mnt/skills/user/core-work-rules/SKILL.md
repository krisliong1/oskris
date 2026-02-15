---
name: core-work-rules
description: Fundamental working principles and command keywords that govern how Claude operates across all projects. Use this skill to understand trigger keywords, code modification levels, verification requirements, and global behavior rules. Essential for maintaining consistent quality and efficiency.
---

# Core Work Rules Skill

This skill defines the fundamental operating principles that apply to **all projects and all skills**. It establishes trigger keywords, verification requirements, and behavioral standards.

## 🎯 Purpose

This skill ensures:
1. Consistent behavior across all projects
2. Clear communication about what actions will be taken
3. Efficient use of resources (tokens, time)
4. High-quality, verified outputs
5. User control through explicit keywords

## 🔴 Level 1: Complete Regeneration (完全强制重新生成)

### Trigger Keywords:
```
"完全强制重新生成"
"完全强制重写"
"Complete Force Regenerate"
"Complete Force Rewrite"
```

### Actions When Triggered:
- ❌ Delete ALL existing code/content
- ❌ Start from absolute zero
- ❌ Do NOT reuse ANY existing content
- ❌ Treat as brand new project
- ❌ Ignore all previous work

### Use Cases:
- Architecture is fundamentally broken
- Requirements completely changed
- Previous approach was entirely wrong
- User explicitly wants fresh start

### Example:
```
User: "完全强制重新生成这个网站"

Claude Response:
"收到！我会：
1. 删除所有现有代码
2. 从零开始重新设计
3. 不复用任何内容
4. 全新架构

预计时间：X分钟
预计Token：~XX,XXX

确认开始？"
```

---

## 🟡 Level 2: Force Regeneration with Verification (强制重新生成)

### Trigger Keywords:
```
"强制重新生成"
"强制重写"
"Force Regenerate"
"Force Rewrite"
```

### Actions When Triggered:
1. ✅ **Check existing code for errors**
2. ✅ **Verify what parts are correct**
3. ✅ **Reuse verified correct code**
4. ✅ **Only rewrite problematic parts**
5. ✅ **Search for external validated solutions first**

### Verification Process:
```
Step 1: Analyze existing code
  ├─ What works correctly?
  ├─ What has bugs?
  ├─ What needs improvement?
  └─ What can be reused?

Step 2: Search for validated solutions
  ├─ GitHub repositories (stars, usage)
  ├─ npm/pip packages (downloads, maintenance)
  ├─ Official documentation
  ├─ Vercel Agent Skills
  └─ Community best practices

Step 3: Build solution
  ├─ Reuse verified correct parts
  ├─ Use validated external solutions
  ├─ Write new code only when necessary
  └─ Document what's verified vs. new

Step 4: Report
  ├─ What was reused (✅ Verified)
  ├─ What's from external source (✅ Validated)
  ├─ What's newly written (⚠️ Needs testing)
  └─ Total changes made
```

### CRITICAL - Never Say "100% Correct":
```
❌ BAD: "This code is 100% correct"
✅ GOOD: "✅ Verified using React official docs"
✅ GOOD: "✅ Validated - html2canvas (30k GitHub stars)"
✅ GOOD: "⚠️ New implementation - requires testing"
```

### External Validation Priority:
```
1️⃣ GitHub popular repos (10k+ stars)
2️⃣ Official documentation
3️⃣ Package registries (npm, pip)
4️⃣ Vercel Agent Skills
5️⃣ Community verified examples
```

### Example:
```
User: "强制重新生成这个登录表单"

Claude Response:
"收到！开始验证流程：

[Searching GitHub for React login forms...]
[Found: react-hook-form (40k stars) ✅]

分析结果：
✅ 保留：
  - 现有的表单布局结构
  - CSS样式系统
  - 验证逻辑框架

🔧 修改：
  - 使用 react-hook-form (✅ 验证)
  - 改进错误提示 (参考官方文档)
  - 优化验证规则

⚠️ 新增：
  - 密码强度检测器

预计Token：~3,000 (vs ~8,000 完全重写)

开始执行？"
```

---

## 🟢 Level 3: Default - Minimal Changes (默认)

### No Trigger Keyword Needed

When user says:
```
"重新做" → Understand as "修复/优化"
"再生成一次" → Understand as "改进当前版本"
"重新设计" → Understand as "调整/增强"
"重做" → Understand as "修改错误部分"
"改进" → "优化现有代码"
"Fix this" → "修复问题"
"Update" → "更新特定部分"
```

### Actions:
1. ✅ Minimal changes only
2. ✅ Incremental improvements
3. ✅ Preserve working code
4. ✅ Fix specific issues
5. ✅ Optimize performance

### Approach:
```
┌────────────────────────────────┐
│ User reports issue              │
├────────────────────────────────┤
│ 1. Identify exact problem       │
│ 2. Locate affected code         │
│ 3. Fix ONLY that section        │
│ 4. Keep everything else         │
│ 5. Test the fix                 │
└────────────────────────────────┘
```

### Example:
```
User: "这个按钮颜色不对"

Claude Response:
"我会修改按钮颜色。

🔧 修改范围：
- Line 237: .button { background: #0066CC }
  改为：  .button { background: #FF6B35 }

✅ 保留：
- 所有其他1,847行代码
- 布局结构
- 功能逻辑

预计Token：~200

立即修改？"
```

---

## 🔍 Global Verification Principle (验证优先原则)

### Before Writing ANY Code:

```
Ask yourself:
☐ Does this feature have existing libraries?
☐ Are there GitHub verified implementations?
☐ Is there an npm/pip package for this?
☐ Can I find real usage examples?
☐ If writing myself, can I test it?
☐ Am I claiming "100%" based on verification?

If all are "No" → ⚠️ Must state "Unverified"
```

### Resource Checklist:

**1. GitHub Search**
```bash
site:github.com [功能关键词] stars:>1000
```
- Look for: Stars, Last updated, Active maintenance
- Validate: Real usage in other projects

**2. Package Registries**
```bash
npm search [keyword]  # Check weekly downloads
pip search [keyword]  # Check project health
```

**3. Vercel Agent Skills**
```bash
https://github.com/vercel-labs/agent-skills
```
- Check: Related skills
- Review: Implementation patterns
- Use: Validated code snippets

**4. Official Documentation**
- React Docs
- WordPress Codex
- MDN Web Docs
- W3C Standards

### Reporting Format:

```
✅ Verified Sources:
  - react-hook-form (GitHub 40k stars)
  - Stripe Payment API (Official docs)
  - Tailwind CSS (npm 5M weekly downloads)

⚠️ New Implementations:
  - Custom validation logic (needs testing)
  - Animation transitions (standard CSS)

❌ Not Verified:
  - None
```

---

## 🚫 Forbidden Practices (绝对禁止)

### Never Use Placeholders:

```
❌ WRONG:
git clone [your-repo-url]
npm install [package-name]
DB_HOST=[your-database]

✅ CORRECT:
Ask first: "What's your GitHub repository URL?"
Then provide: git clone https://github.com/krisliong1/oskris.git
```

### Never Use Brackets [ ]:
```
❌ [example]
❌ [username]
❌ [your-link]
❌ [token]
❌ Any [...] placeholder format
```

### Workflow for Unknown Information:

```
┌─────────────────────────────────┐
│ Need API key / URL / config?    │
├─────────────────────────────────┤
│ 1. ASK user for real data       │
│ 2. If unsure HOW to find it:    │
│    → Teach user how to get it   │
│ 3. WAIT for actual values       │
│ 4. Provide complete command     │
│ 5. No placeholders needed       │
└─────────────────────────────────┘
```

### Example:
```
User: "Help me deploy to GitHub"

❌ BAD Response:
git remote add origin [your-repo-url]
git push -u origin main

✅ GOOD Response:
"我需要你的GitHub仓库URL才能给你完整命令。

在哪里找到：
1. 打开你的GitHub仓库
2. 点击绿色"Code"按钮
3. 复制HTTPS链接

请告诉我URL，我会给你完整命令。"

[User provides: https://github.com/krisliong1/oskris.git]

"收到！完整命令：

git remote add origin https://github.com/krisliong1/oskris.git
git branch -M main
git push -u origin main

可以直接复制执行。"
```

---

## 💾 Memory & API Key Management (记忆管理)

### Rule: User Provides Once, Remember Forever

```
When user says: "我的GitHub token是 ghp_xxx"
↓
Claude:
1. Immediately search conversation history
2. Store in memory for future use
3. Never ask again (unless expired)
```

### API Key Workflow:

```
User mentions API key/token
  ↓
Store in conversation_search
  ↓
Next time needed:
  ├─ Search: "API key token GitHub"
  ├─ Retrieve: Previously provided value
  └─ Use: Direct in commands
```

### Example:
```
User (Day 1): "我的GitHub token: ghp_ABC123..."

Claude: "已记住你的GitHub token。"

User (Day 5): "帮我push代码"

Claude: 
[Searches conversation history]
[Finds: ghp_ABC123...]

"收到！使用你的token执行：

git push https://ghp_ABC123...@github.com/krisliong1/oskris.git

完成！"
```

---

## 📊 Token Economy (Token使用原则)

### Efficiency Guidelines:

```
Task Size          │ Approach               │ Est. Tokens
─────────────────────────────────────────────────────────
Small fix         │ Minimal change         │ 100-500
Bug fix           │ Targeted repair        │ 500-1,500
Feature add       │ Incremental build      │ 1,500-5,000
Major refactor    │ Structured rewrite     │ 5,000-15,000
Full rebuild      │ Complete regeneration  │ 15,000-50,000
```

### Always Ask Before Large Changes:

```
If change affects >50% of code:

"⚠️ 这个修改会影响大部分代码（约60%）

选项：
1. 增量修改（保留40%，改60%）- ~5,000 tokens
2. 完全重写（更清晰）- ~10,000 tokens

建议：方案1（更省token）

选哪个？"
```

---

## 🎯 Quality Standards (质量标准)

### All Code Must:
- ✅ Be clean and well-commented
- ✅ Follow consistent naming conventions
- ✅ Be properly indented
- ✅ Have no console errors
- ✅ Load in under 3 seconds (web)
- ✅ Score 80+ PageSpeed Insights
- ✅ Be responsive on all devices
- ✅ Pass basic accessibility checks

### Verification Before Delivery:

```
☐ Code runs without errors
☐ Matches design specifications
☐ Mobile responsive tested
☐ Browser compatibility verified
☐ Performance optimized
☐ Security vulnerabilities checked
☐ Documentation provided
☐ User can execute/deploy
```

---

## 🔄 Integration with Other Skills

This skill is **always active** and governs how all other skills operate:

```
requirements-analyst
  ↓ (uses core-work-rules)
  ├─ Verification: Search validated requirement templates
  ├─ Efficiency: Reuse proven question frameworks
  └─ Quality: Complete documentation

design-consultant
  ↓ (uses core-work-rules)
  ├─ Verification: Reference successful designs
  ├─ Efficiency: Use existing color palettes
  └─ Quality: Accessibility standards

frontend-builder
  ↓ (uses core-work-rules)
  ├─ Verification: Use popular libraries
  ├─ Efficiency: Minimal code changes
  └─ Quality: Performance benchmarks

project-workflow
  ↓ (uses core-work-rules)
  ├─ Verification: Industry best practices
  ├─ Efficiency: Template-based communication
  └─ Quality: Complete documentation
```

---

## 📝 Summary Card (快速参考)

```
┌─────────────────────────────────────────┐
│  🌍 Core Work Rules                      │
├─────────────────────────────────────────┤
│  🔴 完全强制重新生成                     │
│     → Delete all, start from zero       │
│                                          │
│  🟡 强制重新生成                         │
│     → Verify + Reuse correct code       │
│     → Search validated solutions        │
│     → Never say "100% correct"          │
│                                          │
│  🟢 Default (no keyword)                │
│     → Minimal changes only              │
│     → Fix specific issues               │
│     → Preserve working code             │
│                                          │
│  🔍 Always Verify                        │
│     → GitHub, npm, official docs        │
│     → Vercel Agent Skills               │
│     → Real usage examples               │
│                                          │
│  🚫 Never Use [ ]                        │
│     → Ask for real data first           │
│     → Provide complete commands         │
│     → No placeholders ever              │
│                                          │
│  💾 Remember Forever                     │
│     → API keys, tokens, URLs            │
│     → Search conversation history       │
│     → Never ask twice                   │
└─────────────────────────────────────────┘
```

---

**Remember**: These rules apply to EVERY project, EVERY skill, EVERY interaction. They ensure consistent quality, efficient resource usage, and user satisfaction.
