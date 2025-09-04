from ollama import Client
import gradio as gr

CORRECT_ANS = "mbappe"

class Chat:
    def __init__(self):
        #self.conversation_starter = {
        #    "role": "system",
        #    "content": """
        #        You are a guessing game host. The user has received an image and has to guess what Wikipedia article it comes from. They can ask you clarification questions and propose answers until they guess correctly.
        #        The CORRECT ANSWER (that will terminate the game) is: {CORRECT_ANS}
        #        The context to use for answering clarification questions: {ARTICLE_TEXT}
        #        """,
        #    }
        #self.conversation = [self.conversation_starter]

        self.model_name = "llama3.1:latest"
        self.port = 9007  # 11434
        self.client = Client(host=f"http://localhost:{self.port}")

    def _format_gr_hist(self, msg: list[dict]) -> list[gr.ChatMessage]:
        return [self._format_gr_to_msg(m) for m in msg]
    
    def _format_gr_to_msg(self, msg: gr.ChatMessage) -> dict:
        
        return {"role": msg.role, "content": msg.content}

    def _format_msg_to_gr(self, msg: dict) -> gr.ChatMessage:
        return gr.ChatMessage(role=msg["role"], content=msg["content"])

    def get_response_from_model(self, history: list[gr.ChatMessage]):
        formated_hist = self._format_gr_hist(history)
        # Stream response so you see it as it generates
        chat_response = self.client.chat(
            model=self.model_name,
            messages=formated_hist,
            stream=False,
        )
        content = chat_response["message"]["content"]
        return content #self._format_msg_to_gr(content)
