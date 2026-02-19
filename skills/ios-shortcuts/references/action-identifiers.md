# iOS Shortcuts Action Identifiers Reference

完整的action标识符和参数参考。Claude生成plist时查阅。

## 文本操作

### Text (获取文本)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.gettext</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFTextActionText</key>
    <string>纯文本内容</string>
  </dict>
</dict>
```

### Comment (注释)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.comment</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFCommentActionText</key>
    <string>注释内容</string>
  </dict>
</dict>
```

### Replace Text (替换文本)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.text.replace</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFReplaceTextFind</key>
    <string>查找内容</string>
    <key>WFReplaceTextReplace</key>
    <string>替换内容</string>
    <key>WFReplaceTextRegularExpression</key>
    <false/>
    <key>WFReplaceTextCaseSensitive</key>
    <true/>
  </dict>
</dict>
```

### Split Text (分割文本)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.text.split</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFTextSeparator</key>
    <string>Custom</string>
    <key>WFTextCustomSeparator</key>
    <string>,</string>
  </dict>
</dict>
```

### Combine Text (合并文本)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.text.combine</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFTextSeparator</key>
    <string>New Line</string>
  </dict>
</dict>
```

## 网络操作

### URL
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.url</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFURLActionURL</key>
    <string>https://api.example.com/endpoint</string>
  </dict>
</dict>
```

### Get Contents of URL (HTTP请求)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.downloadurl</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFHTTPMethod</key>
    <string>POST</string>
    <key>WFHTTPHeaders</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>WFDictionaryFieldValueItems</key>
        <array>
          <dict>
            <key>WFItemType</key>
            <integer>0</integer>
            <key>WFKey</key>
            <dict>
              <key>Value</key>
              <dict>
                <key>string</key>
                <string>Content-Type</string>
              </dict>
              <key>WFSerializationType</key>
              <string>WFTextTokenString</string>
            </dict>
            <key>WFValue</key>
            <dict>
              <key>Value</key>
              <dict>
                <key>string</key>
                <string>application/json</string>
              </dict>
              <key>WFSerializationType</key>
              <string>WFTextTokenString</string>
            </dict>
          </dict>
        </array>
      </dict>
      <key>WFSerializationType</key>
      <string>WFDictionaryFieldValue</string>
    </dict>
    <key>WFHTTPBodyType</key>
    <string>Json</string>
    <key>WFJSONValues</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>WFDictionaryFieldValueItems</key>
        <array>
          <!-- JSON body fields -->
        </array>
      </dict>
      <key>WFSerializationType</key>
      <string>WFDictionaryFieldValue</string>
    </dict>
  </dict>
</dict>
```

### Open URL
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.openurl</string>
  <key>WFWorkflowActionParameters</key>
  <dict/>
</dict>
```

## 字典操作

### Dictionary
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.dictionary</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFItems</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>WFDictionaryFieldValueItems</key>
        <array>
          <dict>
            <key>WFItemType</key>
            <integer>0</integer>
            <key>WFKey</key>
            <dict>
              <key>Value</key>
              <dict><key>string</key><string>key1</string></dict>
              <key>WFSerializationType</key>
              <string>WFTextTokenString</string>
            </dict>
            <key>WFValue</key>
            <dict>
              <key>Value</key>
              <dict><key>string</key><string>value1</string></dict>
              <key>WFSerializationType</key>
              <string>WFTextTokenString</string>
            </dict>
          </dict>
        </array>
      </dict>
      <key>WFSerializationType</key>
      <string>WFDictionaryFieldValue</string>
    </dict>
  </dict>
</dict>
```

WFItemType值：0=文本, 1=布尔, 2=数字, 3=数组, 4=字典

### Get Dictionary Value
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.getvalueforkey</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFDictionaryKey</key>
    <string>keyName</string>
  </dict>
</dict>
```

### Get Dictionary from Input (JSON解析)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.detect.dictionary</string>
  <key>WFWorkflowActionParameters</key>
  <dict/>
</dict>
```

## 用户交互

### Show Alert
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.alert</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFAlertActionTitle</key>
    <string>标题</string>
    <key>WFAlertActionMessage</key>
    <string>消息内容</string>
    <key>WFAlertActionCancelButtonShown</key>
    <false/>
  </dict>
</dict>
```

### Show Notification
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.notification</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFNotificationActionTitle</key>
    <string>通知标题</string>
    <key>WFNotificationActionBody</key>
    <string>通知内容</string>
  </dict>
</dict>
```

### Ask for Input
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.ask</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFAskActionPrompt</key>
    <string>请输入内容</string>
    <key>WFInputType</key>
    <string>Text</string>
    <key>WFAskActionDefaultAnswer</key>
    <string>默认值</string>
  </dict>
</dict>
```

WFInputType: Text, Number, URL, Date, Time, Date and Time

### Choose from List
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.choosefromlist</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFChooseFromListActionPrompt</key>
    <string>请选择</string>
    <key>WFChooseFromListActionSelectMultiple</key>
    <false/>
  </dict>
</dict>
```

### Choose from Menu
```xml
<!-- 菜单开始 (WFControlFlowMode=0) -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.choosefrommenu</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>MENU-UUID</string>
    <key>WFControlFlowMode</key>
    <integer>0</integer>
    <key>WFMenuPrompt</key>
    <string>请选择操作</string>
    <key>WFMenuItems</key>
    <array>
      <string>选项1</string>
      <string>选项2</string>
      <string>选项3</string>
    </array>
  </dict>
</dict>

<!-- 选项1的action (WFControlFlowMode=1) -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.choosefrommenu</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>MENU-UUID</string>
    <key>WFControlFlowMode</key>
    <integer>1</integer>
    <key>WFMenuItemTitle</key>
    <string>选项1</string>
  </dict>
</dict>
<!-- 选项1的具体action放这里 -->

<!-- 选项2的action (WFControlFlowMode=1) -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.choosefrommenu</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>MENU-UUID</string>
    <key>WFControlFlowMode</key>
    <integer>1</integer>
    <key>WFMenuItemTitle</key>
    <string>选项2</string>
  </dict>
</dict>
<!-- 选项2的具体action放这里 -->

<!-- 菜单结束 (WFControlFlowMode=2) -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.choosefrommenu</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>MENU-UUID</string>
    <key>WFControlFlowMode</key>
    <integer>2</integer>
  </dict>
</dict>
```

## 剪贴板

### Copy to Clipboard
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.setclipboard</string>
  <key>WFWorkflowActionParameters</key>
  <dict/>
</dict>
```

### Get Clipboard
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.getclipboard</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
  </dict>
</dict>
```

## 变量

### Set Variable
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.setvariable</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFVariableName</key>
    <string>变量名</string>
  </dict>
</dict>
```

### Get Variable
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.getvariable</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFVariable</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>Type</key>
        <string>Variable</string>
        <key>VariableName</key>
        <string>变量名</string>
      </dict>
      <key>WFSerializationType</key>
      <string>WFTextTokenAttachment</string>
    </dict>
  </dict>
</dict>
```

## 脚本

### Run JavaScript on Web Page
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.runjavascript</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFJavaScript</key>
    <string>
var result = document.title;
completion(result);
    </string>
  </dict>
</dict>
```

### Wait
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.delay</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFDelayTime</key>
    <integer>3</integer>
  </dict>
</dict>
```

### Count
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.count</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFCountType</key>
    <string>Items</string>
  </dict>
</dict>
```

WFCountType: Items, Characters, Words, Sentences, Lines

### Get Item from List
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.getitemfromlist</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFItemSpecifier</key>
    <string>First Item</string>
  </dict>
</dict>
```

WFItemSpecifier: First Item, Last Item, Random Item, Item At Index

### List
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.list</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>生成UUID</string>
    <key>WFItems</key>
    <array>
      <string>项目1</string>
      <string>项目2</string>
      <string>项目3</string>
    </array>
  </dict>
</dict>
```

## 编码与转换

### Base64 Encode
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.base64encode</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFEncodeMode</key>
    <string>Encode</string>
  </dict>
</dict>
```

### URL Encode
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.urlencode</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFEncodeMode</key>
    <string>Encode</string>
  </dict>
</dict>
```

## 退出与输出

### Stop Shortcut / Exit
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.exit</string>
  <key>WFWorkflowActionParameters</key>
  <dict/>
</dict>
```

### Output (返回结果给调用者)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.output</string>
  <key>WFWorkflowActionParameters</key>
  <dict/>
</dict>
```

### Quick Look (快速查看)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.previewdocument</string>
  <key>WFWorkflowActionParameters</key>
  <dict/>
</dict>
```

### Share
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.share</string>
  <key>WFWorkflowActionParameters</key>
  <dict/>
</dict>
```

---

*此文档基于 sebj/iOS-Shortcuts-Reference, zachary7829 fileformat, cherrilang.org 等开源参考*
*最后更新: 2026-02-19*
