import gradio as gr
from PIL import Image

history = [gr.ChatMessage(role="assistant", content="De quelle page Wikipedia provient cette image ?"),]
img = Image.open(r"./Mbappe.jpg")

def new_game():
    history = [gr.ChatMessage(role="assistant", content="De quelle page Wikipedia provient cette image ?"), ]
    img = Image.open(r"./Zidane.jpg")
    return history,gr.Image(img,width=300, height=200)

def chatbot_response(history, message):
    # Réponse texte + image
    history.append(gr.ChatMessage(role="user",content=message)),
    history.append(gr.ChatMessage(role="assistant", content="Ceci est une réponse."))
    return history, ""

with gr.Blocks() as demo:

    image = gr.Image(img,width=300, height=200)
    chatbot = gr.Chatbot(
        history,type="messages"
    )
    msg = gr.Textbox(label="",placeholder="Entrez votre question ou réponse...")
    clear = gr.Button("Nouvelle partie")

    msg.submit(chatbot_response, [chatbot, msg], [chatbot, msg])
    clear.click(fn=new_game, outputs = [chatbot,image], queue=False)

demo.launch()
