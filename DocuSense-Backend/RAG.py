import os

import torch

from InformationRetrieval import InformationRetrieval
from LLM import LLM


class RAG:

    TEXT_EMBEDDING_MODEL = "Snowflake/snowflake-arctic-embed-l"

    def __init__(self, prompt_format: str, documents_path: str):

        self.prompt_format = prompt_format
        self.information_retrieval = InformationRetrieval(self.TEXT_EMBEDDING_MODEL)

        self.DEVICE_NAME = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.MODEL_ID = "google/gemma-2-2b-it"
        self.MAX_NEW_TOKENS = 2048

        self.model = LLM(self.MODEL_ID, self.DEVICE_NAME, self.MAX_NEW_TOKENS)

        for file_path in [f"{documents_path}/" + i for i in os.listdir(documents_path) if os.path.isfile(f"{documents_path}/" + i)]:
            with open(file_path, "r", encoding='utf-8') as file:
                self.information_retrieval.add_document(file_path.split("/")[-1], f"http://localhost/{file_path.split("/")[-1]}", file.read())


    def rag(self, chat_name: str, chat_message: str):

        top_docs = self.information_retrieval.get_top_n_results(chat_message)
        top_docs_text = top_docs["text"].to_list()
        top_docs_titles = top_docs["title"].to_list()
        top_docs_links = top_docs["link"].to_list()

        builder = ""

        for i in range(len(top_docs_text)):
            builder += (f"<Document #{i + 1}>\n" +
                        f"<Title>:\n{top_docs_titles[i]}\n" +
                        f"<Link>:\n{top_docs_links[i]}\n" +
                        f"<Contents>:\n{top_docs_text[i]}\n\n")

        formatted_prompt = self.prompt_format.format(question=chat_message, documents=builder)

        print(formatted_prompt)

        return self.model.send_chat(chat_name, formatted_prompt)


if __name__ == "__main__":
    prompt = r"""
<TASK>
You are an expert in answering questions based on documents provided to you. 
Please analyze the documents thoroughly and answer the question(s). 

At the end of your response, provide a citation consisting of the title and link. 

<QUESTION>
{question}

<DOCUMENTS>
{documents}
    """.strip()
    a = RAG(prompt, "./data")

    a.rag("a", "Was there a critical Schwab bug?")