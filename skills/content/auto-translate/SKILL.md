---
name: auto-translate
description: 自动识别英文消息并用中文回复，代码和技术术语保持英文。当用户发送英文消息时触发，确保中文解释+英文代码的混合回复风格。
---

# Auto Translate

用户消息超过50%英文时自动触发，用中文回复。

## 规则

**用中文的**：解释、说明、对话、描述

**保持英文的**：代码、命令、函数名、变量名、文件路径、URL、API端点、框架名(React/Vue/Django)、编程语言名(Python/JavaScript)、工具名(npm/git/docker)、文件格式(.json/.csv)

**术语处理**：首次出现用「英文(中文)」如「API(应用程序接口)」，后续可直接用中文简称。

## 示例

用户: "How do I read a CSV file in Python?"

回复:
```
你可以用pandas读取CSV文件：

import pandas as pd
df = pd.read_csv('data.csv')
print(df.head())

pandas适合数据分析，如果只需简单读取可以用标准库csv模块。
```

## 特殊情况

- 用户要求英文回复 → 整个回复用英文
- 用户本身用中文 → 正常中文回复
- 混合语言 → 以主要语言为准，不确定时默认中文
- 不要主动说明「我把你的英文翻译成...」，直接回复
