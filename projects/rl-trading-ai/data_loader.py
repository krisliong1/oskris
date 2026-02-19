"""
数据加载器 - 获取K线数据
支持: Yahoo Finance（免费）、本地CSV
"""

import os
import urllib.request
import json
import csv
import time
from datetime import datetime, timedelta
import numpy as np


def download_yahoo_finance(symbol, period='2y', interval='1d'):
    """
    从Yahoo Finance下载免费K线数据
    
    参数:
        symbol: 股票代码, 例如 'AAPL', 'TSLA', 'BTC-USD', '0700.HK'
        period: 时间范围 ('1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
        interval: K线间隔 ('1d', '1wk', '1mo')
    
    返回:
        dict: {dates, open, high, low, close, volume}
    """
    print(f"[→] 正在从 Yahoo Finance 下载 {symbol} 数据...")
    
    # 计算时间范围
    end_time = int(time.time())
    period_map = {
        '1mo': 30, '3mo': 90, '6mo': 180,
        '1y': 365, '2y': 730, '5y': 1825, 'max': 7300
    }
    days = period_map.get(period, 730)
    start_time = end_time - days * 86400
    
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?period1={start_time}&period2={end_time}&interval={interval}"
    )
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/120.0.0.0 Safari/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"[✗] Yahoo Finance 下载失败: {e}")
        print("[→] 将使用模拟数据进行演示...")
        return None
    
    result = data.get('chart', {}).get('result', [])
    if not result:
        print(f"[✗] 未找到 {symbol} 的数据")
        return None
    
    chart = result[0]
    timestamps = chart.get('timestamp', [])
    quote = chart.get('indicators', {}).get('quote', [{}])[0]
    
    if not timestamps:
        return None
    
    dates = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d') for ts in timestamps]
    
    print(f"[✓] 成功下载 {len(dates)} 条 {symbol} K线数据")
    
    return {
        'dates': dates,
        'open': [float(x) if x else 0 for x in quote.get('open', [])],
        'high': [float(x) if x else 0 for x in quote.get('high', [])],
        'low': [float(x) if x else 0 for x in quote.get('low', [])],
        'close': [float(x) if x else 0 for x in quote.get('close', [])],
        'volume': [int(x) if x else 0 for x in quote.get('volume', [])]
    }


def load_csv(filepath):
    """
    从本地CSV文件加载数据
    CSV格式: date,open,high,low,close,volume
    """
    print(f"[→] 正在加载 {filepath}...")
    
    data = {'dates': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['dates'].append(row.get('date', row.get('Date', '')))
            data['open'].append(float(row.get('open', row.get('Open', 0))))
            data['high'].append(float(row.get('high', row.get('High', 0))))
            data['low'].append(float(row.get('low', row.get('Low', 0))))
            data['close'].append(float(row.get('close', row.get('Close', 0))))
            data['volume'].append(int(float(row.get('volume', row.get('Volume', 0)))))
    
    print(f"[✓] 加载了 {len(data['dates'])} 条K线数据")
    return data


def generate_synthetic_data(num_days=500, initial_price=100, volatility=0.02, seed=42):
    """
    生成模拟K线数据（用于离线测试）
    使用几何布朗运动 + 趋势 + 均值回归
    """
    print(f"[→] 生成 {num_days} 天模拟K线数据...")
    np.random.seed(seed)
    
    dates = []
    opens, highs, lows, closes, volumes = [], [], [], [], []
    
    price = initial_price
    trend = 0
    
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_days):
        date = start_date + timedelta(days=i)
        # 跳过周末
        if date.weekday() >= 5:
            continue
        
        dates.append(date.strftime('%Y-%m-%d'))
        
        # 趋势切换
        if np.random.random() < 0.02:
            trend = np.random.choice([-1, 0, 1]) * 0.001
        
        # 日内波动
        daily_return = trend + volatility * np.random.randn()
        
        # 均值回归（防止价格跑太远）
        if price > initial_price * 2:
            daily_return -= 0.005
        elif price < initial_price * 0.5:
            daily_return += 0.005
        
        open_price = price
        close_price = price * (1 + daily_return)
        
        # 生成高低价
        intraday_vol = abs(daily_return) + volatility * 0.5
        high_price = max(open_price, close_price) * (1 + abs(np.random.randn()) * intraday_vol * 0.5)
        low_price = min(open_price, close_price) * (1 - abs(np.random.randn()) * intraday_vol * 0.5)
        
        # 成交量
        base_vol = 1000000
        vol = int(base_vol * (1 + abs(daily_return) * 20) * (0.5 + np.random.random()))
        
        opens.append(round(open_price, 2))
        highs.append(round(high_price, 2))
        lows.append(round(low_price, 2))
        closes.append(round(close_price, 2))
        volumes.append(vol)
        
        price = close_price
    
    print(f"[✓] 生成了 {len(dates)} 条模拟K线")
    
    return {
        'dates': dates,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volumes
    }


def dict_to_dataframe_like(data):
    """
    将dict数据转换为类DataFrame对象（不依赖pandas）
    """
    import pandas as pd
    df = pd.DataFrame(data)
    if 'dates' in df.columns:
        df = df.rename(columns={'dates': 'date'})
    return df


def prepare_data(symbol=None, csv_path=None, use_synthetic=False, **kwargs):
    """
    统一数据准备接口
    
    优先级:
    1. CSV文件（如果提供）
    2. Yahoo Finance下载（如果提供symbol）
    3. 模拟数据（兜底）
    """
    import pandas as pd
    
    data = None
    
    if csv_path and os.path.exists(csv_path):
        data = load_csv(csv_path)
    elif symbol:
        data = download_yahoo_finance(symbol, **kwargs)
    
    if data is None or use_synthetic:
        synth_kwargs = {k: v for k, v in kwargs.items() 
                       if k in ('num_days', 'initial_price', 'volatility', 'seed')}
        data = generate_synthetic_data(**synth_kwargs)
    
    df = pd.DataFrame(data)
    if 'dates' in df.columns:
        df = df.rename(columns={'dates': 'date'})
    
    # 清洗
    df = df.replace(0, np.nan).dropna().reset_index(drop=True)
    
    print(f"\n[数据概要]")
    print(f"  时间范围: {df['date'].iloc[0]} → {df['date'].iloc[-1]}")
    print(f"  数据量: {len(df)} 条K线")
    print(f"  价格范围: {df['close'].min():.2f} → {df['close'].max():.2f}")
    print(f"  平均成交量: {df['volume'].mean():,.0f}")
    
    return df
