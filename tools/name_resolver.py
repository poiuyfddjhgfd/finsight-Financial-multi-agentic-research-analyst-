import yfinance as yf
def resolve_ticker(company_name: str):
    if not company_name:
        return None
    
    try:
        results = yf.Search(company_name).quotes
        
        if not results:
            return None
        
        # Sirf EQUITY type results filter karo, highest score wala pehla
        equity_results = [r for r in results if r.get("quoteType") == "EQUITY"]
        
        if not equity_results:
            return results[0]["symbol"]
        
        return equity_results[0]["symbol"]
        
    except Exception as e:
        print(f"Error: {e}")
        return None