---
name: advanced-learning-engine  
description: Oskris持续进化引擎进化版。搜索验证→消化应用→技能创建→存储闭环。防止知识过时，确保技能可用。
---

# Advanced Learning Engine

## 核心理念：知识会过时

### ⚠️ 自信偏差问题
- 30%以上的训练数据已过时
- 技术栈快速更新
- 平台功能持续变化
- 必须**搜索验证**而非依赖记忆

## 5步学习闭环

### 第1步: 承认无知
```
❌ "据我所知..." + 输出旧信息
✅ "让我搜索最新信息..." + 实际搜索
```

### 第2步: 多源验证
```python
search_sources = [
    "英文权威文档",      # 官方API、技术规范
    "GitHub最新项目",   # 实际代码实现
    "2025-2026更新",   # 最新版本变化
    "马来西亚本地化"    # 地区特定信息
]
```

### 第3步: 知识提炼
- 区分**通用知识** vs **新信息**
- 按模板格式整理学习报告
- 达到**专业级**质量标准

### 第4步: 立即应用
```
学习 → 直接执行任务
不是: 学习 → 写报告 → 建议用户去做
而是: 学习 → 我直接帮用户完成
```

### 第5步: 存储闭环
```bash
# 自动执行
1. 学习报告 → learning-reports/topic.md
2. 新技能 → skills/category/name/SKILL.md  
3. 过程记录 → learning-logs/date-topic.md
4. 搜索结果 → 永久保存，不丢弃
5. 更新记忆 → 关键结论入库
6. 失败记录 → references/past-mistakes.md
```

## 技能创建标准

### 格式要求
```yaml
---
name: skill-name  # 小写+连字符，≤64字符
description: >-   # ≤1024字符，清晰说明用途
  详细描述何时触发此技能...
---
```

### 内容结构
```markdown
# 技能标题

## 触发条件
明确说明什么情况下使用

## 核心流程  
具体步骤和检查清单

## 质量标准
专业级输出要求

## 实战经验
基于实际使用的经验总结
```

### 质量检验
- [ ] 技能能否被正确触发？
- [ ] 流程是否完整可执行？
- [ ] 输出是否达到专业级？
- [ ] 错误时是否有替代方案？

## 苏格拉底教学法

### 适用场景
- 用户学生使用此skill
- 复杂概念需要引导理解

### 实施策略  
```python
def socratic_teaching(student_level, goal):
    roadmap = generate_learning_path(student_level, goal, stages=3-7)
    for stage in roadmap:
        questions = generate_guiding_questions(stage)
        responses = collect_student_answers(questions)
        feedback = adaptive_feedback(responses)
        if understanding_verified(feedback):
            advance_to_next_stage()
        else:
            review_and_reinforce()
```

## 错误处理机制

### 发现错误时
1. **承认错误**，不找借口
2. **立即搜索**确认正确信息
3. **更新记录** → past-mistakes.md
4. **推送GitHub**保存教训
5. **检查是否影响**其他技能或记忆

### 预防措施
- 时效性问题前必须搜索
- 技术实现前验证可行性
- 关键决策多源交叉验证

## 环境适配能力

### 自动检测
```python
def detect_environment():
    if has_tool("web_search"):
        use_search_validation = True
    if has_tool("filesystem"):
        use_direct_file_ops = True
    else:
        provide_download_instructions = True
```

### 适配策略
- **工具可用** → 直接执行
- **工具不可用** → 提供替代方案
- **不确定** → 搜索确认，不猜测

---
*基于Oskris学习引擎实战优化*