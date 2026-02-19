# 用户工具链说明

## 你的4个工具

### 1. Shortcut Source Helper (快捷助手)
**来源**: RoutineHub #10060 by gluebyte
**功能**: plist ↔ shortcut 双向转换（核心工具）

**用法A - plist转shortcut（Claude生成的文件导入用这个）**:
1. 把Claude生成的 .plist 文件传到iPhone
2. 用"快捷助手"打开
3. 自动转换为shortcut并签名
4. 导入到快捷指令App

**用法B - shortcut转plist（反向工程用）**:
1. 运行"快捷助手"
2. 选择一个已有的快捷指令
3. 输出其plist源码
4. 可以发给Claude分析/修改

### 2. Shortcut Source Tool (快捷方式源工具)
**来源**: RoutineHub #5256 by gluebyte
**功能**: 开发者工具

特性：
- 查看快捷指令源码
- 复制/粘贴多个action（在两个空Comment之间）
- 比较两个快捷指令的差异
- 支持从 .txt, .json, .xml, .plist, .wflow, .shortcut, iCloud链接 读取

### 3. Import shortcut (导入快捷指令)
**功能**: 直接导入 .shortcut 文件

### 4. Shortcut to XML plist
**功能**: 把现有的signed shortcut导出为XML plist格式
用于反向工程现有快捷指令

## 工作流程

### Claude创建新快捷指令
```
Claude生成 .plist → 下载到iPhone → Shortcut Source Helper打开 → 导入完成
```

### 修改现有快捷指令
```
Shortcut to XML plist 导出 → 发给Claude → Claude修改 → 保存新.plist → Source Helper导入
```

### 学习其他人的快捷指令
```
Source Tool 查看源码 → 复制相关action → 发给Claude参考
```
