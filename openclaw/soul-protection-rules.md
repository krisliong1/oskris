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
