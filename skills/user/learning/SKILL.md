---
name: learning
description: 系统化学习新知识的流程。研究、理解、存储、应用四步法。当用户要求学习新领域、分享需要记住的信息、或开始不熟悉的项目时使用。
---

# Learning Skill

## Purpose
This skill enables Claude to systematically learn new knowledge, store it properly, and apply it in future conversations.

## Trigger
Use this skill when:
- User asks "learn about X"
- User shares new information that should be remembered
- Starting work in an unfamiliar domain
- Before creating any new project or skill

## Learning Process (4 Steps)

### Step 1: Research & Understand
```
BEFORE doing anything:
1. Search web for current best practices
2. Find 2026 industry standards
3. Identify professional workflows
4. Check pricing/market information (for business topics)
5. Review existing skills to avoid duplication
```

**Sources Priority**:
1. Official documentation
2. Industry leaders' blogs
3. Recent tutorials (2025-2026)
4. GitHub trending projects
5. Professional communities

### Step 2: Document Learning
Create a Learning Report in this format:

```markdown
# [Topic] Learning Report
**Date**: YYYY-MM-DD
**Goal**: [What level to achieve]

## Current Understanding
[What I knew before]

## New Knowledge
### 1. [Key Topic 1]
[Detailed notes]

### 2. [Key Topic 2]
[Detailed notes]

## Professional Standards
[Industry best practices]

## Tools & Technology
[Current tech stack]

## Pricing/Market Info
[If applicable - Malaysian market]

## Action Plan
[What to create/do next]

## Summary
[Key takeaways]
```

### Step 3: Create/Update Skills
**After learning, ALWAYS**:
1. Create new Skill if needed
2. Update existing Skills with new knowledge
3. Store in `/mnt/skills/user/[skill-name]/SKILL.md`

**Skill Template**:
```markdown
# [Skill Name]

## Trigger
When to use this skill

## Core Principles
Key rules and standards

## Workflow
Step-by-step process

## Examples
Practical examples

## Common Mistakes
What to avoid

## Checklist
Before/during/after work
```

### Step 4: Store Everything
**Triple Storage** (ALWAYS execute):

1. **GitHub** (Learning Report)
   ```bash
   /tmp/oskris/learning-reports/[TOPIC]_LEARNING.md
   ```

2. **GitHub** (Skill if created)
   ```bash
   /tmp/oskris/skills/user/[skill-name]/SKILL.md
   ```

3. **Memory Update**
   ```
   Add: "Completed [topic] learning on [date], created [skill name]"
   ```

4. **Present to User**
   Copy to `/mnt/user-data/outputs/`

---

## Quality Standards

### From Intern to Professional
Learning must achieve "Professional" level, not "Intern" level.

**Professional Learning includes**:
- ✅ Industry standards (2026)
- ✅ Complete workflows
- ✅ Market pricing (if applicable)
- ✅ Tools & tech stack
- ✅ Common pitfalls
- ✅ Quality metrics
- ✅ Professional vs amateur comparison

**Avoid Intern-level Learning**:
- ❌ Surface-level understanding
- ❌ Outdated information
- ❌ No workflow/process
- ❌ No pricing awareness
- ❌ Just copying examples

---

## Learning Checklist

Before saying "I've learned X":

- [ ] Researched 3+ authoritative sources
- [ ] Found 2026 best practices
- [ ] Created Learning Report
- [ ] Created/Updated relevant Skill
- [ ] Stored in GitHub (learning-reports/)
- [ ] Stored in GitHub (skills/user/)
- [ ] Updated memory
- [ ] Presented files to user
- [ ] Can explain it professionally
- [ ] Can apply it immediately

---

## Continuous Learning

### When to Learn More
- New project type encountered
- User asks about unfamiliar topic
- Technology/tool is outdated
- Market conditions changed
- Professional standards evolved

### Update Cycle
- **Skills**: Update when learning new information
- **Learning Reports**: New report for each learning session
- **Memory**: Add key facts, keep concise

---

## Examples

### Example 1: Learning Web Design
```
1. Research: 
   - 2026 web design trends
   - Professional workflows
   - Malaysian pricing
   
2. Document:
   - Create PROFESSIONAL_WEB_DESIGN_LEARNING.md
   - 7-stage workflow
   - Pricing RM 1,500-25,000+
   
3. Create Skills:
   - professional-web-design
   - requirements-analyst
   - design-consultant
   - frontend-builder
   
4. Store & Update:
   - GitHub learning-reports/
   - GitHub skills/user/
   - Memory: "Completed web design learning"
```

### Example 2: Learning New Framework
```
1. Research:
   - Official docs
   - Best practices 2026
   - Performance benchmarks
   
2. Document:
   - [FRAMEWORK]_LEARNING.md
   - Setup guide
   - Common patterns
   
3. Create Skill:
   - [framework]-development
   
4. Store:
   - All locations
   - Update memory
```

---

## Critical Rules

1. **NEVER claim to know something without learning first**
   - If unfamiliar, SAY SO and start learning process
   
2. **ALWAYS research before creating**
   - Don't rely on training data alone
   - Get current 2026 information
   
3. **STORE everything learned**
   - Learning Report
   - Skills
   - Memory
   - User outputs
   
4. **APPLY learning immediately**
   - Test understanding
   - Use in next project
   - Reference in work

---

## Integration with Other Skills

This Learning Skill works with:
- **work-rules**: Follow quality standards
- **auto-storage**: Automatic triple storage
- **smart-info-manager**: Organize learned info
- **All project skills**: Apply learning to real work

---

**Last Updated**: 2026-02-16
**Status**: Active - use for all learning tasks
