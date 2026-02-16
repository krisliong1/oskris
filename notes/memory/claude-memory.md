# Claude 记忆系统

最后更新: 2026-02-16

## 核心配置
1. GitHub: krisliong1/oskris, 只推main分支, /tmp克隆操作
2. VPS: 76.13.191.45, Ubuntu 25.10, 2核8GB, Malaysia
3. Hostinger API已配置(token存Claude记忆)
4. 域名: oskris.com(到期2027)
5. 用户邮箱: oskrismy@gmail.com / official@oskris.com

## 工作规则
6. 所有价格用RM(马来西亚令吉)
7. 用户零代码基础, Claude负责学习+执行
8. 质量等级: 初级→中级→高级→专业级, 要求专业级
9. 先验证再执行, 不用占位符
10. 代码/命令保持英文, 其他用华文回复
11. 提供命令不加#注释, 只给纯代码
12. 文件已存在用str_replace, 不要盲目创建

## 自动存储
13. Claude修改文件后自动: 上传GitHub + Hostinger API同步VPS
14. 每步告诉用户新建/更新了什么
15. 敏感信息禁止存GitHub, 只存VPS+记忆
16. 记忆更新后同步此文件: notes/memory/claude-memory.md

## Skills分类
17. core/ - 核心系统(work-rules, core-work-rules, secrets-manager等)
18. web-development/ - 网站开发(project-workflow, frontend-builder等)
19. content/ - 翻译(auto-translate, smart-info-manager)
20. product/ - 产品(product-self-knowledge, app-recommendations)

## 当前项目
21. websitedesign.oskris.com - 网站设计服务
22. 定价: RM 1,999 / 4,999 / 9,999
