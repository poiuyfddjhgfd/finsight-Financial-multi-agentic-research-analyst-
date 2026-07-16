from agents.data_collector import DataCollectorAgent

class FundamentalAnalystAgent:
    def __init__(self, symbol):
        self.collector = DataCollectorAgent(symbol)
    
    def analyze(self):
        info = self.collector.get_company_info()
        financials = self.collector.get_financials()
        
        # 1. Market Cap (fast_info dict keys)
        market_cap = info.get("marketCap", 0)
        
        # 2. Revenue Growth (0 is latest year, 1 is previous year)
        revenue_row = financials.loc["Total Revenue"]
        current_rev = revenue_row.iloc[0]
        previous_rev = revenue_row.iloc[1]
        revenue_growth = ((current_rev - previous_rev) / previous_rev) * 100
        
        # 3. 52-week performance & current price (fast_info dict keys)
        year_high = info.get("yearHigh", 0)
        year_low = info.get("yearLow", 0)
        current_price = info.get("lastPrice", 0)
        
        # 4. Currency extract karna (Default USD rakhenge agar kuch na mile)
        currency = info.get("currency", "USD")
        print(f"Currency detected: {currency}")
        
        return {
            "market_cap": round(market_cap / 1e9, 2),  # Billions mein
            "revenue_growth_pct": round(revenue_growth, 2),
            "52_week_high": round(year_high, 2),
            "52_week_low": round(year_low, 2),
            "current_price": round(current_price, 2),
            "currency": currency  
        }