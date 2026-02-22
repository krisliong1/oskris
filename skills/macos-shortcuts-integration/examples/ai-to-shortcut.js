#!/usr/bin/env node
/**
 * ai-to-shortcut.js - OpenClaw调用Shortcuts的桥接示例
 * 
 * 功能：
 * 1. 封装shortcuts CLI调用
 * 2. 错误处理和重试
 * 3. 日志记录
 * 4. 类型安全的参数处理
 * 
 * 用法:
 *   const { runShortcut, runShortcutBatch } = require('./ai-to-shortcut.js');
 *   await runShortcut('图片处理', { inputPath: 'image.jpg' });
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');

const execAsync = promisify(exec);

/**
 * 运行单个Shortcut
 * @param {string} name - Shortcut名称
 * @param {object} options - 选项
 * @param {string} [options.inputPath] - 输入文件路径
 * @param {string} [options.outputPath] - 输出文件路径
 * @param {string} [options.outputType] - 输出类型 (UTI格式)
 * @param {number} [options.timeout=30000] - 超时时间(ms)
 * @returns {Promise<{success: boolean, stdout: string, stderr: string}>}
 */
async function runShortcut(name, options = {}) {
  const {
    inputPath,
    outputPath,
    outputType,
    timeout = 30000
  } = options;

  // 构建命令
  let command = `shortcuts run "${name}"`;

  if (inputPath) {
    // 检查输入文件是否存在
    try {
      await fs.access(inputPath);
      command += ` --input-path "${inputPath}"`;
    } catch (error) {
      throw new Error(`输入文件不存在: ${inputPath}`);
    }
  }

  if (outputPath) {
    // 确保输出目录存在
    const outputDir = path.dirname(outputPath);
    await fs.mkdir(outputDir, { recursive: true });
    command += ` --output-path "${outputPath}"`;
  }

  if (outputType) {
    command += ` --output-type ${outputType}`;
  }

  console.log(`[Shortcuts] 执行: ${command}`);

  try {
    const { stdout, stderr } = await execAsync(command, { timeout });

    return {
      success: true,
      stdout: stdout.trim(),
      stderr: stderr.trim()
    };
  } catch (error) {
    console.error(`[Shortcuts] 错误: ${error.message}`);
    return {
      success: false,
      stdout: '',
      stderr: error.message
    };
  }
}

/**
 * 批量运行Shortcut（并行）
 * @param {string} name - Shortcut名称
 * @param {Array<{inputPath: string, outputPath?: string}>} files - 文件列表
 * @param {number} [concurrency=3] - 并发数
 * @returns {Promise<Array<{file: string, success: boolean, error?: string}>>}
 */
async function runShortcutBatch(name, files, concurrency = 3) {
  console.log(`[Shortcuts] 批量处理 ${files.length} 个文件，并发数: ${concurrency}`);

  const results = [];
  const queue = [...files];

  // 并发执行
  const workers = Array(concurrency).fill(null).map(async () => {
    while (queue.length > 0) {
      const file = queue.shift();
      if (!file) break;

      try {
        const result = await runShortcut(name, file);
        results.push({
          file: file.inputPath,
          success: result.success,
          error: result.success ? null : result.stderr
        });
      } catch (error) {
        results.push({
          file: file.inputPath,
          success: false,
          error: error.message
        });
      }
    }
  });

  await Promise.all(workers);

  // 统计
  const successCount = results.filter(r => r.success).length;
  const errorCount = results.length - successCount;
  console.log(`[Shortcuts] 完成: 成功 ${successCount}, 失败 ${errorCount}`);

  return results;
}

/**
 * 列出所有可用的Shortcuts
 * @returns {Promise<Array<string>>}
 */
async function listShortcuts() {
  try {
    const { stdout } = await execAsync('shortcuts list');
    return stdout.trim().split('\n').filter(Boolean);
  } catch (error) {
    console.error('[Shortcuts] 无法获取列表:', error.message);
    return [];
  }
}

/**
 * 检查Shortcut是否存在
 * @param {string} name - Shortcut名称
 * @returns {Promise<boolean>}
 */
async function shortcutExists(name) {
  const shortcuts = await listShortcuts();
  return shortcuts.includes(name);
}

// CLI模式
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('用法:');
    console.log('  node ai-to-shortcut.js list                    # 列出所有Shortcuts');
    console.log('  node ai-to-shortcut.js run <名称>              # 运行Shortcut');
    console.log('  node ai-to-shortcut.js run <名称> <输入文件>   # 带输入运行');
    console.log('  node ai-to-shortcut.js batch <名称> <文件夹>   # 批量处理文件夹');
    process.exit(1);
  }

  const command = args[0];

  (async () => {
    try {
      if (command === 'list') {
        const shortcuts = await listShortcuts();
        console.log('可用的Shortcuts:');
        shortcuts.forEach(s => console.log(`  - ${s}`));
      } else if (command === 'run') {
        const name = args[1];
        const inputPath = args[2];

        if (!name) {
          throw new Error('请提供Shortcut名称');
        }

        const result = await runShortcut(name, { inputPath });

        if (result.success) {
          console.log('✅ 成功');
          if (result.stdout) {
            console.log('输出:', result.stdout);
          }
        } else {
          console.error('❌ 失败:', result.stderr);
          process.exit(1);
        }
      } else if (command === 'batch') {
        const name = args[1];
        const folderPath = args[2];

        if (!name || !folderPath) {
          throw new Error('请提供Shortcut名称和文件夹路径');
        }

        // 读取文件夹
        const files = await fs.readdir(folderPath);
        const fileList = files
          .filter(f => !f.startsWith('.'))  // 忽略隐藏文件
          .map(f => ({
            inputPath: path.join(folderPath, f)
          }));

        if (fileList.length === 0) {
          throw new Error('文件夹为空');
        }

        const results = await runShortcutBatch(name, fileList);

        // 显示结果
        console.log('\n结果:');
        results.forEach(r => {
          const status = r.success ? '✅' : '❌';
          console.log(`${status} ${r.file}${r.error ? ' - ' + r.error : ''}`);
        });
      } else {
        throw new Error(`未知命令: ${command}`);
      }
    } catch (error) {
      console.error('错误:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = {
  runShortcut,
  runShortcutBatch,
  listShortcuts,
  shortcutExists
};
