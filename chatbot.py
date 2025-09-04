import gradio as gr
from PIL import Image
from orchestrator import Orchestrator
import requests
from io import BytesIO
import cairosvg

headers = {"User-Agent": "Mozilla/5.0"}
orchestrator = Orchestrator()

def new_game(categorie="random"):

    orchestrator.chose_article(categorie)
    print(orchestrator.get_image())
    response = requests.get(orchestrator.get_image(),headers=headers)
    answer = orchestrator.get_title()
    system_prompt = f"""You are an assistant that gives hints to the user. Answer questions, keeping the answer a secret. Here some context:
        {' '.join(orchestrator.get_article().split()[:30]).replace(answer, "TO_GUESS")}"""
    init_message = "Welcome!\nWhat Wikipedia article is this image from? Ask some clarification questions if you do not know what article could the image be from, or guess directly!\n"

    if orchestrator.get_image().endswith(".svg"):
        img = Image.open(BytesIO(cairosvg.svg2png(bytestring=response.content)))
    else:
        img = Image.open(BytesIO(response.content))
    history = [gr.ChatMessage(role="system", content=system_prompt), gr.ChatMessage(role="assistant", content=init_message), ]

    # img_gr = gr.Image(img,width=300, height=200,show_label=False,show_download_button=False)
    #
    # chatbot = gr.Chatbot(
    #     [gr.ChatMessage(role="assistant", content=init_message), ],
    #     type="messages",
    #     label="ChatGDviné"
    # )
    #
    # msg = gr.Textbox(label="",placeholder="Entrez votre question ou réponse...",interactive=True)
    orchestrator.is_win = False
    return history, img, gr.update("",interactive=True)


def chatbot_response(history, message):
    # Réponse texte + image
    history.append(gr.ChatMessage(role="user",content=message)),
    #history.append(gr.ChatMessage(role="assistant", content="Ceci est une réponse."))
    model_response = orchestrator.get_response_from_model(history)
    if orchestrator.is_win:
        history.append(gr.ChatMessage(role="assistant", content="Bravo vous avez trouvé !"))
    else:
        history.append(gr.ChatMessage(role="assistant", content=model_response))
    state = not orchestrator.is_win

    return history, gr.update(value="",interactive=state)

with gr.Blocks() as demo:
    #init
    history, img, _ = new_game()

    img_gr = gr.Image(img,width=300, height=200,show_label=False,show_download_button=False)

    chatbot = gr.Chatbot(
        history,
        type="messages",
        label="ChatGDviné"
    )

    msg = gr.Textbox(label="",placeholder="Entrez votre question ou réponse...",interactive=True)

    with gr.Sidebar("", open=True, position="right"):
        #slider
        categorie = gr.Dropdown(
            choices=["random","actor","movie","people","singer","writer"],
            label="Catégorie",
            interactive=True,
            value="random",
        )

    clear = gr.Button("Nouvelle partie")

    msg.submit(chatbot_response, [chatbot, msg], [chatbot, msg])
    clear.click(fn=new_game,inputs=categorie, outputs = [chatbot,img_gr,msg], queue=False)

demo.launch(share=True)
