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
        error = """
        <div style='background: linear-gradient(135deg, #1f1015, #110609); border-left: 4px solid #ff4d4d; border-radius: 12px; padding: 20px; color: #ff9999; font-family: "Segoe UI", sans-serif; box-shadow: 0 4px 15px rgba(255, 77, 77, 0.15);'>
            <b style='color: #ff4d4d;'>⚠️ Error:</b> Please enter a valid company name or ticker.
        </div>
        """
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
            
        # --- Modern Premium Dashboard Style Card Structure ---
        # Background: Gradient (#16213e to #0f3460), Border-left accent: #00b894 (Mint Green)
        
        # --- 1. Technical Formatting ---
        tech = report['technical_analysis']
        tech_html = f"""
        <div style="background: linear-gradient(135deg, #16213e, #0f3460); border-left: 4px solid #00b894; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 184, 148, 0.2); color: white; padding: 20px; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6;">
            <h3 style="color: #00b894; margin-top: 0; font-size: 1.3rem; border-bottom: 1px solid rgba(0,184,148,0.2); padding-bottom: 8px;">📈 Technical Insights ({ticker})</h3>
            <p style="margin: 10px 0;"><b>Current Price:</b> <span style="font-size: 1.1rem; color: #00cec9;">{c_symbol}{tech['current_price']:.2f}</span></p>
            <p style="margin: 10px 0;"><b>RSI (14):</b> {tech['rsi']['value']:.2f} — <span style="color:{'#ff7675' if 'Sell' in tech['rsi']['signal'] else '#00b894'}; font-weight: bold;">{tech['rsi']['signal']}</span></p>
            <p style="margin: 10px 0;"><b>SMA (20):</b> {tech['sma']['value']:.2f} — <b style="color: #00cec9;">{tech['sma']['signal']}</b></p>
            <p style="margin: 10px 0;"><b>MACD Status:</b> Line: {tech['macd']['macd_line']:.2f} | Signal: {tech['macd']['signal_line']:.2f} — <b style="color: #00b894;">{tech['macd']['signal']}</b></p>
        </div>
        """
        
        # --- 2. Fundamental Formatting ---
        mcap_val = fund['market_cap']
        mcap_str = f"{c_symbol}{mcap_val:,.2f} Billion" if isinstance(mcap_val, (int, float)) else str(mcap_val)
        
        fund_html = f"""
        <div style="background: linear-gradient(135deg, #16213e, #0f3460); border-left: 4px solid #00cec9; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 206, 201, 0.2); color: white; padding: 20px; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6;">
            <h3 style="color: #00cec9; margin-top: 0; font-size: 1.3rem; border-bottom: 1px solid rgba(0,206,201,0.2); padding-bottom: 8px;">📊 Fundamental Health</h3>
            <p style="margin: 10px 0;"><b>Market Cap:</b> {mcap_str}</p>
            <p style="margin: 10px 0;"><b>Revenue Growth (YoY):</b> <span style="color: {'#00b894' if fund['revenue_growth_pct'] >= 0 else '#ff7675'}; font-weight: bold;">{fund['revenue_growth_pct']:.2f}%</span></p>
            <p style="margin: 10px 0;"><b>52-Week High/Low:</b> {c_symbol}{fund['52_week_low']:.2f} - {c_symbol}{fund['52_week_high']:.2f}</p>
        </div>
        """
        
        # --- 3. Sentiment Formatting ---
        sent = report['sentiment_analysis']
        sent_color = "#00b894" if sent['sentiment'] == "Positive" else "#ff7675" if sent['sentiment'] == "Negative" else "#ffeaa7"
        
        sent_html = f"""
        <div style="background: linear-gradient(135deg, #16213e, #0f3460); border-left: 4px solid {sent_color}; border-radius: 12px; box-shadow: 0 4px 15px rgba(255, 255, 255, 0.05); color: white; padding: 20px; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6;">
            <h3 style="color: {sent_color}; margin-top: 0; font-size: 1.3rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px;">📰 Intelligence Sentiment</h3>
            <p style="margin: 10px 0;"><b>Overall Market Tone:</b> <span style="color:{sent_color}; font-weight: bold; text-transform: uppercase;">{sent['sentiment']}</span></p>
            <p style="margin: 10px 0;"><b>Avg Sentiment Score:</b> {sent['average_score']:.3f}</p>
            <p style="margin: 10px 0;"><b>Total Sample Headlines:</b> {sent['headlines_analyzed']}</p>
        </div>
        """
        
        return tech_html, fund_html, sent_html
        
    except Exception as e:
        error_msg = f"""
        <div style='background: linear-gradient(135deg, #1f1015, #110609); border-left: 4px solid #ff4d4d; border-radius: 12px; padding: 20px; color: #ff9999; font-family: "Segoe UI", sans-serif;'>
            <b style='color: #ff4d4d;'>Execution Error:</b> {str(e)}
        </div>
        """
        return error_msg, error_msg, error_msg

# --- Custom Premium Dark CSS Stylesheet Inject ---
custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%) !important;
    font-family: 'Segoe UI', Roboto, sans-serif !important;
}
.gr-button-primary {
    background: linear-gradient(90deg, #00b894, #00cec9) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    color: #0f0f1a !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
}
.gr-button-primary:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 15px rgba(0, 206, 201, 0.4) !important;
}
input, textarea {
    background-color: #16213e !important;
    border: 1px solid rgba(0, 184, 148, 0.3) !important;
    color: white !important;
    border-radius: 8px !important;
}
input:focus, textarea:focus {
    border-color: #00cec9 !important;
}
h1 {
    background: linear-gradient(90deg, #00b894, #00cec9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
}
label, p, span, th, td {
    color: #b2bec3 !important;
}
.tabs {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
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
                lines=6,
                value="Apple reports record breaking revenue this quarter\nApple faces antitrust lawsuit from European regulators"
            )
            analyze_btn = gr.Button("🚀 Run Multi-Agent Analysis", variant="primary")
            
        with gr.Column(scale=2):
            gr.Markdown("### 📋 Aggregated Analysis Reports")
            with gr.Tabs():
                with gr.TabItem("📈 Technical Analysis"):
                    tech_output = gr.HTML(value="<div style='color: #636e72; font-style: italic; padding: 10px;'>Submit data to run pipeline agents...</div>")
                with gr.TabItem("📊 Fundamental Analysis"):
                    fund_output = gr.HTML(value="<div style='color: #636e72; font-style: italic; padding: 10px;'>Submit data to run pipeline agents...</div>")
                with gr.TabItem("📰 Sentiment Analysis"):
                    sent_output = gr.HTML(value="<div style='color: #636e72; font-style: italic; padding: 10px;'>Submit data to run pipeline agents...</div>")

    # Wire up the event handler
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