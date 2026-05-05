import gradio as gr
import os
from ragEngine import NLPAssistantEngine
from voiceService import VoiceService

engine = NLPAssistantEngine()
voice_service = VoiceService()

def chat_response(message, history):
    try:
        response = engine.generate_response(message)
        return response
    except Exception as e:
        return f"Вибачте, сталася помилка: {str(e)}"

async def play_audio(history):
    if not history or len(history) == 0:
        return None
    
    last_answer = None
    for msg in reversed(history):
        role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", None)
        if role == "assistant":
            last_answer = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", None)
            break
    
    if last_answer:
        audio_path = await voice_service.text_to_speech(str(last_answer))
        return audio_path
    return None

async def process_voice(audio_path):
    if audio_path is None:
        return ""
    try:
        text = await voice_service.speech_to_text(audio_path)
        return text
    except Exception as e:
        return f"Помилка розпізнавання: {str(e)}"

theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="slate",
    radius_size="lg",
).set(
    block_title_text_weight="600",
    block_label_text_weight="600",
)

with gr.Blocks(title="NLP AI Помічник", theme=theme) as demo:
    gr.Markdown(
        """
        # 🤖 NLP AI Помічник
        """
    )
    
    chatbot = gr.Chatbot(label="Історія повідомлень", height=500)
    
    with gr.Row():
        msg = gr.Textbox(
            label="Ваше запитання",
            placeholder="Наприклад: Що таке TF-IDF?",
            scale=8,
            container=True
        )
        submit_btn = gr.Button("Надіслати", variant="primary", scale=2)
    
    with gr.Row():
        audio_input = gr.Audio(
            label="Записати питання голосом", 
            sources=["microphone"], 
            type="filepath",
            scale=5
        )
        with gr.Column(scale=5):
            play_btn = gr.Button("🔊 Озвучити відповідь", variant="secondary")
            audio_output = gr.Audio(label="Голосова відповідь", autoplay=True, interactive=False)
    
    with gr.Row():
        clear_btn = gr.ClearButton([msg, chatbot, audio_output, audio_input], value="Очистити чат")

    def user_msg(user_message, history):
        history.append({"role": "user", "content": user_message})
        return "", history

    def bot_msg(history):
        user_message = history[-1]["content"]
        bot_response = chat_response(user_message, history[:-1])
        history.append({"role": "assistant", "content": bot_response})
        return history

    msg.submit(user_msg, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_msg, chatbot, chatbot
    )
    submit_btn.click(user_msg, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_msg, chatbot, chatbot
    )
    
    audio_input.stop_recording(fn=process_voice, inputs=[audio_input], outputs=[msg])
    audio_input.change(fn=process_voice, inputs=[audio_input], outputs=[msg])
    play_btn.click(fn=play_audio, inputs=[chatbot], outputs=[audio_output])

if __name__ == "__main__":
    audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "volume", "audio"))
    os.makedirs(audio_dir, exist_ok=True)
    demo.launch(allowed_paths=[audio_dir])
