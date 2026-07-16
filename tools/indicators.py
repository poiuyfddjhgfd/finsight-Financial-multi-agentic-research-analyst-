import pandas as pd

def calculate_rsi(df, period=14):
    # 1. Consecutive rows ka difference
    delta = df["Close"].diff()
    
    # 2. Gains aur losses alag karna
    gains = delta.clip(lower=0)
    losses = (-delta).clip(lower=0)
    
    # 3. Rolling mean nikalna
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()
    
    # 4. RS aur RSI calculate karna
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_sma(df, window=20):
    # Simple Moving Average
    return df["Close"].rolling(window=window).mean()

def calculate_macd(df):
    # 1. 12-day aur 26-day EMA
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    
    # 2. MACD Line
    macd_line = ema12 - ema26
    
    # 3. Signal Line (9-day EMA of MACD Line)
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    
    # 4. Histogram
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

