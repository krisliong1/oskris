#!/usr/bin/env python3
"""
=============================================================
  RL Trading AI - 本地强化学习量化交易系统
=============================================================

完全本地运行，零API，零账号，零付费
AI自己学习最优买卖策略

使用方法:

  1. 快速演示（模拟数据）:
     python main.py

  2. 真实股票数据:
     python main.py --symbol AAPL
     python main.py --symbol TSLA --period 2y
     python main.py --symbol BTC-USD

  3. 加密货币:
     python main.py --symbol BTC-USD
     python main.py --symbol ETH-USD

  4. 港股:
     python main.py --symbol 0700.HK

  5. 从CSV加载:
     python main.py --csv your_data.csv

  6. 调整参数:
     python main.py --symbol AAPL --episodes 200 --lr 0.0003

=============================================================
"""

import argparse
import os
import sys
import time
import numpy as np

# 确保能找到模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import prepare_data
from trading_env import TradingEnv
from dqn_agent import DQNAgent
from visualization import plot_training_results, print_performance_report


def train(env, agent, episodes=100, verbose=True):
    """
    训练强化学习Agent
    
    参数:
        env: 交易环境
        agent: DQN Agent
        episodes: 训练回合数
        verbose: 是否打印训练过程
    """
    best_return = -float('inf')
    returns_history = []
    
    print(f"\n{'='*60}")
    print(f"  开始训练 | Episodes: {episodes}")
    print(f"  状态维度: {env.state_dim} | 动作空间: {env.action_dim}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    for episode in range(1, episodes + 1):
        state = env.reset()
        total_reward = 0
        steps = 0
        
        while True:
            action = agent.select_action(state, training=True)
            next_state, reward, done, info = env.step(action)
            
            agent.store_transition(state, action, reward, next_state, done)
            loss = agent.learn()
            
            total_reward += reward
            state = next_state
            steps += 1
            
            if done:
                break
        
        perf = env.get_performance()
        returns_history.append(perf['total_return_pct'])
        
        # 保存最佳模型
        if perf['total_return_pct'] > best_return:
            best_return = perf['total_return_pct']
            agent.save('models/best_model.json')
        
        if verbose and episode % max(1, episodes // 20) == 0:
            elapsed = time.time() - start_time
            avg_return = np.mean(returns_history[-10:])
            print(
                f"  Episode {episode:>4d}/{episodes}"
                f"  |  Return: {perf['total_return_pct']:>7.2f}%"
                f"  |  Avg10: {avg_return:>7.2f}%"
                f"  |  Trades: {perf['total_trades']:>3d}"
                f"  |  WinRate: {perf['win_rate_pct']:>5.1f}%"
                f"  |  ε: {agent.epsilon:.3f}"
                f"  |  {elapsed:.0f}s"
            )
    
    total_time = time.time() - start_time
    print(f"\n  训练完成! 用时 {total_time:.1f}s | 最佳回报: {best_return:.2f}%")
    
    return returns_history


def backtest(env, agent, verbose=True):
    """
    回测（用训练好的模型跑一遍，不探索）
    """
    print(f"\n{'='*60}")
    print(f"  开始回测...")
    print(f"{'='*60}")
    
    state = env.reset()
    agent.epsilon = 0  # 关闭探索
    
    while True:
        action = agent.select_action(state, training=False)
        next_state, reward, done, info = env.step(action)
        state = next_state
        if done:
            break
    
    perf = env.get_performance()
    
    if verbose:
        print_performance_report(perf, env.trades)
    
    return perf


def main():
    parser = argparse.ArgumentParser(description='RL Trading AI - 本地强化学习量化交易')
    
    # 数据源
    parser.add_argument('--symbol', type=str, default=None,
                       help='股票代码 (例: AAPL, TSLA, BTC-USD, 0700.HK)')
    parser.add_argument('--csv', type=str, default=None,
                       help='本地CSV文件路径')
    parser.add_argument('--period', type=str, default='2y',
                       help='数据周期 (1mo, 3mo, 6mo, 1y, 2y, 5y)')
    parser.add_argument('--synthetic', action='store_true',
                       help='使用模拟数据')
    
    # 训练参数
    parser.add_argument('--episodes', type=int, default=100,
                       help='训练回合数 (默认100)')
    parser.add_argument('--lr', type=float, default=0.0005,
                       help='学习率 (默认0.0005)')
    parser.add_argument('--window', type=int, default=30,
                       help='观察窗口 (默认30)')
    parser.add_argument('--balance', type=float, default=100000,
                       help='初始资金 (默认100000)')
    
    # 其他
    parser.add_argument('--load', type=str, default=None,
                       help='加载已训练模型路径')
    parser.add_argument('--no-plot', action='store_true',
                       help='不生成图表')
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════════════╗
    ║        RL Trading AI v1.0                       ║
    ║        本地强化学习量化交易系统                    ║
    ║                                                  ║
    ║  ✓ 完全本地运行    ✓ 无需API Key               ║
    ║  ✓ 无需登录        ✓ 无需付费                   ║
    ║  ✓ AI自主学习      ✓ 自动优化策略               ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    # ===== 1. 加载数据 =====
    use_synthetic = args.synthetic or (args.symbol is None and args.csv is None)
    
    df = prepare_data(
        symbol=args.symbol,
        csv_path=args.csv,
        use_synthetic=use_synthetic,
        period=args.period
    )
    
    # ===== 2. 分割训练/测试数据 =====
    split_idx = int(len(df) * 0.7)
    train_df = df.iloc[:split_idx].reset_index(drop=True)
    test_df = df.iloc[split_idx:].reset_index(drop=True)
    
    print(f"\n  训练数据: {len(train_df)} 条 | 测试数据: {len(test_df)} 条")
    
    # ===== 3. 创建环境 =====
    train_env = TradingEnv(
        train_df,
        window_size=args.window,
        initial_balance=args.balance
    )
    
    test_env = TradingEnv(
        test_df,
        window_size=args.window,
        initial_balance=args.balance
    )
    
    # ===== 4. 创建Agent =====
    config = {
        'lr': args.lr,
        'hidden_dims': [256, 128, 64],
    }
    
    agent = DQNAgent(
        state_dim=train_env.state_dim,
        action_dim=train_env.action_dim,
        config=config
    )
    
    # 加载已有模型
    if args.load and os.path.exists(args.load):
        agent.load(args.load)
    
    # ===== 5. 训练 =====
    os.makedirs('models', exist_ok=True)
    returns = train(train_env, agent, episodes=args.episodes)
    
    # ===== 6. 加载最佳模型回测 =====
    best_model_path = 'models/best_model.json'
    if os.path.exists(best_model_path):
        agent.load(best_model_path)
    
    # 训练集回测
    print("\n  [训练集回测]")
    train_env_bt = TradingEnv(train_df, window_size=args.window, initial_balance=args.balance)
    train_perf = backtest(train_env_bt, agent)
    
    # 测试集回测（关键！）
    print("\n  [测试集回测 - 未见过的数据]")
    test_perf = backtest(test_env, agent)
    
    # ===== 7. 生成图表 =====
    if not args.no_plot:
        try:
            chart_path = plot_training_results(
                test_env, agent, test_df, save_dir='output'
            )
        except Exception as e:
            print(f"[!] 图表生成失败: {e}")
    
    # ===== 8. 保存最终模型 =====
    agent.save('models/final_model.json')
    
    print(f"""
    ╔══════════════════════════════════════════════════╗
    ║  完成!                                           ║
    ║                                                  ║
    ║  模型文件:  models/best_model.json               ║
    ║  报告图表:  output/rl_trading_report.png         ║
    ║                                                  ║
    ║  下次运行:                                       ║
    ║  python main.py --symbol AAPL --load models/best_model.json  ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    # ===== 9. 对比总结 =====
    print("\n  [训练集 vs 测试集对比]")
    print(f"  {'指标':<15} {'训练集':>12} {'测试集':>12}")
    print(f"  {'-'*40}")
    print(f"  {'总收益率':<13} {train_perf['total_return_pct']:>11.2f}% {test_perf['total_return_pct']:>11.2f}%")
    print(f"  {'最大回撤':<13} {train_perf['max_drawdown_pct']:>11.2f}% {test_perf['max_drawdown_pct']:>11.2f}%")
    print(f"  {'夏普比率':<13} {train_perf['sharpe_ratio']:>12.2f} {test_perf['sharpe_ratio']:>12.2f}")
    print(f"  {'胜率':<15} {train_perf['win_rate_pct']:>11.2f}% {test_perf['win_rate_pct']:>11.2f}%")
    print(f"  {'交易次数':<13} {train_perf['total_trades']:>12d} {test_perf['total_trades']:>12d}")


if __name__ == '__main__':
    main()
