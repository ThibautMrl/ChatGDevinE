import gradio as gr
from PIL import Image

init_message = "De quelle page Wikipedia provient cette image ?"

def new_game():
    history = [gr.ChatMessage(role="assistant", content=init_message), ]
    img = Image.open(r"./Zidane.jpg")
    return history,gr.Image(img,width=300, height=200)

def chatbot_response(history, message):
    # Réponse texte + image
    history.append(gr.ChatMessage(role="user",content=message)),
    history.append(gr.ChatMessage(role="assistant", content="Ceci est une réponse."))
    return history, ""

with gr.Blocks() as demo:

    image = gr.Image(Image.open(r"./Mbappe.jpg"),width=300, height=200)
    chatbot = gr.Chatbot(
        [gr.ChatMessage(role="assistant", content=init_message), ],
        type="messages"
    )
    msg = gr.Textbox(label="",placeholder="Entrez votre question ou réponse...")
    clear = gr.Button("Nouvelle partie")

    msg.submit(chatbot_response, [chatbot, msg], [chatbot, msg])
    clear.click(fn=new_game, outputs = [chatbot,image], queue=False)

demo.launch()
