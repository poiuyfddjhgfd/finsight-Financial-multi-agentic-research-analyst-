from agents.data_collector import DataCollectorAgent
from agents.technical import TechnicalAnalystAgent
from agents.fundamental import FundamentalAnalystAgent
from agents.sentiment import SentimentAgent

class FinSightOrchestrator:
    def __init__(self, symbol):
        self.symbol = symbol
        # 1. Sabse pehle data collector initialize karo jo yfinance se data laaye
        self.data_collector = DataCollectorAgent(symbol)
        
        # 2. Baki agents ko initialize karo
        # Fundamental aur Sentiment ko directly symbol chahiye hota hai
        self.fundamental_agent = FundamentalAnalystAgent(symbol)
        self.sentiment_agent = SentimentAgent(symbol)
        
    def run(self, headlines: list):
        print(self.symbol, "ki analysis shuru ho rahi hai...")
        
        # Step 1: Technical analysis ke liye data collect karo
        # DataCollector se stock ka historical dataframe nikalenge
        df = self.data_collector.get_price_data(period="3mo")
        
        # Step 2: TechnicalAgent ko df pass karke initialize/run karo
        technical_agent = TechnicalAnalystAgent(df)
        technical_output = technical_agent.analyze()
        
        # Step 3: Fundamental analysis run karo
        fundamental_output = self.fundamental_agent.analyze()
        
        # Step 4: Sentiment analysis run karo (headlines pass karke)
        sentiment_output = self.sentiment_agent.analyze(headlines)
        
        # Step 5: Sabhi reports ko ek master dictionary mein merge karo
        final_report = {
            "symbol": self.symbol,
            "technical_analysis": technical_output,
            "fundamental_analysis": fundamental_output,
            "sentiment_analysis": sentiment_output
        }
        
        return final_report    