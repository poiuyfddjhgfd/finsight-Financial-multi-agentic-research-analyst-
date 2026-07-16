import yfinance as yf

class DataCollectorAgent:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)

    def get_price_data(self, period="1mo"):
        return self.ticker.history(period=period)

    def get_company_info(self):
        return dict(self.ticker.fast_info)

    def get_financials(self):
        return self.ticker.financials

    def collect_all(self):
        return {
            "price_data": self.get_price_data(),
            "company_info": self.get_company_info(),
            "financials": self.get_financials()
        }