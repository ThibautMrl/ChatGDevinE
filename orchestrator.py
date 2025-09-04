import gradio as gr 
from typing import List, Optional
from PIL import Image

from wikiPage import WikiInterface #get_random_wikipedia_page_with_image
from llm_interface import Chat

class Orchestrator():
    def __init__(self):
        self.wiki_url : Optional[str]
        self.article : Optional[str]
        self.title : Optional[str]
        self.image : Optional[str]
        self.is_win : bool = False
        self.chat_backbone = Chat()
        self.wiki_interface = WikiInterface()

    def chose_article(self):
        page = self.wiki_interface.get_random_page()
        self.title = page["title"]
        self.article = page["content"]
        self.image = page["image"]

    def get_article(self) -> str:
        return self.article

    def get_image(self) -> Image:
        return self.image
    
    def get_title(self) -> str:
        return self.title

    def _test_response(self, history : List[gr.ChatMessage]) -> bool:
        if self.title in history[-1].content:
            return True
        else:
            return False
        
    def get_response_from_model(self, history : List[gr.ChatMessage]) -> str:
        self._test_response(history)
        response = self.chat_backbone.get_response_from_model(history)
        return response
