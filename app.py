import gradio as gr
import numpy as np
from agents.orchestrator import FinSightOrchestrator
from tools.name_resolver import resolve_ticker


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
        err = "<div style='color:#ff6b6b;padding:20px;'>⚠️ Please enter a company name or ticker.</div>"
        return err, err, err

    headlines = [l.strip() for l in headlines_text.split('\n') if l.strip()]
    if not headlines:
        headlines = ["Market stability observed for this asset."]

    try:
        ticker = resolve_ticker(company_input) or company_input.strip().upper()
        orchestrator = FinSightOrchestrator(ticker)
        report = convert_numpy(orchestrator.run(headlines))

        fund = report['fundamental_analysis']
        currency_code = fund.get('currency', 'USD')
        c_symbol = {"USD": "$", "INR": "₹", "EUR": "€", "GBP": "£"}.get(currency_code, currency_code + " ")

        tech = report['technical_analysis']
        rsi_color = "#ff6b6b" if "Sell" in tech['rsi']['signal'] else "#51cf66"
        rev_color = "#51cf66" if fund['revenue_growth_pct'] >= 0 else "#ff6b6b"

        CARD = "background:#0d1b2a;border-radius:16px;padding:28px;font-family:'Segoe UI',sans-serif;color:#e0e6ed;border:1px solid #1e3a5f;"
        LABEL = "color:#7eb8d4;font-size:0.82rem;text-transform:uppercase;letter-spacing:0.08em;margin:0;"
        VALUE = "color:#ffffff;font-size:1.15rem;font-weight:600;margin:2px 0 18px;"
        DIVIDER = "<div style='border-top:1px solid #1e3a5f;margin:18px 0;'></div>"

        tech_html = f"""
        <div style="{CARD}">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:22px;">
                <div style="width:4px;height:28px;background:linear-gradient(180deg,#00d2ff,#3a7bd5);border-radius:2px;"></div>
                <h3 style="color:#00d2ff;margin:0;font-size:1.1rem;letter-spacing:0.04em;">TECHNICAL ANALYSIS — {ticker}</h3>
            </div>
            <p style="{LABEL}">Current Price</p>
            <p style="color:#00d2ff;font-size:1.8rem;font-weight:700;margin:2px 0 18px;">{c_symbol}{tech['current_price']:.2f}</p>
            {DIVIDER}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                <div>
                    <p style="{LABEL}">RSI (14)</p>
                    <p style="{VALUE}">{tech['rsi']['value']:.2f}</p>
                    <span style="background:{rsi_color}22;color:{rsi_color};padding:4px 10px;border-radius:20px;font-size:0.8rem;font-weight:600;">{tech['rsi']['signal']}</span>
                </div>
                <div>
                    <p style="{LABEL}">SMA (20)</p>
                    <p style="{VALUE}">{tech['sma']['value']:.2f}</p>
                    <span style="background:#51cf6622;color:#51cf66;padding:4px 10px;border-radius:20px;font-size:0.8rem;font-weight:600;">{tech['sma']['signal']}</span>
                </div>
            </div>
            {DIVIDER}
            <p style="{LABEL}">MACD</p>
            <p style="{VALUE}">Line: {tech['macd']['macd_line']:.2f} &nbsp;|&nbsp; Signal: {tech['macd']['signal_line']:.2f}</p>
            <span style="background:#3a7bd522;color:#00d2ff;padding:4px 10px;border-radius:20px;font-size:0.8rem;font-weight:600;">{tech['macd']['signal']}</span>
        </div>
        """

        fund_html = f"""
        <div style="{CARD}">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:22px;">
                <div style="width:4px;height:28px;background:linear-gradient(180deg,#51cf66,#2f9e44);border-radius:2px;"></div>
                <h3 style="color:#51cf66;margin:0;font-size:1.1rem;letter-spacing:0.04em;">FUNDAMENTAL ANALYSIS</h3>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                <div>
                    <p style="{LABEL}">Market Cap</p>
                    <p style="{VALUE}">{c_symbol}{fund['market_cap']:,.1f}B</p>
                </div>
                <div>
                    <p style="{LABEL}">Revenue Growth (YoY)</p>
                    <p style="color:{rev_color};font-size:1.15rem;font-weight:700;margin:2px 0 18px;">{'▲' if fund['revenue_growth_pct'] >= 0 else '▼'} {abs(fund['revenue_growth_pct']):.2f}%</p>
                </div>
            </div>
            {DIVIDER}
            <p style="{LABEL}">52-Week Range</p>
            <div style="display:flex;align-items:center;gap:12px;margin-top:6px;">
                <span style="color:#ff6b6b;font-weight:600;">Low: {c_symbol}{fund['52_week_low']:.2f}</span>
                <div style="flex:1;height:4px;background:linear-gradient(90deg,#ff6b6b,#51cf66);border-radius:2px;"></div>
                <span style="color:#51cf66;font-weight:600;">High: {c_symbol}{fund['52_week_high']:.2f}</span>
            </div>
        </div>
        """

        sent = report['sentiment_analysis']
        sent_color = {"Positive": "#51cf66", "Negative": "#ff6b6b"}.get(sent['sentiment'], "#ffd43b")
        sent_icon = {"Positive": "▲", "Negative": "▼"}.get(sent['sentiment'], "●")
        score_bar = max(0, min(100, int((sent['average_score'] + 1) * 50)))

        sent_html = f"""
        <div style="{CARD}">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:22px;">
                <div style="width:4px;height:28px;background:linear-gradient(180deg,{sent_color},{sent_color}88);border-radius:2px;"></div>
                <h3 style="color:{sent_color};margin:0;font-size:1.1rem;letter-spacing:0.04em;">SENTIMENT ANALYSIS</h3>
            </div>
            <div style="text-align:center;padding:16px 0;">
                <div style="font-size:3rem;font-weight:800;color:{sent_color};">{sent_icon} {sent['sentiment'].upper()}</div>
                <div style="color:#7eb8d4;font-size:0.9rem;margin-top:4px;">Based on {sent['headlines_analyzed']} headlines</div>
            </div>
            {DIVIDER}
            <p style="{LABEL}">Sentiment Score</p>
            <div style="background:#1e3a5f;border-radius:8px;height:8px;margin:10px 0;">
                <div style="background:{sent_color};width:{score_bar}%;height:100%;border-radius:8px;transition:width 0.5s;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;color:#7eb8d4;font-size:0.75rem;">
                <span>Bearish -1.0</span>
                <span style="color:{sent_color};font-weight:600;">{sent['average_score']:.3f}</span>
                <span>Bullish +1.0</span>
            </div>
        </div>
        """

        return tech_html, fund_html, sent_html

    except Exception as e:
        err = f"<div style='background:#1a0a0a;border:1px solid #ff6b6b;border-radius:12px;padding:20px;color:#ff6b6b;'><b>Error:</b> {str(e)}</div>"
        return err, err, err


css = """
* { box-sizing: border-box; }
body, .gradio-container {
    background: #060e1a !important;
    color: #e0e6ed !important;
}
.gradio-container { max-width: 1200px !important; margin: 0 auto !important; }
input, textarea, .gr-textbox textarea, .gr-textbox input {
    background: #0d1b2a !important;
    color: #e0e6ed !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
    font-family: 'Segoe UI', sans-serif !important;
}
input:focus, textarea:focus {
    border-color: #00d2ff !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(0,210,255,0.15) !important;
}
label span, .gr-form label {
    color: #7eb8d4 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
button.primary {
    background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important;
    color: #060e1a !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 14px !important;
    transition: opacity 0.2s !important;
}
button.primary:hover { opacity: 0.88 !important; }
.tabs { border-color: #1e3a5f !important; }
.tab-nav button {
    color: #7eb8d4 !important;
    background: transparent !important;
    border: none !important;
    font-size: 0.9rem !important;
}
.tab-nav button.selected {
    color: #00d2ff !important;
    border-bottom: 2px solid #00d2ff !important;
}
.gr-panel, .gr-box, .panel, .block {
    background: transparent !important;
    border: none !important;
}
h1 { color: #00d2ff !important; font-size: 1.8rem !important; font-weight: 800 !important; }
p { color: #7eb8d4 !important; }
"""

with gr.Blocks(css=css, title="FinSight") as demo:
    gr.HTML("""
    <div style="padding:24px 0 8px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:6px;height:40px;background:linear-gradient(180deg,#00d2ff,#3a7bd5);border-radius:3px;"></div>
            <div>
                <h1 style="margin:0;color:#00d2ff;font-size:1.8rem;font-weight:800;letter-spacing:0.02em;">FinSight</h1>
                <p style="margin:0;color:#7eb8d4;font-size:0.85rem;">Multi-Agent Financial Research Analyst</p>
            </div>
        </div>
    </div>
    """)

    with gr.Row(equal_height=False):
        with gr.Column(scale=1, min_width=280):
            company_input = gr.Textbox(
                label="Company Name / Ticker",
                placeholder="Apple, Tesla, Reliance, MSFT...",
                value="Apple"
            )
            headlines_input = gr.TextArea(
                label="Recent Headlines (one per line)",
                placeholder="Apple reports record breaking revenue\nApple faces antitrust lawsuit...",
                lines=6,
                value="Apple reports record breaking revenue this quarter\nApple faces antitrust lawsuit from European regulators"
            )
            analyze_btn = gr.Button("Run Analysis →", variant="primary")

        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.TabItem("Technical"):
                    tech_output = gr.HTML("<div style='color:#1e3a5f;padding:40px;text-align:center;font-size:0.9rem;'>Run analysis to view results</div>")
                with gr.TabItem("Fundamental"):
                    fund_output = gr.HTML("<div style='color:#1e3a5f;padding:40px;text-align:center;font-size:0.9rem;'>Run analysis to view results</div>")
                with gr.TabItem("Sentiment"):
                    sent_output = gr.HTML("<div style='color:#1e3a5f;padding:40px;text-align:center;font-size:0.9rem;'>Run analysis to view results</div>")

    analyze_btn.click(
        fn=analyze_stock,
        inputs=[company_input, headlines_input],
        outputs=[tech_output, fund_output, sent_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)