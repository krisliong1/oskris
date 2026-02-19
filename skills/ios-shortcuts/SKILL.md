---
name: ios-shortcuts
description: >-
  创建和生成iOS/iPadOS/macOS快捷指令。Claude生成XML plist源码，用户通过
  Shortcut Source Helper工具导入到设备。支持所有快捷指令action类型：
  HTTP请求、文本处理、条件判断、循环、变量、通知、剪贴板、文件操作、
  URL Scheme、字典操作等。当用户说"做一个快捷指令"、"创建shortcut"、
  "自动化XX操作"、"iOS automation"时触发。也适用于修改现有快捷指令源码。
---

# iOS Shortcuts Creator

Claude直接生成iOS快捷指令的XML plist源码，用户通过工具链导入到设备。

## 用户工具链（已安装在用户设备上）

| 工具 | 用途 | 来源 |
|------|------|------|
| **Shortcut Source Helper** | plist ↔ shortcut 双向转换（核心工具） | RoutineHub #10060 by gluebyte |
| **Shortcut Source Tool** | 开发者工具：查看/编辑/比较源码、复制action | RoutineHub #5256 by gluebyte |
| **Import shortcut** | 直接导入快捷指令文件 | 配套工具 |
| **Shortcut to XML plist** | 把现有shortcut导出为XML plist | 反向工程用 |

## 核心工作流

```
用户需求 → Claude生成XML plist → 保存为.plist文件
  → 用户在iOS打开 → Shortcut Source Helper自动转换+签名
  → 快捷指令就绪 ✅
```

### 具体步骤
1. Claude生成完整的XML plist代码
2. 保存为 `.plist` 文件（通过 /mnt/user-data/outputs/）
3. 用户在iOS设备上打开该文件
4. Shortcut Source Helper自动处理：转换为shortcut → 签名 → 导入
5. 如果在Mac上：`shortcuts sign` CLI工具也可以签名

## Plist文件结构（必须严格遵循）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <!-- 图标 -->
  <key>WFWorkflowIcon</key>
  <dict>
    <key>WFWorkflowIconGlyphNumber</key>
    <integer>61440</integer>
    <key>WFWorkflowIconStartColor</key>
    <integer>4282601983</integer>
  </dict>

  <!-- 输入类型 -->
  <key>WFWorkflowInputContentItemClasses</key>
  <array>
    <string>WFStringContentItem</string>
  </array>

  <!-- 出现位置 -->
  <key>WFWorkflowTypes</key>
  <array>
    <string>NCWidget</string>
    <string>WatchKit</string>
  </array>

  <!-- 导入问题（可选） -->
  <key>WFWorkflowImportQuestions</key>
  <array/>

  <!-- 核心：动作数组 -->
  <key>WFWorkflowActions</key>
  <array>
    <!-- 所有action放这里 -->
  </array>

  <!-- 版本信息 -->
  <key>WFWorkflowMinimumClientVersionString</key>
  <string>900</string>
  <key>WFWorkflowMinimumClientVersion</key>
  <integer>900</integer>
  <key>WFWorkflowClientVersion</key>
  <integer>2702</integer>
</dict>
</plist>
```

## Action基本格式

每个action都是一个dict，包含identifier和parameters：

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.XXXXX</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <!-- 参数 -->
  </dict>
</dict>
```

## 常用Action速查

详见 `references/action-identifiers.md`，这里列出最常用的：

### 文本与变量
| Action | Identifier | 关键参数 |
|--------|-----------|---------|
| 文本 | `is.workflow.actions.gettext` | WFTextActionText |
| 数字 | `is.workflow.actions.number` | WFNumberActionNumber |
| 设置变量 | `is.workflow.actions.setvariable` | WFVariableName |
| 获取变量 | `is.workflow.actions.getvariable` | WFVariable |
| 注释 | `is.workflow.actions.comment` | WFCommentActionText |

### 流程控制
| Action | Identifier | 关键参数 |
|--------|-----------|---------|
| If条件 | `is.workflow.actions.conditional` | GroupingIdentifier, WFCondition, WFControlFlowMode(0=if,1=else,2=endif) |
| 重复 | `is.workflow.actions.repeat.count` | GroupingIdentifier, WFRepeatCount, WFControlFlowMode(0=start,2=end) |
| 每项重复 | `is.workflow.actions.repeat.each` | GroupingIdentifier, WFInput, WFControlFlowMode |
| 选择菜单 | `is.workflow.actions.choosefrommenu` | GroupingIdentifier, WFMenuItems, WFControlFlowMode |

### 网络与数据
| Action | Identifier | 关键参数 |
|--------|-----------|---------|
| URL | `is.workflow.actions.url` | WFURLActionURL |
| HTTP请求 | `is.workflow.actions.downloadurl` | WFHTTPMethod, WFHTTPHeaders, WFHTTPBodyType, WFRequestVariable |
| 获取URL内容 | `is.workflow.actions.getwebpagecontents` | — |
| 获取字典值 | `is.workflow.actions.getvalueforkey` | WFDictionaryKey |
| JSON解析 | `is.workflow.actions.detect.dictionary` | — |

### 用户交互
| Action | Identifier | 关键参数 |
|--------|-----------|---------|
| 显示提醒 | `is.workflow.actions.alert` | WFAlertActionMessage, WFAlertActionTitle |
| 显示通知 | `is.workflow.actions.notification` | WFNotificationActionBody, WFNotificationActionTitle |
| 要求输入 | `is.workflow.actions.ask` | WFAskActionPrompt, WFInputType |
| 从列表选择 | `is.workflow.actions.choosefromlist` | WFChooseFromListActionPrompt |
| 快速查看 | `is.workflow.actions.previewdocument` | — |

### 剪贴板与分享
| Action | Identifier | 关键参数 |
|--------|-----------|---------|
| 复制到剪贴板 | `is.workflow.actions.setclipboard` | — |
| 获取剪贴板 | `is.workflow.actions.getclipboard` | — |
| 分享 | `is.workflow.actions.share` | — |
| 打开URL | `is.workflow.actions.openurl` | — |

### 脚本
| Action | Identifier | 关键参数 |
|--------|-----------|---------|
| 运行JavaScript | `is.workflow.actions.runjavascript` | WFJavaScript |
| Base64编码 | `is.workflow.actions.base64encode` | WFEncodeMode(Encode/Decode) |
| URL编码 | `is.workflow.actions.urlencode` | WFEncodeMode |
| 哈希 | `is.workflow.actions.hash` | WFHashType |
| 退出快捷指令 | `is.workflow.actions.exit` | — |
| 无操作 | `is.workflow.actions.nothing` | — |

## 变量引用系统（关键！）

### UUID引用
每个action可以有UUID，后续action通过OutputUUID引用其输出：

```xml
<!-- 定义：有UUID的action -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.gettext</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>A1B2C3D4-E5F6-7890-ABCD-EF1234567890</string>
    <key>WFTextActionText</key>
    <string>Hello World</string>
  </dict>
</dict>

<!-- 引用：使用OutputUUID -->
<key>WFInput</key>
<dict>
  <key>Value</key>
  <dict>
    <key>OutputUUID</key>
    <string>A1B2C3D4-E5F6-7890-ABCD-EF1234567890</string>
    <key>OutputName</key>
    <string>Text</string>
    <key>Type</key>
    <string>ActionOutput</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenAttachment</string>
</dict>
```

### 内联变量（字符串内嵌变量）
在文本中嵌入变量引用，使用 `attachmentsByRange`：

```xml
<key>WFTextActionText</key>
<dict>
  <key>Value</key>
  <dict>
    <key>attachmentsByRange</key>
    <dict>
      <key>{0, 1}</key>
      <dict>
        <key>OutputUUID</key>
        <string>UUID-HERE</string>
        <key>OutputName</key>
        <string>Variable Name</string>
        <key>Type</key>
        <string>ActionOutput</string>
      </dict>
    </dict>
    <key>string</key>
    <string>￼ is the value</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenString</string>
</dict>
```

**重要**：`{0, 1}` 中的位置对应string中的 `￼`（U+FFFC Object Replacement Character）。

### 魔术变量
| 类型 | Type值 |
|------|--------|
| Action输出 | ActionOutput |
| 快捷指令输入 | ExtensionInput |
| 剪贴板 | Clipboard |
| 当前日期 | CurrentDate |
| 重复索引 | WFRepeatEachCurrentItem / WFRepeatIndex |
| 询问输入 | Ask |

## 流程控制详解

### If/Else/EndIf
同一个GroupingIdentifier串联：

```xml
<!-- If (WFControlFlowMode=0) -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.conditional</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>SAME-UUID-FOR-ALL-THREE</string>
    <key>WFControlFlowMode</key>
    <integer>0</integer>
    <key>WFCondition</key>
    <integer>4</integer>
    <key>WFConditionalActionString</key>
    <string>比较值</string>
  </dict>
</dict>

<!-- 中间放if-true的action -->

<!-- Else (WFControlFlowMode=1) -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.conditional</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>SAME-UUID-FOR-ALL-THREE</string>
    <key>WFControlFlowMode</key>
    <integer>1</integer>
  </dict>
</dict>

<!-- 中间放else的action -->

<!-- EndIf (WFControlFlowMode=2) -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.conditional</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>SAME-UUID-FOR-ALL-THREE</string>
    <key>WFControlFlowMode</key>
    <integer>2</integer>
  </dict>
</dict>
```

### WFCondition 条件类型
| 值 | 含义 |
|----|------|
| 0 | 等于 |
| 1 | 不等于 |
| 2 | 大于 |
| 3 | 大于等于 |
| 4 | 小于 |
| 5 | 小于等于 |
| 99 | 包含 |
| 999 | 不包含 |
| 100 | 开头是 |
| 101 | 结尾是 |

## 图标颜色值

| 颜色 | 值 |
|------|------|
| 红色 | 4282601983 |
| 深橙 | 4251333119 |
| 橙色 | 4271458559 |
| 黄色 | 4274264319 |
| 绿色 | 4292093695 |
| 浅蓝 | 431817727 |
| 蓝色 | 463140863 |
| 深蓝 | 946986751 |
| 紫色 | 2071128575 |
| 深灰 | 3679049983 |

## 输出规则

1. **必须生成完整、可直接使用的XML plist**，不能有占位符
2. **UUID必须唯一**，使用标准格式（8-4-4-4-12）
3. **保存为.plist文件**到 `/mnt/user-data/outputs/`
4. **告诉用户**：用Shortcut Source Helper打开这个文件即可导入
5. 复杂快捷指令先列出action流程让用户确认，再生成代码

## 限制与注意

- Claude无法直接签名shortcut文件（需要Apple私钥），只生成plist源码
- 某些高级action（如Shortcuts Events、App Intents）的参数结构可能不在此文档中
- 遇到不确定的action → 搜索验证，或让用户用Shortcut to XML plist导出类似shortcut的源码给Claude参考
- 内联变量中的U+FFFC字符在某些编辑器中不可见，但必须存在

## 快速参考

生成plist前的检查清单：
- [ ] XML声明和DOCTYPE正确
- [ ] WFWorkflowActions数组完整
- [ ] 所有GroupingIdentifier正确配对（if/else/endif, repeat start/end）
- [ ] UUID全部唯一且格式正确
- [ ] 变量引用的OutputUUID对应正确的源action
- [ ] WFControlFlowMode值正确（0=开始, 1=else, 2=结束）
- [ ] 没有占位符，所有值都是真实的
