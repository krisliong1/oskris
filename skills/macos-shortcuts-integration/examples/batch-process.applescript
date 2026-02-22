-- batch-process.applescript
-- 批量处理文件夹中的文件示例
-- 用法: osascript batch-process.applescript "/path/to/folder" "快捷指令名称"

on run argv
	-- 获取参数
	if (count of argv) < 2 then
		display dialog "用法: osascript batch-process.applescript <文件夹路径> <Shortcut名称>"
		return
	end if
	
	set folderPath to item 1 of argv
	set shortcutName to item 2 of argv
	
	-- 检查文件夹是否存在
	try
		set folderPOSIX to POSIX file folderPath as alias
	on error
		display dialog "错误：文件夹不存在 - " & folderPath
		return
	end try
	
	-- 获取文件夹中的所有文件
	tell application "Finder"
		set fileList to every file of folder folderPOSIX
	end tell
	
	-- 初始化计数器
	set successCount to 0
	set errorCount to 0
	set totalCount to count of fileList
	
	-- 显示进度
	display notification "开始处理 " & totalCount & " 个文件" with title "批量处理"
	
	-- 逐个处理
	repeat with currentFile in fileList
		try
			set filePath to POSIX path of (currentFile as alias)
			
			-- 调用Shortcut
			tell application "Shortcuts Events"
				run shortcut shortcutName with input filePath
			end tell
			
			set successCount to successCount + 1
			
		on error errMsg
			log "处理失败: " & filePath & " - " & errMsg
			set errorCount to errorCount + 1
		end try
	end repeat
	
	-- 显示结果
	set resultMessage to "完成！\\n成功: " & successCount & "\\n失败: " & errorCount
	display notification resultMessage with title "批量处理完成"
	display dialog resultMessage buttons {"确定"} default button "确定"
	
end run
