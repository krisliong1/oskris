"""
交易环境 - OpenAI Gym 风格
强化学习AI在这个环境中学习买卖决策
"""

import numpy as np
import pandas as pd


class TradingEnv:
    """
    强化学习交易环境
    
    状态空间: 过去N根K线的OHLCV + 技术指标 + 持仓信息
    动作空间: 0=持有, 1=买入, 2=卖出
    奖励: 基于收益率 + 风险惩罚
    """
    
    def __init__(self, df, window_size=30, initial_balance=100000,
                 commission=0.001, max_position=1.0):
        """
        参数:
            df: DataFrame, 必须包含 open, high, low, close, volume
            window_size: 观察窗口大小（看过去多少根K线）
            initial_balance: 初始资金
            commission: 手续费率
            max_position: 最大仓位比例
        """
        self.df = df.reset_index(drop=True)
        self.window_size = window_size
        self.initial_balance = initial_balance
        self.commission = commission
        self.max_position = max_position
        
        # 预计算技术指标
        self._compute_indicators()
        
        # 状态维度
        self.state_dim = self._get_state_dim()
        self.action_dim = 3  # 持有、买入、卖出
        
        self.reset()
    
    def _compute_indicators(self):
        """计算技术指标"""
        df = self.df.copy()
        
        # 移动平均线
        df['ma5'] = df['close'].rolling(5).mean()
        df['ma10'] = df['close'].rolling(10).mean()
        df['ma20'] = df['close'].rolling(20).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / (loss + 1e-10)
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema12 = df['close'].ewm(span=12).mean()
        ema26 = df['close'].ewm(span=26).mean()
        df['macd'] = ema12 - ema26
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # 布林带
        df['bb_mid'] = df['close'].rolling(20).mean()
        bb_std = df['close'].rolling(20).std()
        df['bb_upper'] = df['bb_mid'] + 2 * bb_std
        df['bb_lower'] = df['bb_mid'] - 2 * bb_std
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / (df['bb_mid'] + 1e-10)
        
        # ATR (平均真实波幅)
        high_low = df['high'] - df['low']
        high_close = (df['high'] - df['close'].shift(1)).abs()
        low_close = (df['low'] - df['close'].shift(1)).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = tr.rolling(14).mean()
        
        # 成交量变化率
        df['volume_ratio'] = df['volume'] / (df['volume'].rolling(20).mean() + 1e-10)
        
        # 价格变化率
        df['returns'] = df['close'].pct_change()
        df['returns_5'] = df['close'].pct_change(5)
        df['returns_10'] = df['close'].pct_change(10)
        
        # 波动率
        df['volatility'] = df['returns'].rolling(20).std()
        
        # 填充NaN
        df = df.fillna(0)
        
        self.df = df
        
        # 特征列
        self.feature_cols = [
            'open', 'high', 'low', 'close', 'volume',
            'ma5', 'ma10', 'ma20',
            'rsi', 'macd', 'macd_signal', 'macd_hist',
            'bb_width', 'atr', 'volume_ratio',
            'returns', 'returns_5', 'returns_10', 'volatility'
        ]
    
    def _get_state_dim(self):
        """获取状态维度"""
        # 窗口内每根K线的特征数 + 持仓信息(3个)
        return len(self.feature_cols) * self.window_size + 3
    
    def _normalize(self, data):
        """标准化数据"""
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0) + 1e-10
        return (data - mean) / std
    
    def reset(self):
        """重置环境"""
        self.current_step = self.window_size
        self.balance = self.initial_balance
        self.shares = 0
        self.total_value = self.initial_balance
        self.entry_price = 0
        self.trades = []
        self.values_history = [self.initial_balance]
        self.actions_history = []
        
        return self._get_state()
    
    def _get_state(self):
        """获取当前状态"""
        # 获取窗口数据
        start = self.current_step - self.window_size
        end = self.current_step
        
        window_data = self.df[self.feature_cols].iloc[start:end].values
        normalized = self._normalize(window_data)
        flat = normalized.flatten()
        
        # 持仓信息
        current_price = self.df['close'].iloc[self.current_step]
        position_ratio = (self.shares * current_price) / (self.total_value + 1e-10)
        unrealized_pnl = 0
        if self.shares > 0 and self.entry_price > 0:
            unrealized_pnl = (current_price - self.entry_price) / self.entry_price
        
        portfolio_info = np.array([
            position_ratio,
            unrealized_pnl,
            self.balance / self.initial_balance
        ])
        
        state = np.concatenate([flat, portfolio_info])
        return state.astype(np.float32)
    
    def step(self, action):
        """
        执行动作
        
        参数:
            action: 0=持有, 1=买入, 2=卖出
            
        返回:
            state, reward, done, info
        """
        current_price = self.df['close'].iloc[self.current_step]
        prev_value = self.total_value
        
        reward = 0
        trade_info = None
        
        if action == 1 and self.shares == 0:  # 买入
            max_shares = int((self.balance * self.max_position) / (current_price * (1 + self.commission)))
            if max_shares > 0:
                cost = max_shares * current_price * (1 + self.commission)
                self.balance -= cost
                self.shares = max_shares
                self.entry_price = current_price
                trade_info = {
                    'type': 'BUY',
                    'price': current_price,
                    'shares': max_shares,
                    'step': self.current_step,
                    'date': self.df.index[self.current_step] if isinstance(self.df.index, pd.DatetimeIndex) else self.current_step
                }
        
        elif action == 2 and self.shares > 0:  # 卖出
            revenue = self.shares * current_price * (1 - self.commission)
            pnl = revenue - self.shares * self.entry_price * (1 + self.commission)
            self.balance += revenue
            trade_info = {
                'type': 'SELL',
                'price': current_price,
                'shares': self.shares,
                'pnl': pnl,
                'pnl_pct': (current_price - self.entry_price) / self.entry_price * 100,
                'step': self.current_step,
                'date': self.df.index[self.current_step] if isinstance(self.df.index, pd.DatetimeIndex) else self.current_step
            }
            self.shares = 0
            self.entry_price = 0
        
        if trade_info:
            self.trades.append(trade_info)
        
        # 更新总资产
        self.total_value = self.balance + self.shares * current_price
        self.values_history.append(self.total_value)
        self.actions_history.append(action)
        
        # 计算奖励
        reward = self._calculate_reward(prev_value, action, trade_info)
        
        # 前进一步
        self.current_step += 1
        done = self.current_step >= len(self.df) - 1
        
        # 如果亏损超过30%，强制结束
        if self.total_value < self.initial_balance * 0.7:
            done = True
            reward -= 5.0  # 大额惩罚
        
        info = {
            'total_value': self.total_value,
            'balance': self.balance,
            'shares': self.shares,
            'trade': trade_info
        }
        
        next_state = self._get_state() if not done else np.zeros(self.state_dim, dtype=np.float32)
        
        return next_state, reward, done, info
    
    def _calculate_reward(self, prev_value, action, trade_info):
        """
        计算奖励（关键：好的奖励函数决定AI学到什么）
        """
        # 基础奖励：资产变化率
        value_change = (self.total_value - prev_value) / prev_value
        reward = value_change * 100  # 放大
        
        # 交易奖励/惩罚
        if trade_info:
            if trade_info['type'] == 'SELL':
                if trade_info['pnl'] > 0:
                    reward += 1.0  # 盈利卖出奖励
                else:
                    reward -= 0.5  # 亏损卖出小惩罚（但止损是对的）
        
        # 持仓时的浮动盈亏
        if self.shares > 0:
            current_price = self.df['close'].iloc[self.current_step]
            unrealized = (current_price - self.entry_price) / self.entry_price
            if unrealized < -0.05:  # 浮亏超过5%
                reward -= 0.3  # 惩罚不止损
        
        # 空仓时市场上涨的机会成本
        if self.shares == 0:
            current_return = self.df['returns'].iloc[self.current_step]
            if current_return > 0.01:  # 市场涨1%+但你空仓
                reward -= 0.1
        
        return reward
    
    def get_performance(self):
        """获取策略表现"""
        values = np.array(self.values_history)
        returns = np.diff(values) / values[:-1]
        
        total_return = (values[-1] - values[0]) / values[0] * 100
        
        # 最大回撤
        peak = np.maximum.accumulate(values)
        drawdown = (peak - values) / peak
        max_drawdown = np.max(drawdown) * 100
        
        # 夏普比率（假设年化252交易日）
        if len(returns) > 1 and np.std(returns) > 0:
            sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252)
        else:
            sharpe = 0
        
        # 胜率
        winning_trades = [t for t in self.trades if t['type'] == 'SELL' and t.get('pnl', 0) > 0]
        total_sell_trades = [t for t in self.trades if t['type'] == 'SELL']
        win_rate = len(winning_trades) / max(len(total_sell_trades), 1) * 100
        
        # 盈亏比
        avg_win = np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0
        losing_trades = [t for t in self.trades if t['type'] == 'SELL' and t.get('pnl', 0) <= 0]
        avg_loss = abs(np.mean([t['pnl'] for t in losing_trades])) if losing_trades else 1
        profit_factor = avg_win / max(avg_loss, 1e-10)
        
        return {
            'total_return_pct': round(total_return, 2),
            'max_drawdown_pct': round(max_drawdown, 2),
            'sharpe_ratio': round(sharpe, 2),
            'total_trades': len(total_sell_trades),
            'win_rate_pct': round(win_rate, 2),
            'profit_factor': round(profit_factor, 2),
            'final_value': round(values[-1], 2)
        }
