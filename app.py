import os
import gradio as gr
from agent import respond
from config import PERSONAS

custom_css = """
footer { display: none !important; }
.header-card {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    padding: 18px 24px;
    border-radius: 14px;
    margin-bottom: 10px;
}
.header-card h1 { margin: 0; font-size: 1.5rem; color: white; }
.header-card p { margin: 4px 0 0; opacity: 0.92; font-size: 0.95rem; }
.tool-pill {
    display: inline-block;
    background: rgba(79, 70, 229, 0.12);
    border: 1px solid rgba(79, 70, 229, 0.3);
    border-radius: 999px;
    padding: 4px 10px;
    margin: 3px 2px;
    font-size: 0.82rem;
}
"""

with gr.Blocks(fill_height=True) as demo:
    with gr.Sidebar():
        gr.Markdown("### ⚙️ Agent Controls")
        persona_dropdown = gr.Dropdown(
            choices=list(PERSONAS.keys()),
            value="Concise Assistant",
            label="Response Style",
        )
        gr.Markdown("### 🔌 Active Live Tools")
        gr.HTML(
            """
            <div>
              <span class="tool-pill">🟢 System Clock</span>
              <span class="tool-pill">🟢 Open-Meteo 3-Day Weather</span>
              <span class="tool-pill">🟢 Frankfurter FX (INR)</span>
              <span class="tool-pill">🟢 Wikipedia Researcher</span>
              <span class="tool-pill">🟢 Safe Math Engine</span>
            </div>
            """
        )
        gr.Markdown(
            "---\n**Modular Architecture:**\n"
            "- `tools/` — 5 isolated Python tools\n"
            "- `agent.py` — Streaming & failover\n"
            "- `config.py` — `v1beta` SDK & personas"
        )

    gr.HTML(
        """
        <div class="header-card">
          <h1>✦ Pulse AI — Multi-Tool Workspace</h1>
          <p>Modular Python tools • Word-by-word streaming • Automatic model failover</p>
        </div>
        """
    )

    gr.ChatInterface(
        fn=respond,
        additional_inputs=[persona_dropdown],
        editable=True,
        chatbot=gr.Chatbot(
            placeholder=(
                "<div style='text-align: center; padding: 28px;'>"
                "<h3>👋 Welcome to Pulse AI</h3>"
                "<p>Pick a response style in the left sidebar or click an example below to test all 5 tools.</p>"
                "</div>"
            ),
            buttons=["copy"],
        ),
        textbox=gr.Textbox(
            placeholder="Ask about 3-day weather, live INR rates, Wikipedia topics, or math calculations...",
            container=False,
            scale=7,
        ),
        examples=[
            ["What is the current weather and 3-day forecast in Pune?", "Concise Assistant"],
            ["Look up Shaniwar Wada on Wikipedia and check Pune's weather", "Detailed Analyst"],
            ["Calculate (185000 * 0.18) / 12 and convert that INR amount to USD", "Concise Assistant"],
        ],
        fill_height=True,
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    server_name = os.environ.get("SERVER_NAME", "127.0.0.1")
    demo.launch(
        server_name=server_name,
        server_port=port,
        inbrowser=True,
        theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="slate"),
        css=custom_css,
    )
    