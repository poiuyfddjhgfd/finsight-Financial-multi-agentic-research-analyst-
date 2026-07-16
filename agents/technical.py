from tools.indicators import calculate_rsi, calculate_sma, calculate_macd

class TechnicalAnalystAgent:
    def __init__(self, df):
        self.df = df

    def analyze(self):
        # 1. Indicators calculate karna (latest value nikalne ke liye .iloc[-1] use karenge)
        rsi_series = calculate_rsi(self.df)
        sma_series = calculate_sma(self.df)
        macd_line, signal_line, histogram = calculate_macd(self.df)
        
        latest_price = self.df["Close"].iloc[-1]
        latest_rsi = rsi_series.iloc[-1]
        latest_sma = sma_series.iloc[-1]
        latest_macd = macd_line.iloc[-1]
        latest_signal = signal_line.iloc[-1]
        
        # 2. RSI Interpretation (with warning thresholds added)
        if latest_rsi >= 70:
            rsi_signal = "Overbought (Sell)"
        elif latest_rsi >= 65:
            rsi_signal = "Approaching Overbought (Sell Warning)"
        elif latest_rsi <= 30:
            rsi_signal = "Oversold (Buy)"
        elif latest_rsi <= 35:
            rsi_signal = "Approaching Oversold (Buy Warning)"
        else:
            rsi_signal = "Neutral"
            
        # 3. SMA Interpretation
        if latest_price > latest_sma:
            sma_signal = "Bullish (Buy)"
        else:
            sma_signal = "Bearish (Sell)"
            
        # 4. MACD Interpretation (Crossover logic)
        if latest_macd > latest_signal:
            macd_signal = "Bullish Momentum (Buy)"
        else:
            macd_signal = "Bearish Momentum (Sell)"
            
        # Structured dictionary return karna
        return {
            "current_price": round(latest_price, 2),
            "rsi": {
                "value": round(latest_rsi, 2),
                "signal": rsi_signal
            },
            "sma": {
                "value": round(latest_sma, 2),
                "signal": sma_signal
            },
            "macd": {
                "macd_line": round(latest_macd, 2),
                "signal_line": round(latest_signal, 2),
                "signal": macd_signal
            }
        }