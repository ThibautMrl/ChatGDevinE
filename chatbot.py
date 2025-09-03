import gradio as gr
from PIL import Image

def chatbot_response(history, message):
    # Réponse texte + image
    history.append((message, "Ceci est une réponse."))
    return history, ""

with gr.Blocks() as demo:
    img = Image.open(r"./Mbappe.jpg")
    image = gr.Image(img,width=300, height=200)
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(chatbot_response, [chatbot, msg], [chatbot, msg])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
