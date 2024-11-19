import copy
import threading
from threading import Thread
from typing import Generator

from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

class LLM:

    def __init__(self, hf_model_id: str, device: str, max_new_tokens: int):
        self.model_id = hf_model_id
        self.device = device

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id)
        self.model = self.model.to(device)

        self.max_new_tokens = max_new_tokens

        self.chats: [str, list[str]] = dict()
        self.locks: [str, threading.Lock] = dict()

    def send_chat(self, chat_name: str, message: str) -> Generator[str, None, None]:

        # Create the chat if not exists:
        if chat_name not in self.chats:
            self.chats[chat_name] = []
            self.locks[chat_name] = threading.Lock()

        messages = copy.deepcopy(self.chats.get(chat_name))
        lock = self.locks.get(chat_name)

        chat_message = {"role": "user", "content": message}

        messages.append(chat_message)

        question = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        question = self.tokenizer(question, return_tensors="pt").to(self.device)

        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)

        # Args to pass to model generate function:
        generation_kwargs = dict(question, streamer=streamer, max_new_tokens=self.max_new_tokens)

        # Start the generation thread:
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        with lock:
            # Get the response for chat history:
            assistant_response = ""

            for i in streamer:
                if type(i) == str and i != "<end_of_turn>" and len(i) > 0:
                    assistant_response += i
                    yield i

            response = assistant_response.strip()

            # Add the response:
            if len(response) > 0:

                # Get the model's response:
                response_message = {"role": "assistant", "content": response}

                # After the response, append the messages:
                real_messages = self.chats.get(chat_name)
                real_messages.append(chat_message)
                real_messages.append(response_message)
