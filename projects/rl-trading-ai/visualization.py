"""
可视化模块 - 生成交易报告和图表
"""

import os


def plot_training_results(env, agent, df, save_dir='output'):
    """生成训练结果图表"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("[!] matplotlib未安装，跳过图表生成")
        print("[→] 安装方法: pip install matplotlib")
        return
    
    os.makedirs(save_dir, exist_ok=True)
    
    plt.rcParams['font.size'] = 10
    fig, axes = plt.subplots(4, 1, figsize=(16, 20))
    fig.suptitle('RL Trading AI - Performance Report', fontsize=16, fontweight='bold')
    
    # ===== 1. 价格 + 买卖信号 =====
    ax1 = axes[0]
    prices = df['close'].values[:len(env.actions_history) + env.window_size]
    
    ax1.plot(prices, color='#333333', linewidth=0.8, alpha=0.9, label='Price')
    
    # 标记买卖点
    buy_steps = [t['step'] for t in env.trades if t['type'] == 'BUY']
    sell_steps = [t['step'] for t in env.trades if t['type'] == 'SELL']
    
    if buy_steps:
        buy_prices = [prices[s] if s < len(prices) else prices[-1] for s in buy_steps]
        ax1.scatter(buy_steps, buy_prices, marker='^', color='#00C853', 
                   s=100, zorder=5, label=f'BUY ({len(buy_steps)})')
    
    if sell_steps:
        sell_prices = [prices[s] if s < len(prices) else prices[-1] for s in sell_steps]
        ax1.scatter(sell_steps, sell_prices, marker='v', color='#FF1744',
                   s=100, zorder=5, label=f'SELL ({len(sell_steps)})')
    
    ax1.set_title('Price Chart + Trading Signals')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylabel('Price')
    
    # ===== 2. 资产曲线 vs 买入持有 =====
    ax2 = axes[1]
    values = np.array(env.values_history)
    
    # 买入持有基准
    start_price = prices[env.window_size]
    buy_hold = env.initial_balance * (prices[env.window_size:env.window_size+len(values)] / start_price)
    if len(buy_hold) < len(values):
        buy_hold = np.pad(buy_hold, (0, len(values) - len(buy_hold)), 'edge')
    buy_hold = buy_hold[:len(values)]
    
    ax2.plot(values, color='#2962FF', linewidth=1.5, label='AI Strategy')
    ax2.plot(buy_hold, color='#FF6D00', linewidth=1, alpha=0.7, label='Buy & Hold')
    ax2.axhline(y=env.initial_balance, color='gray', linestyle='--', alpha=0.5)
    ax2.fill_between(range(len(values)), values, env.initial_balance,
                     where=values >= env.initial_balance, alpha=0.1, color='green')
    ax2.fill_between(range(len(values)), values, env.initial_balance,
                     where=values < env.initial_balance, alpha=0.1, color='red')
    
    ax2.set_title('Portfolio Value: AI vs Buy & Hold')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylabel('Value')
    
    # ===== 3. 回撤图 =====
    ax3 = axes[2]
    peak = np.maximum.accumulate(values)
    drawdown = (peak - values) / peak * 100
    
    ax3.fill_between(range(len(drawdown)), 0, drawdown, color='#FF1744', alpha=0.3)
    ax3.plot(drawdown, color='#FF1744', linewidth=0.8)
    ax3.set_title(f'Drawdown (Max: {max(drawdown):.1f}%)')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylabel('Drawdown %')
    ax3.invert_yaxis()
    
    # ===== 4. 训练Loss曲线 =====
    ax4 = axes[3]
    if agent.losses:
        # 平滑
        window = min(100, len(agent.losses) // 5 + 1)
        losses = np.array(agent.losses)
        if len(losses) > window:
            smoothed = np.convolve(losses, np.ones(window)/window, mode='valid')
            ax4.plot(smoothed, color='#6200EA', linewidth=0.8)
        else:
            ax4.plot(losses, color='#6200EA', linewidth=0.8)
    
    ax4.set_title('Training Loss')
    ax4.grid(True, alpha=0.3)
    ax4.set_ylabel('Loss')
    ax4.set_xlabel('Training Steps')
    
    plt.tight_layout()
    
    filepath = os.path.join(save_dir, 'rl_trading_report.png')
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n[✓] 报告图表已保存: {filepath}")
    return filepath


def print_performance_report(perf, trades):
    """打印文字版交易报告"""
    print("\n" + "=" * 60)
    print("           RL TRADING AI - 策略表现报告")
    print("=" * 60)
    
    print(f"\n  总收益率:     {perf['total_return_pct']:>10.2f}%")
    print(f"  最大回撤:     {perf['max_drawdown_pct']:>10.2f}%")
    print(f"  夏普比率:     {perf['sharpe_ratio']:>10.2f}")
    print(f"  总交易次数:   {perf['total_trades']:>10d}")
    print(f"  胜率:         {perf['win_rate_pct']:>10.2f}%")
    print(f"  盈亏比:       {perf['profit_factor']:>10.2f}")
    print(f"  最终资产:     {perf['final_value']:>10,.2f}")
    
    print("\n  --- 最近10笔交易 ---")
    recent = trades[-20:]  # 最近20条记录（买+卖各10）
    for t in recent:
        if t['type'] == 'SELL':
            pnl = t.get('pnl', 0)
            pnl_pct = t.get('pnl_pct', 0)
            emoji = "🟢" if pnl > 0 else "🔴"
            print(f"  {emoji} SELL @ {t['price']:.2f}  |  PnL: {pnl:+.2f} ({pnl_pct:+.1f}%)")
        else:
            print(f"  🔵 BUY  @ {t['price']:.2f}  |  {t['shares']} shares")
    
    print("\n" + "=" * 60)
