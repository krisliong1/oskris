# RL Trading AI - 本地强化学习量化交易系统

## 这是什么？

一个**完全在你电脑本地运行**的AI量化交易系统。AI通过强化学习（DQN算法），自己从历史K线数据中学习最优的买卖策略。

### 核心特点
- ✅ **零API** - 不需要任何AI平台的API Key
- ✅ **零账号** - 不需要登录任何服务
- ✅ **零付费** - 完全免费
- ✅ **零联网**（训练时） - 下载数据后可完全离线运行
- ✅ **AI自主进化** - 强化学习让AI自己发现最优策略

---

## 快速开始

### 1. 安装依赖
```bash
pip install numpy pandas matplotlib
```

### 2. 运行（模拟数据快速演示）
```bash
python main.py
```

### 3. 用真实股票数据
```bash
# 美股
python main.py --symbol AAPL
python main.py --symbol TSLA --episodes 200

# 加密货币
python main.py --symbol BTC-USD
python main.py --symbol ETH-USD

# 港股
python main.py --symbol 0700.HK

# 本地CSV
python main.py --csv your_data.csv
```

---

## 文件结构

```
rl-trading-ai/
├── main.py           # 主程序（训练+回测+报告）
├── dqn_agent.py      # DQN强化学习Agent（纯NumPy实现）
├── trading_env.py    # 交易环境（状态/动作/奖励设计）
├── data_loader.py    # 数据加载器（Yahoo Finance/CSV/模拟）
├── visualization.py  # 可视化报告
├── requirements.txt  # 依赖
├── models/           # 训练好的模型
│   ├── best_model.json
│   └── final_model.json
└── output/           # 输出报告
    └── rl_trading_report.png
```

---

## 核心原理

### 强化学习 (Reinforcement Learning)

传统量化策略：人定规则 → AI执行
强化学习策略：AI自己从数据中学规则

```
环境(市场) ←→ Agent(AI)
  ↓               ↑
状态(K线+指标) → 动作(买/卖/持有)
  ↓               ↑
奖励(赚钱+/-亏钱)
```

### DQN (Deep Q-Network)

- Q值 = 在某状态下，执行某动作，未来能获得的总收益
- 神经网络学习预测每个动作的Q值
- 选Q值最高的动作执行
- Double DQN + Experience Replay 提升稳定性

### 状态空间（AI看到的信息）
- 过去30根K线的OHLCV
- 技术指标：MA5/10/20, RSI, MACD, 布林带, ATR
- 成交量变化率、波动率
- 当前持仓信息

### 奖励设计（AI的学习信号）
- 资产增值 → 正奖励
- 盈利平仓 → 额外奖励
- 浮亏不止损 → 惩罚
- 错过行情 → 小惩罚
- 亏损30%+ → 强制结束 + 大惩罚

---

## 参数调优

| 参数 | 默认值 | 说明 |
|------|--------|------|
| --episodes | 100 | 训练回合数，越多学越好（但更慢） |
| --lr | 0.0005 | 学习率，太大不稳定，太小学太慢 |
| --window | 30 | 看过去多少根K线 |
| --balance | 100000 | 初始资金 |

### 建议
- 初次测试：`--episodes 50` 快速看效果
- 正式训练：`--episodes 200-500`
- 数据越多效果越好：`--period 5y`

---

## ⚠️ 风险提示

**这是一个学习和研究工具，不是投资建议！**

- 历史回测表现 ≠ 未来真实表现
- AI策略也会亏钱
- 过拟合是最大风险（训练集赚钱但测试集亏钱）
- 任何投资决策请自行负责

---

## 技术栈

- **Python 3.8+**
- **NumPy** - 数值计算 + 神经网络（纯NumPy实现，不依赖PyTorch/TF）
- **Pandas** - 数据处理
- **Matplotlib** - 可视化（可选）
- **Yahoo Finance** - 免费数据源（可选，可用CSV代替）
