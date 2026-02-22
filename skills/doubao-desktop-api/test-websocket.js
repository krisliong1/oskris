#!/usr/bin/env node
/**
 * Doubao WebSocket 测试脚本
 * 
 * 尝试连接本地 WebSocket 服务器并分析协议
 * 
 * 安装: npm install ws
 * 运行: node test-websocket.js
 */

const WebSocket = require('ws');

const WS_URL = 'ws://127.0.0.1:49853';

/**
 * 测试 WebSocket 连接
 */
async function testWebSocket() {
  console.log('🔌 尝试连接 Doubao WebSocket...');
  console.log(`📍 地址: ${WS_URL}\n`);
  
  const ws = new WebSocket(WS_URL, {
    headers: {
      'Origin': 'chrome-extension://obkcimipmjdkghadnfcjojepocldeggd',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
  });
  
  // 连接成功
  ws.on('open', function open() {
    console.log('✅ WebSocket 连接成功！\n');
    
    // 尝试发送一些测试消息
    console.log('📤 发送测试消息...\n');
    
    // 测试 1: JSON 消息
    try {
      ws.send(JSON.stringify({
        type: 'hello',
        version: '1.0'
      }));
      console.log('✉️  发送 JSON 消息');
    } catch (e) {
      console.log('❌ JSON 消息失败:', e.message);
    }
    
    // 测试 2: 文本消息
    try {
      ws.send('hello');
      console.log('✉️  发送文本消息');
    } catch (e) {
      console.log('❌ 文本消息失败:', e.message);
    }
    
    // 测试 3: 二进制消息（尝试 Protobuf 握手）
    try {
      // 简单的二进制数据
      const buffer = Buffer.from([0x08, 0x01, 0x12, 0x04, 0x74, 0x65, 0x73, 0x74]);
      ws.send(buffer);
      console.log('✉️  发送二进制消息 (Protobuf 格式测试)');
    } catch (e) {
      console.log('❌ 二进制消息失败:', e.message);
    }
    
    console.log('\n⏳ 等待服务器响应...\n');
    
    // 5秒后如果没有响应就关闭
    setTimeout(() => {
      console.log('⏱️  5秒超时，关闭连接');
      ws.close();
    }, 5000);
  });
  
  // 接收消息
  ws.on('message', function message(data) {
    console.log('📥 收到消息:');
    console.log('─'.repeat(60));
    
    if (Buffer.isBuffer(data)) {
      console.log('类型: 二进制 (Binary)');
      console.log('长度:', data.length, 'bytes');
      console.log('Hex:', data.toString('hex'));
      console.log('内容尝试解析:');
      
      try {
        // 尝试作为 UTF-8
        console.log('  UTF-8:', data.toString('utf8'));
      } catch (e) {
        console.log('  UTF-8: 无法解析');
      }
      
      try {
        // 尝试作为 JSON
        const json = JSON.parse(data.toString());
        console.log('  JSON:', JSON.stringify(json, null, 2));
      } catch (e) {
        console.log('  JSON: 无法解析（可能是 Protobuf）');
      }
      
    } else {
      console.log('类型: 文本 (Text)');
      console.log('内容:', data);
      
      try {
        const json = JSON.parse(data);
        console.log('JSON 解析:', JSON.stringify(json, null, 2));
      } catch (e) {
        console.log('非 JSON 格式');
      }
    }
    
    console.log('─'.repeat(60) + '\n');
  });
  
  // 连接错误
  ws.on('error', function error(err) {
    console.log('\n❌ WebSocket 错误:');
    console.log('   消息:', err.message);
    console.log('   代码:', err.code);
    
    if (err.code === 'ECONNREFUSED') {
      console.log('\n💡 提示:');
      console.log('   - 确保 Doubao 桌面应用正在运行');
      console.log('   - 检查端口 49853 是否被占用');
      console.log('   - 运行 `ps aux | grep Doubao` 确认进程');
    }
  });
  
  // 连接关闭
  ws.on('close', function close(code, reason) {
    console.log('\n🔌 WebSocket 连接关闭');
    console.log('   关闭代码:', code);
    console.log('   关闭原因:', reason.toString() || '(无)');
    
    if (code === 1000) {
      console.log('   状态: 正常关闭');
    } else if (code === 1006) {
      console.log('   状态: 异常关闭（可能被服务器拒绝）');
      console.log('\n💡 可能原因:');
      console.log('   - 需要用户登录状态');
      console.log('   - 消息格式不正确');
      console.log('   - 需要特定的握手协议');
    }
  });
}

/**
 * 分析捕获的 WebSocket 消息
 * 
 * 使用方法:
 * 1. 用 Wireshark 捕获 WebSocket 流量
 * 2. 导出为 hex 格式
 * 3. 调用此函数分析
 */
function analyzeMessage(hexString) {
  console.log('🔍 分析 WebSocket 消息\n');
  
  const buffer = Buffer.from(hexString.replace(/\s/g, ''), 'hex');
  
  console.log('原始数据:');
  console.log('  Hex:', hexString);
  console.log('  长度:', buffer.length, 'bytes');
  console.log('');
  
  console.log('尝试解析:');
  
  // 1. UTF-8
  try {
    const utf8 = buffer.toString('utf8');
    console.log('  UTF-8:', utf8);
  } catch (e) {
    console.log('  UTF-8: ❌ 失败');
  }
  
  // 2. JSON
  try {
    const json = JSON.parse(buffer.toString());
    console.log('  JSON:', JSON.stringify(json, null, 2));
  } catch (e) {
    console.log('  JSON: ❌ 失败');
  }
  
  // 3. Protobuf 结构猜测
  console.log('\n  Protobuf 分析:');
  
  let offset = 0;
  while (offset < buffer.length) {
    const byte = buffer[offset];
    const fieldNumber = byte >> 3;
    const wireType = byte & 0x07;
    
    const wireTypes = ['Varint', 'Fixed64', 'Length-delimited', 'Start group', 'End group', 'Fixed32'];
    
    console.log(`    [${offset}] Field ${fieldNumber}, Type ${wireTypes[wireType] || 'Unknown'}`);
    
    if (wireType === 0) {
      // Varint
      offset++;
      let value = 0;
      let shift = 0;
      while (offset < buffer.length && (buffer[offset] & 0x80) !== 0) {
        value |= (buffer[offset] & 0x7f) << shift;
        shift += 7;
        offset++;
      }
      if (offset < buffer.length) {
        value |= buffer[offset] << shift;
        offset++;
      }
      console.log(`          → Value: ${value}`);
    } else if (wireType === 2) {
      // Length-delimited
      offset++;
      const length = buffer[offset];
      offset++;
      const data = buffer.slice(offset, offset + length);
      console.log(`          → Length: ${length}`);
      console.log(`          → Data: ${data.toString('hex')}`);
      console.log(`          → UTF-8: ${data.toString('utf8')}`);
      offset += length;
    } else {
      // 其他类型
      offset++;
      break;
    }
    
    if (offset >= buffer.length - 1) break;
  }
}

// 主程序
async function main() {
  const args = process.argv.slice(2);
  
  if (args[0] === '--analyze' && args[1]) {
    // 分析模式
    analyzeMessage(args[1]);
  } else {
    // 测试模式
    await testWebSocket();
  }
}

// 运行
if (require.main === module) {
  main().catch(error => {
    console.error('\n💥 程序错误:', error);
    process.exit(1);
  });
}

module.exports = {
  testWebSocket,
  analyzeMessage
};
