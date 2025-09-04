from ollama import Client

class AnswerChecker:
    def __init__(self, correct_answer:str):
        self.model_name = "gemma3:1b"
        self.port = 11434
        self.client = Client(host=f"http://localhost:{self.port}")
        self.correct_answer = correct_answer
        
    def check_ans(self, ans:str) -> bool:
        msgs = [
            {
                "role": "system",
                "content": f"Your role is to check if the user's message contains the answer '{self.correct_answer}'. answer 'YES' if it does, otherwise, answer 'NO'", 'metadata': {},
            },
            {
                "role": "user", 
                "content": f"{ans}", 'metadata': {},
            },
            ]
        
        chat_response = self.client.chat(model=self.model_name,messages=msgs)
        content = chat_response["message"]["content"]
        if "YES" in content:
            return True
        return False
        
