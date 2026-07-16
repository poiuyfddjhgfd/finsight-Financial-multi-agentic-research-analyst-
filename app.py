import gradio as gr
import numpy as np
from agents.orchestrator import FinSightOrchestrator
from tools.name_resolver import resolve_ticker

# NumPy data types (np.float64, np.int64) ko convert karne ka function taaki formatting crash na ho
def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    return obj

def analyze_stock(company_input, headlines_text):
    if not company_input:
        error = "<div style='color:#ff4d4d; background-color: #0a1a0f; padding:10px; border-radius: 4px; border: 1px solid #ff4d4d;'>Please enter a valid company name or ticker.</div>"
        return error, error, error
    
    # Headlines formatting
    headlines = [line.strip() for line in headlines_text.split('\n') if line.strip()]
    if not headlines:
        headlines = ["Market stability observed for this asset."]
        
    try:
        # Step 1: Company Name se Ticker resolve karo
        ticker = resolve_ticker(company_input)
        if not ticker:
            ticker = company_input.strip().upper()
            
        orchestrator = FinSightOrchestrator(ticker)
        report = orchestrator.run(headlines)
        
        # NumPy elements ko standard float/int mein convert kiya
        report = convert_numpy(report)
        
        # --- Dynamic Currency Mapping ---
        fund = report['fundamental_analysis']
        currency_code = fund.get('currency', 'USD')
        
        if currency_code == "USD":
            c_symbol = "$"
        elif currency_code == "INR":
            c_symbol = "₹"
        elif currency_code == "EUR":
            c_symbol = "€"
        elif currency_code == "GBP":
            c_symbol = "£"
        else:
            c_symbol = f"{currency_code} "
            
        # --- Finance Green Custom Theme Styling ---
        # Background: #0a1a0f (Dark Green), Text: #e0ffe0, Accents/Borders: #00ff88 (Bright Green)
        
        # --- 1. Technical Formatting ---
        tech = report['technical_analysis']
        tech_html = f"""
        <div style="padding: 15px; border-left: 5px solid #00ff88; background-color: #0a1a0f; color: #e0ffe0; margin-bottom: 10px; font-family: Arial, sans-serif; border-radius: 4px;">
            <h3 style="color: #00ff88; margin-top: 0;">📈 Price & Indicators ({ticker})</h3>
            <p><b>Current Price:</b> {c_symbol}{tech['current_price']:.2f}</p>
            <p><b>RSI (14):</b> {tech['rsi']['value']:.2f} — <span style="color:{'#ff4d4d' if 'Sell' in tech['rsi']['signal'] else '#00ff88'}"><b>{tech['rsi']['signal']}</b></span></p>
            <p><b>SMA (20):</b> {tech['sma']['value']:.2f} — <b style="color: #00ff88;">{tech['sma']['signal']}</b></p>
            <p><b>MACD:</b> Line: {tech['macd']['macd_line']:.2f} | Signal: {tech['macd']['signal_line']:.2f} — <b style="color: #00ff88;">{tech['macd']['signal']}</b></p>
        </div>
        """
        
        # --- 2. Fundamental Formatting ---
        mcap_val = fund['market_cap']
        mcap_str = f"{c_symbol}{mcap_val:,.2f} Billion" if isinstance(mcap_val, (int, float)) else str(mcap_val)
        
        fund_html = f"""
        <div style="padding: 15px; border-left: 5px solid #00cc66; background-color: #0a1a0f; color: #e0ffe0; margin-bottom: 10px; font-family: Arial, sans-serif; border-radius: 4px;">
            <h3 style="color: #00cc66; margin-top: 0;">📊 Company Health</h3>
            <p><b>Market Cap:</b> {mcap_str}</p>
            <p><b>Revenue Growth:</b> {fund['revenue_growth_pct']:.2f}%</p>
            <p><b>52-Week Range:</b> {c_symbol}{fund['52_week_low']:.2f} - {c_symbol}{fund['52_week_high']:.2f}</p>
        </div>
        """
        
        # --- 3. Sentiment Formatting ---
        sent = report['sentiment_analysis']
        sent_color = "#00ff88" if sent['sentiment'] == "Positive" else "#ff4d4d" if sent['sentiment'] == "Negative" else "#ff9f43"
        
        sent_html = f"""
        <div style="padding: 15px; border-left: 5px solid #00ff88; background-color: #0a1a0f; color: #e0ffe0; margin-bottom: 10px; font-family: Arial, sans-serif; border-radius: 4px;">
            <h3 style="color: #00ff88; margin-top: 0;">📰 News Sentiment</h3>
            <p><b>Overall Sentiment:</b> <span style="color:{sent_color}"><b>{sent['sentiment']}</b></span></p>
            <p><b>Average Sentiment Score:</b> {sent['average_score']:.3f}</p>
            <p><b>Headlines Analyzed:</b> {sent['headlines_analyzed']}</p>
        </div>
        """
        
        return tech_html, fund_html, sent_html
        
    except Exception as e:
        error_msg = f"<div style='color:#ff4d4d; background-color: #0a1a0f; padding:10px; font-family: Arial; border-radius: 4px; border: 1px solid #ff4d4d;'><b>Error occurred:</b> {str(e)}</div>"
        return error_msg, error_msg, error_msg

# --- Gradio UI Layout with Custom Dark Finance Dashboard Style ---
custom_css = """
.gradio-container {
    background-color: #050d07 !important;
    color: #00ff88 !important;
}
label, .gr-form, .gr-box, p, h1, h2, h3 {
    color: #e0ffe0 !important;
}
input, textarea {
    background-color: #0a1a0f !important;
    color: #ffffff !important;
    border: 1px solid #00cc66 !important;
}
button.primary {
    background: linear-gradient(45deg, #00cc66, #00ff88) !important;
    color: #050d07 !important;
    font-weight: bold !important;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🔍 FinSight: Multi-Agent Financial Analyst")
    gr.Markdown("Enter a company name or stock ticker symbol and recent news headlines to generate an aggregated research report.")
    
    with gr.Row():
        with gr.Column(scale=1):
            company_input = gr.Textbox(label="Company Name / Ticker", placeholder="e.g., Apple, Tesla, Reliance, MSFT", value="Apple")
            headlines_input = gr.TextArea(
                label="Recent Headlines (One per line)", 
                placeholder="Apple reports record breaking revenue this quarter\nApple faces antitrust lawsuit from European regulators",
                lines=5,
                value="Apple reports record breaking revenue this quarter\nApple faces antitrust lawsuit from European regulators"
            )
            analyze_btn = gr.Button("🚀 Run Multi-Agent Analysis", variant="primary")
            
        with gr.Column(scale=2):
            gr.Markdown("### 📋 Analysis Results")
            with gr.Tabs():
                with gr.TabItem("📈 Technical Analysis"):
                    tech_output = gr.HTML(value="<div style='color: #8cc499;'>Submit analysis to view technical indicators.</div>")
                with gr.TabItem("📊 Fundamental Analysis"):
                    fund_output = gr.HTML(value="<div style='color: #8cc499;'>Submit analysis to view company metrics.</div>")
                with gr.TabItem("📰 Sentiment Analysis"):
                    sent_output = gr.HTML(value="<div style='color: #8cc499;'>Submit analysis to view news sentiment.</div>")

    # Click Trigger Event
    analyze_btn.click(
        fn=analyze_stock, 
        inputs=[company_input, headlines_input], 
        outputs=[tech_output, fund_output, sent_output]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )