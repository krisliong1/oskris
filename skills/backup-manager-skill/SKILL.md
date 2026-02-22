# Backup Manager Skill

## 职责
专门负责所有备份任务：数据备份、同步、验证、恢复

## 核心原则
- VPS备份优先于GitHub
- credentials/只备份VPS，不上GitHub
- 每次备份后验证完整性
- 使用rsync增量备份

## 工作流程
1. 接收备份任务
2. 检查源和目标
3. 执行rsync
4. 验证完整性（du -sh对比）
5. 记录到MEMORY.md
6. 提交学习报告

## 常用命令
```bash
rsync -avz --progress SOURCE/ DEST/
ssh root@76.13.191.45 "du -sh /path"
```

## 禁止操作
- 不能删除备份（只能覆盖）
- 不能修改核心文件（444保护）
