#!/usr/bin/env node
/**
 * Doubao 自动化测试脚本
 * 
 * 使用 Playwright 自动化 Doubao 网页版
 * 
 * 安装: npm install playwright
 * 运行: node test-automation.js
 */

const { chromium } = require('playwright');

// 配置
const CONFIG = {
  userDataDir: '/Users/openclaw/Library/Application Support/openclaw/browser/Default',
  doubaoUrl: 'https://www.doubao.com/chat/',
  headless: false,  // 设置为 true 可以无头运行
  timeout: 60000    // 60秒超时
};

/**
 * 向 Doubao 提问并获取回复
 * @param {string} question - 要问的问题
 * @returns {Promise<string>} - AI 的回复
 */
async function askDoubao(question) {
  console.log(`\n🤖 向 Doubao 提问: "${question}"\n`);
  
  const browser = await chromium.launchPersistentContext(CONFIG.userDataDir, {
    headless: CONFIG.headless,
    channel: 'chrome'
  });
  
  try {
    const page = await browser.newPage();
    
    // 导航到 Doubao
    console.log('📖 打开 Doubao...');
    await page.goto(CONFIG.doubaoUrl, { waitUntil: 'networkidle' });
    
    // 等待聊天输入框
    console.log('⏳ 等待页面加载...');
    const inputSelector = 'textarea, [contenteditable="true"], input[type="text"]';
    await page.waitForSelector(inputSelector, { timeout: CONFIG.timeout });
    
    // 输入问题
    console.log('✍️  输入问题...');
    await page.fill(inputSelector, question);
    
    // 发送（按 Enter 或点击发送按钮）
    console.log('📤 发送消息...');
    await page.keyboard.press('Enter');
    
    // 等待回复
    console.log('⏳ 等待 AI 回复...');
    await page.waitForTimeout(3000);  // 等待 3 秒让消息开始显示
    
    // 等待回复完成（检测"停止生成"按钮消失）
    try {
      await page.waitForFunction(() => {
        // 查找可能表示生成中的元素
        const stopButton = document.querySelector('[data-testid="stop-generate"]');
        const loadingIndicator = document.querySelector('.loading, .generating');
        return !stopButton && !loadingIndicator;
      }, { timeout: CONFIG.timeout });
    } catch (e) {
      console.log('⚠️  超时等待回复完成，将返回当前内容');
    }
    
    // 提取最后一条消息
    console.log('📥 提取回复...');
    
    // 尝试多种选择器
    const messageSelectors = [
      '[data-testid="chat-message"]',
      '.message-item',
      '.chat-message',
      '[role="article"]'
    ];
    
    let response = null;
    for (const selector of messageSelectors) {
      const messages = await page.locator(selector).all();
      if (messages.length > 0) {
        const lastMessage = messages[messages.length - 1];
        response = await lastMessage.textContent();
        break;
      }
    }
    
    if (!response) {
      // 如果都找不到，尝试截图并返回页面 HTML
      await page.screenshot({ path: 'doubao-debug.png' });
      console.log('⚠️  无法提取回复，已保存截图: doubao-debug.png');
      response = '无法提取回复（请查看截图）';
    }
    
    console.log('\n✅ 收到回复:\n');
    console.log('─'.repeat(60));
    console.log(response.trim());
    console.log('─'.repeat(60));
    
    return response.trim();
    
  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    throw error;
  } finally {
    await browser.close();
  }
}

/**
 * 批量提问
 * @param {string[]} questions - 问题数组
 */
async function askMultiple(questions) {
  const results = [];
  
  for (let i = 0; i < questions.length; i++) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`问题 ${i + 1}/${questions.length}`);
    console.log('='.repeat(60));
    
    try {
      const answer = await askDoubao(questions[i]);
      results.push({
        question: questions[i],
        answer: answer,
        success: true
      });
    } catch (error) {
      results.push({
        question: questions[i],
        error: error.message,
        success: false
      });
    }
    
    // 等待一下再问下一个问题
    if (i < questions.length - 1) {
      console.log('\n⏳ 等待 3 秒...');
      await new Promise(resolve => setTimeout(resolve, 3000));
    }
  }
  
  return results;
}

/**
 * 生成图片（如果支持）
 * @param {string} prompt - 图片描述
 */
async function generateImage(prompt) {
  console.log(`\n🎨 生成图片: "${prompt}"\n`);
  
  const browser = await chromium.launchPersistentContext(CONFIG.userDataDir, {
    headless: CONFIG.headless,
    channel: 'chrome'
  });
  
  try {
    const page = await browser.newPage();
    await page.goto(CONFIG.doubaoUrl);
    
    // 切换到图片生成模式（如果有的话）
    console.log('🔍 查找图片生成入口...');
    const imageButtonSelectors = [
      '[data-testid="image-mode"]',
      'button:has-text("画图")',
      'button:has-text("图片")'
    ];
    
    let found = false;
    for (const selector of imageButtonSelectors) {
      if (await page.locator(selector).count() > 0) {
        await page.click(selector);
        found = true;
        break;
      }
    }
    
    if (!found) {
      console.log('⚠️  未找到图片生成入口，尝试直接输入...');
    }
    
    // 输入提示词
    const inputSelector = 'textarea, [contenteditable="true"]';
    await page.waitForSelector(inputSelector);
    await page.fill(inputSelector, prompt);
    await page.keyboard.press('Enter');
    
    // 等待图片生成
    console.log('⏳ 等待图片生成（可能需要较长时间）...');
    await page.waitForTimeout(10000);  // 等待 10 秒
    
    // 尝试查找生成的图片
    const imageSelectors = [
      'img[src*="generated"]',
      '.generated-image img',
      '[data-testid="generated-image"]'
    ];
    
    let imageUrl = null;
    for (const selector of imageSelectors) {
      if (await page.locator(selector).count() > 0) {
        imageUrl = await page.locator(selector).first().getAttribute('src');
        break;
      }
    }
    
    if (imageUrl) {
      console.log('✅ 图片已生成:', imageUrl);
    } else {
      await page.screenshot({ path: 'doubao-image-debug.png' });
      console.log('⚠️  未检测到生成的图片，已保存截图');
    }
    
    return imageUrl;
    
  } finally {
    await browser.close();
  }
}

// 主程序
async function main() {
  console.log('🚀 Doubao 自动化测试');
  console.log('='.repeat(60));
  
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    // 默认测试
    console.log('📝 运行默认测试...\n');
    
    const testQuestions = [
      '用一句话解释AI是什么',
      '写一个Python的Hello World程序',
      '今天是几号？'
    ];
    
    const results = await askMultiple(testQuestions);
    
    // 总结
    console.log('\n' + '='.repeat(60));
    console.log('📊 测试总结');
    console.log('='.repeat(60));
    
    results.forEach((result, index) => {
      console.log(`\n${index + 1}. ${result.question}`);
      if (result.success) {
        console.log(`   ✅ 成功`);
      } else {
        console.log(`   ❌ 失败: ${result.error}`);
      }
    });
    
  } else if (args[0] === '--image') {
    // 图片生成测试
    const prompt = args[1] || '一只可爱的猫咪';
    await generateImage(prompt);
    
  } else {
    // 单个问题
    const question = args.join(' ');
    await askDoubao(question);
  }
  
  console.log('\n✅ 测试完成！\n');
}

// 运行
if (require.main === module) {
  main().catch(error => {
    console.error('\n💥 程序错误:', error);
    process.exit(1);
  });
}

// 导出函数供其他脚本使用
module.exports = {
  askDoubao,
  askMultiple,
  generateImage
};
