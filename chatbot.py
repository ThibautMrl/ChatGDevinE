import gradio as gr
from PIL import Image
from orchestrator import Orchestrator
import requests
from io import BytesIO
import cairosvg

headers = {"User-Agent": "Mozilla/5.0"}
init_message = "De quelle page Wikipedia provient cette image ?"
orchestrator = Orchestrator()

def new_game():
    orchestrator.chose_article()
    print(orchestrator.get_image())
    response = requests.get(orchestrator.get_image(),headers=headers)

    if orchestrator.get_image().endswith(".svg"):
        img = Image.open(BytesIO(cairosvg.svg2png(bytestring=response.content)))
    else:
        img = Image.open(BytesIO(response.content))

    img_gr = gr.Image(img,width=300, height=200)

    chatbot = gr.Chatbot(
        [gr.ChatMessage(role="assistant", content=init_message), ],
        type="messages",
        label="ChatGDviné"
    )

    return chatbot, img_gr

def new_game_button():
    history,img = new_game()
    return history, gr.Image(img,label="",width=300, height=200)

def chatbot_response(history, message):
    # Réponse texte + image
    history.append(gr.ChatMessage(role="user",content=message)),
    history.append(gr.ChatMessage(role="assistant", content="Ceci est une réponse."))
    return history, ""

with gr.Blocks() as demo:
    #init
    chatbot, image = new_game()
    # chatbot = gr.Chatbot(
    #     [gr.ChatMessage(role="assistant", content=init_message), ],
    #     type="messages"
    # )
    with gr.Sidebar("", open=True, position="right"):
        #slider
        slider = gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Vues par page minimum")
        output = gr.Number(visible=False)
        slider.change(fn=lambda x: x, inputs=slider, outputs=output)

        clue = gr.Textbox(label="Indices")

    msg = gr.Textbox(label="",placeholder="Entrez votre question ou réponse...")
    clear = gr.Button("Nouvelle partie")

    msg.submit(chatbot_response, [chatbot, msg], [chatbot, msg])
    clear.click(fn=new_game, outputs = [chatbot,image], queue=False)

demo.launch(share=True)
