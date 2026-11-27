from google.genai import errors, types
from config import MODELS, PERSONAS, client
from tools import ALL_TOOLS


def format_history(history):
    formatted = []
    for turn in history:
        content = turn["content"]
        if isinstance(content, list):
            text = " ".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in content
            )
        else:
            text = str(content)

        formatted.append(
            types.Content(
                role="user" if turn["role"] == "user" else "model",
                parts=[types.Part.from_text(text=text)],
            )
        )
    return formatted


def respond(message, history, persona_choice):
    formatted_history = format_history(history)
    config = types.GenerateContentConfig(
        system_instruction=PERSONAS.get(persona_choice, PERSONAS["Concise Assistant"]),
        tools=ALL_TOOLS,
    )

    for model_name in MODELS:
        try:
            chat = client.chats.create(
                model=model_name,
                config=config,
                history=formatted_history,
            )
            partial_text = ""
            for chunk in chat.send_message_stream(message):
                if (
                    chunk.candidates
                    and chunk.candidates[0].content
                    and chunk.candidates[0].content.parts
                ):
                    for part in chunk.candidates[0].content.parts:
                        if part.text:
                            partial_text += part.text
                            yield partial_text
            if partial_text:
                return
        except errors.ServerError:
            continue
        except Exception as e:
            yield f"Unexpected error: {e}"
            return

    yield "Google's servers are temporarily busy across models. Please wait a few seconds and try again!"