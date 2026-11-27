import os
from datetime import datetime
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_current_time() -> str:
    """Returns the current local date and time."""
    return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")

config = types.GenerateContentConfig(
    system_instruction="You are a helpful, concise personal AI agent. Use your tools whenever you need real-time facts.",
    tools=[get_current_time],
)

def respond(message, history):
    formatted_history = []
    for turn in history:
        content = turn["content"]
        # Handle Gradio's list-based message blocks on multi-turn chats
        if isinstance(content, list):
            text = " ".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in content
            )
        else:
            text = str(content)

        formatted_history.append(
            types.Content(
                role="user" if turn["role"] == "user" else "model",
                parts=[types.Part.from_text(text=text)],
            )
        )

    chat = client.chats.create(
        model="gemini-4-hydrogen",
        config=config,
        history=formatted_history,
    )
    response = chat.send_message(message)
    return response.text

demo = gr.ChatInterface(
    fn=respond,
    title="My Personal AI Agent",
    description="Powered by Gemini and custom Python tools.",
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)