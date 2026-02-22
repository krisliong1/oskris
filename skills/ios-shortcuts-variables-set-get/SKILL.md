# iOS Shortcuts 变量基础操作

**难度**: ⭐  
**优先级**: P0（核心必备）  
**学习时长**: 20分钟

---

## 简介

变量是Shortcuts中**最基础的数据存储机制**。就像编程中的变量一样，它让你能存储数据、在多个actions之间传递信息。

**为什么需要它？**
- 💾 临时存储数据（用户输入、计算结果等）
- 🔄 在actions之间传递信息
- 🧮 执行复杂运算
- 📝 构建动态文本

**核心概念**: Set（存）→ Get（取）→ 使用

---

## 核心概念

### 什么是变量？

在Shortcuts中，变量是**命名的数据容器**。你可以：
1. **Set Variable** - 存储数据到变量
2. **Get Variable** - 读取变量的值
3. **使用多次** - 同一个变量可以被多次读取

### 变量的生命周期

```
Shortcut开始 → Set Variable → ... → Get Variable → ... → Shortcut结束
                ↓                      ↓
              创建变量              读取变量
```

**重要**: 变量只在当前shortcut运行期间存在，运行结束后消失。

---

## 基础用法

### 1. Set Variable（设置变量）

**Action**: Set Variable  
**作用**: 将当前数据存储到命名变量中

#### 最简单的例子

```
[Text] "Hello World"
  ↓
[Set Variable] Name: MyText
  ↓
(现在"Hello World"存在变量MyText中)
```

**在Shortcuts中的操作**:
1. 添加"Set Variable" action
2. 输入变量名（如"MyText"）
3. 上一个action的输出自动成为变量的值

---

### 2. Get Variable（获取变量）

**Action**: Get Variable  
**作用**: 读取之前存储的变量值

#### 读取并使用

```
[Set Variable] Name: MyText, Value: "Hello"
  ↓
[Get Variable] MyText
  ↓
[Show Result]  ← 显示"Hello"
```

**在Shortcuts中的操作**:
1. 添加"Get Variable" action
2. 从下拉菜单选择变量名
3. 该变量的值作为输出传递给下一个action

---

### 3. 变量命名规则

#### ✅ 好的变量名

```
UserName
EmailAddress
CurrentDate
FileCount
APIResponse
```

**原则**:
- 有意义、描述性强
- 使用驼峰命名法（CamelCase）
- 避免空格和特殊字符

#### ❌ 不好的变量名

```
x
temp
var1
a
data
```

**问题**: 不知道存的是什么，难以维护

---

## 实际示例

### 示例1: 用户输入存储

```
[Ask for Input]
  Prompt: "What's your name?"
  ↓
[Set Variable] Name: UserName
  ↓
[Text] "Hello, [UserName]!"
  ↓
[Show Result]
```

**运行流程**:
1. 用户输入"Alice"
2. 存储到UserName变量
3. 在文本中使用UserName
4. 显示"Hello, Alice!"

**实际应用**: 收集用户输入，后续多处使用

---

### 示例2: 计算结果存储

```
[Number] 10
  ↓
[Calculate] × 5
  ↓
[Set Variable] Name: Result
  ↓
[Text] "10 × 5 = [Result]"
  ↓
[Show Result]  ← 显示"10 × 5 = 50"
```

**实际应用**: 存储中间计算结果，避免重复计算

---

### 示例3: 多次使用同一变量

```
[Ask for Input] "Enter a word:"
  ↓
[Set Variable] Name: Word
  ↓
[Text] "Original: [Word]"
  ↓
[Show Alert]
  ↓
[Get Variable] Word
  ↓
[Change Case] To: UPPERCASE
  ↓
[Text] "Uppercase: [Result]"
  ↓
[Show Alert]
```

**关键点**: Word变量被读取两次，用于不同目的

---

### 示例4: 变量更新

```
[Number] 0
  ↓
[Set Variable] Name: Counter
  ↓
[Get Variable] Counter
  ↓
[Calculate] + 1
  ↓
[Set Variable] Name: Counter  ← 更新变量
  ↓
[Show Result]  ← 显示1
```

**实际应用**: 计数器、累加器

---

## 变量作用域

### 局部变量（Local Variables）

通过Set Variable创建的变量是**局部的**：
- ✅ 在当前shortcut内可用
- ❌ 不能在其他shortcuts中访问
- ❌ 运行结束后消失

```
Shortcut A
  ├─ Set Variable: MyVar = "Hello"
  └─ Get Variable: MyVar  ← ✅ 可用

Shortcut B
  └─ Get Variable: MyVar  ← ❌ 不存在！
```

### 跨Shortcut传递数据

如果需要在shortcuts之间传递数据，使用：
1. **Output** - 通过"Stop and Output"返回数据
2. **Clipboard** - 使用剪贴板
3. **Files** - 保存到文件
4. **Dictionaries** - 作为参数传递

（详见`ios-shortcuts-run-shortcut` skill）

---

## 常见陷阱

### ❌ 陷阱1: 先Get后Set

```
# 错误顺序
[Get Variable] MyVar  ← 变量还不存在！
  ↓
[Set Variable] MyVar
```

**错误**: 变量不存在，Get会失败

**正确**:
```
[Set Variable] MyVar
  ↓
[Get Variable] MyVar  ← 现在存在了
```

---

### ❌ 陷阱2: 变量名拼写错误

```
[Set Variable] Name: UserName
  ↓
[Get Variable] UserNmae  ← 拼写错误！
```

**结果**: 读取不到数据，或读取到错误的变量

**解决**: 
- 使用清晰易记的名称
- 在Shortcuts中从下拉菜单选择（避免手打）

---

### ❌ 陷阱3: 变量值被覆盖

```
[Set Variable] MyVar = "First"
  ↓
(一些操作)
  ↓
[Set Variable] MyVar = "Second"  ← 覆盖了！
  ↓
[Get Variable] MyVar  ← 只能得到"Second"
```

**解决**: 
- 使用不同的变量名
- 或在覆盖前先保存旧值

---

### ❌ 陷阱4: 期望变量持久化

```
# 第一次运行
Shortcut A: Set Variable MyVar = "Data"

# 第二次运行
Shortcut A: Get Variable MyVar  ← ❌ 不存在！
```

**原因**: 变量不会在运行之间保存

**解决**: 使用文件或iCloud存储持久数据

---

## 高级技巧

### 技巧1: 使用Describe性名称

```
# 不好
[Set Variable] Name: x

# 好
[Set Variable] Name: APIResponseJSON
```

**好处**: 6个月后看代码还知道是什么

---

### 技巧2: 变量作为参数传递

```
[Set Variable] FilePath = "/Users/me/file.txt"
  ↓
[Get Variable] FilePath
  ↓
[Get File] Path: [FilePath]
```

**应用**: 配置项集中管理

---

### 技巧3: 条件赋值

```
[If] (Condition is true)
  [Set Variable] Status = "Success"
[Otherwise]
  [Set Variable] Status = "Failed"
[End If]
  ↓
[Get Variable] Status
```

**应用**: 根据条件设置不同值

---

### 技巧4: 列表/字典存储

```
[Dictionary]
  - name: "Alice"
  - age: 25
  ↓
[Set Variable] Name: UserInfo
  ↓
[Get Variable] UserInfo
  ↓
[Get Dictionary Value] Key: "name"
```

**应用**: 存储结构化数据（详见`ios-shortcuts-dictionary-basics`）

---

## 完整示例：用户信息收集

```
# 1. 收集信息
[Ask for Input] "Your name?"
  ↓
[Set Variable] Name: UserName

[Ask for Input] "Your age?"
  ↓
[Set Variable] Name: UserAge

[Choose from Menu] "Select gender:"
  - Male
  - Female
  - Other
  ↓
[Set Variable] Name: UserGender

# 2. 构建输出
[Text]
"""
=== User Profile ===
Name: [UserName]
Age: [UserAge]
Gender: [UserGender]
Created: [Current Date]
"""
  ↓
[Show Result]

# 3. 可选：保存到文件
[Get Variable] UserName
  ↓
[Text] "profile_[UserName].txt"
  ↓
[Set Variable] Name: FileName
  ↓
[Get Variable] (Profile Text)
  ↓
[Save File] Name: [FileName]
```

**应用场景**:
- 表单数据收集
- 配置信息收集
- 多步骤向导

---

## 变量 vs Magic Variables

### 区别

| 特性 | 变量（Variables） | Magic Variables |
|-----|-----------------|-----------------|
| 创建方式 | 手动Set Variable | 自动创建 |
| 命名 | 自定义名称 | 自动命名（可重命名） |
| 可见性 | 需要Get Variable | 直接可用 |
| 适用场景 | 需要明确命名时 | 快速引用上一个结果 |

### 何时用变量？

- ✅ 需要在多个地方使用同一数据
- ✅ 需要更新/累加值
- ✅ 变量名有明确业务含义
- ✅ 需要条件赋值

### 何时用Magic Variables？

- ✅ 只是引用上一个action的输出
- ✅ 不需要特殊命名
- ✅ 线性流程（不回头引用）

**建议**: 简单场景用Magic Variables，复杂场景用Set/Get Variable

（详见`ios-shortcuts-magic-variables` skill）

---

## 调试变量

### 方法1: Show Result

```
[Set Variable] MyVar = "Test"
  ↓
[Get Variable] MyVar
  ↓
[Show Result]  ← 查看变量内容
```

---

### 方法2: 添加注释Action

```
[Set Variable] UserInput
  ↓
[Comment] "Debug: UserInput should contain user's text"
  ↓
[Get Variable] UserInput
  ↓
[Show Alert] [UserInput]  ← 弹窗显示
```

---

### 方法3: 复制到剪贴板

```
[Get Variable] DebugData
  ↓
[Copy to Clipboard]
  ↓
(然后粘贴查看)
```

---

## 实战练习

### 练习1: 基础存取
创建一个shortcut：
1. 询问用户名
2. 存储到变量
3. 在3个不同的地方使用这个变量

### 练习2: 计数器
创建一个计数器shortcut：
1. 初始值为0
2. 每次加1
3. 显示当前值

### 练习3: 信息汇总
创建一个shortcut收集3个信息：
1. 名字、年龄、城市
2. 每个存储到变量
3. 最后显示汇总报告

---

## 相关Skills

### 必须配合学习
- `ios-shortcuts-magic-variables` - 更便捷的变量使用方式
- `ios-shortcuts-text-basic` - 在文本中使用变量

### 组合使用
- `ios-shortcuts-dictionary-basics` - 存储结构化数据
- `ios-shortcuts-list-operations` - 存储列表数据
- `ios-shortcuts-if-conditions` - 条件赋值

### 进阶方向
- `ios-shortcuts-repeat-loops` - 在循环中使用变量
- `ios-shortcuts-input-output-flow` - 变量与输入输出

---

## 快速参考

### Set Variable
- **位置**: Scripting → Set Variable
- **输入**: 任何数据
- **输出**: 无（但创建了变量）
- **配置**: 变量名称

### Get Variable
- **位置**: Scripting → Get Variable
- **输入**: 无
- **输出**: 变量的值
- **配置**: 选择变量名

---

**记住**: 变量是Shortcuts的基础！熟练掌握Set和Get，才能构建复杂逻辑。

**下一步**: 学习 `ios-shortcuts-magic-variables` 了解更便捷的方式

**最后更新**: 2026-02-22
