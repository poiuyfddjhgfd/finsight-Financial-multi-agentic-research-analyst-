from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAgent:
    def __init__(self, symbol):
        self.symbol = symbol
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze(self, headlines: list):
        if not headlines:
            return {
                "average_score": 0.0,
                "sentiment": "Neutral",
                "headlines_analyzed": 0
            }

        scores = []
        for headline in headlines:
            score = self.analyzer.polarity_scores(headline)
            # 1. Sabse important key 'compound' hai
            scores.append(score["compound"])  
        
        avg_score = sum(scores) / len(scores)
        
        # 2. Sentiment thresholds aur labels
        if avg_score >= 0.05:
            sentiment = "Positive"
        elif avg_score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        return {
            "average_score": round(avg_score, 3),
            "sentiment": sentiment,
            "headlines_analyzed": len(headlines)
        }
    




    