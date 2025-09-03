import gradio as gr 
from typing import List, Optional
from PIL import Image

from .wikiPage import get_random_wikipedia_page_with_image


class Orchestrator():
    def __init__(self):
        self.wiki_url : Optional[str]
        self.article : Optional[str]
        self.title : Optional[str]
        self.image : Optional[str]
        self.is_win : bool = False

    def chose_article(self):
        page = get_random_wikipedia_page_with_image()
        self.title = page.title
        _ = page.summary
        self.article = page.content.strip()
        self.image = page.images[0]

    def get_article(self) -> str:
        return self.article

    def get_image(self) -> Image:
        return self.image
    
    def get_title(self) -> str:
        raise self.title

    def _test_response(self, history : List[gr.ChatMessage]) -> bool:
        if self.title in history[-1].content:
            return True
        else:
            return False
        
    def get_response_from_model(self, history : List[gr.ChatMessage]) -> str:
        self._test_response(history)
        raise NotImplementedError
