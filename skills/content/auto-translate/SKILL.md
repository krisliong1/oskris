---
name: auto-translate
description: 自动识别英文消息并用中文回复,同时确保代码、技术术语和命令保持英文。当用户发送英文消息时,自动用中文翻译并回复,但所有代码、编程语言关键字、命令行指令、技术术语等保持原始英文。
---

# 自动翻译 Skill

## 核心功能

这个skill会:
1. **自动检测用户消息的语言** - 识别消息是否主要为英文
2. **智能翻译回复** - 用中文回复用户,但保持技术内容的准确性
3. **代码语言保护** - 确保所有代码、命令和技术术语保持英文

## 触发条件

当用户的消息满足以下条件时自动激活:
- 消息主要由英文组成(超过50%的内容为英文字符)
- 消息包含英文句子或段落
- 用户明确用英文提问或交流

## 回复规则

### 1. 语言使用
- **默认回复语言**: 中文(简体)
- **用户偏好**: 中文是首选语言
- **翻译原则**: 自然流畅的中文表达,不要生硬的直译

### 2. 代码和技术内容保护

**必须保持英文的内容**:
- 所有编程代码(Python, JavaScript, HTML, CSS等)
- 编程语言关键字和函数名
- 命令行指令和shell命令
- 文件路径和文件名
- API端点和URL
- 技术术语的英文原名(可在首次出现时附上中文解释)
- 变量名、类名、方法名
- 配置文件内容
- 数据库查询语句
- 正则表达式

**示例**:

用户问(英文): "How do I create a Python function to calculate factorial?"

正确回复(中文+英文代码):
```
你可以这样创建一个计算阶乘的Python函数:

​```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
​```

这个函数使用递归方法计算阶乘。
```

错误回复(不要这样):
```
你可以这样创建一个计算阶乘的蟒蛇函数:  # ❌ 不要翻译Python

​```python
定义 阶乘(数字):  # ❌ 不要翻译代码
    如果 数字 == 0 或者 数字 == 1:
        返回 1
    返回 数字 * 阶乘(数字 - 1)
​```
```

### 3. 混合内容处理

当回复中包含中文解释和英文技术内容时:
- 中文部分: 流畅自然的解释和说明
- 英文部分: 所有代码、命令、术语保持原样
- 术语处理: 首次出现时可以"英文术语(中文解释)"的格式,如 "API(应用程序接口)"

**示例**:

用户问(英文): "What's the difference between GET and POST requests?"

正确回复:
```
GET和POST是两种主要的HTTP请求方法,它们的区别是:

1. **GET请求**:
   - 用于从服务器获取数据
   - 参数在URL中可见,如: `https://api.example.com/users?id=123`
   - 适合查询操作

2. **POST请求**:
   - 用于向服务器发送数据
   - 参数在请求体(request body)中,更安全
   - 适合创建或更新数据

代码示例:
​```javascript
// GET请求
fetch('https://api.example.com/users?id=123')
  .then(response => response.json())
  .then(data => console.log(data));

// POST请求
fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ name: 'John', age: 30 })
});
​```
```

### 4. 技术术语处理指南

| 场景 | 处理方式 | 示例 |
|------|---------|------|
| 编程语言名 | 保持英文 | Python, JavaScript, Java |
| 框架/库名 | 保持英文 | React, Vue, Django |
| 技术概念(首次) | 英文(中文) | API(应用程序接口) |
| 技术概念(后续) | 可用中文简称 | 接口、数据库 |
| 命令和工具 | 保持英文 | npm, git, docker |
| 文件格式 | 保持英文 | .json, .csv, .xlsx |

### 5. 非技术对话

如果用户用英文问非技术问题,正常用中文回复即可:

用户问: "What's the weather like today?"
回复: "抱歉,我需要知道你所在的位置才能查询天气信息。你在哪个城市?"

## 特殊情况

### 用户明确要求英文回复
如果用户明确说"please reply in English"或"用英文回复",则:
- 整个回复使用英文
- 暂时覆盖此skill的默认行为

### 用户用中文提问
如果用户本身就用中文提问,则:
- 正常用中文回复
- 代码和技术内容仍保持英文

### 混合语言输入
如果用户消息中既有中文又有英文:
- 以主要语言(占比>50%)为准
- 如果难以判断,默认用中文回复

## 实施要点

1. **不要主动说明翻译**: 直接用中文回复即可,不需要说"我已经将你的英文问题翻译..."
2. **保持专业性**: 技术术语使用行业标准的中文表达
3. **代码完整性**: 代码块必须完全可执行,不能因翻译而破坏语法
4. **自然表达**: 中文回复要符合中文的表达习惯,不要英文式中文
5. **一致性**: 同一技术术语在对话中保持一致的表达方式

## 示例对话

**用户**: "How can I read a CSV file in Python?"

**Claude回复**:
```
你可以使用Python的`pandas`库来读取CSV文件,这是最常用的方法:

​```python
import pandas as pd

# 读取CSV文件
df = pd.read_csv('your_file.csv')

# 查看前几行
print(df.head())

# 查看基本信息
print(df.info())
​```

如果你想用Python的标准库,也可以使用`csv`模块:

​```python
import csv

with open('your_file.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)
​```

`pandas`的方法更强大,适合数据分析;`csv`模块更轻量,适合简单的读取操作。
```

---

**用户**: "What is React and why should I use it?"

**Claude回复**:
```
React是Facebook开发的一个JavaScript库,用于构建用户界面。以下是使用React的主要原因:

1. **组件化开发**: 可以将UI拆分成独立、可复用的组件
2. **虚拟DOM**: 提高性能,减少实际DOM操作
3. **声明式编程**: 代码更易读易维护
4. **生态系统丰富**: 大量的第三方库和工具支持

简单的React组件示例:

​```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

// 使用组件
<Welcome name="张三" />
​```

React特别适合构建单页应用(SPA)和复杂的交互界面。
```

## 结论

此skill的核心是:**用中文思考和解释,用英文编码和命令**。确保用户能用熟悉的中文理解技术概念,同时保证所有代码和命令的准确性和可执行性。
