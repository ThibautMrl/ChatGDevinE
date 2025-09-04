import gradio as gr 
from typing import List, Optional
from PIL import Image

from wikiPage import WikiInterface
from llm_interface import Chat
from answer_checker import AnswerChecker


class Orchestrator():
    def __init__(self):
        self.wiki_url : Optional[str]
        self.article : Optional[str]
        self.title : Optional[str]
        self.image : Optional[str]
        self.is_win : bool = False
        self.chat_backbone = Chat()
        self.wiki_interface = WikiInterface()
        self.answer_checker : Optional[AnswerChecker]

    def chose_article(self):
        page = self.wiki_interface.get_random_page()
        self.title = page["title"]
        self.article = page["content"]
        self.image = page["image"]
        self.answer_checker = AnswerChecker(self.title)
        print(f"{self.title=}")

    def get_article(self) -> str:
        return self.article

    def get_image(self) -> Image:
        return self.image
    
    def get_title(self) -> str:
        return self.title

    def _test_response(self, history : List[gr.ChatMessage]) -> bool:
        if self.answer_checker.check_ans(history[-1].content):
            self.is_win = True
            print("WIN")
        #if self.title in history[-1].content:
        #    self.is_win = True
        
    def get_response_from_model(self, history : List[gr.ChatMessage]) -> str:
        self._test_response(history)
        response = self.chat_backbone.get_response_from_model(history)
        return response

