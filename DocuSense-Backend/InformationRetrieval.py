import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer

CHUNK_SIZE = 2048
CHUNK_OVERLAP = 128

class InformationRetrieval:

    def __init__(self, model_name: str):
        # Store model name:
        self.model_name = model_name

        # Text embedding model:
        self.model = SentenceTransformer(self.model_name)

        # DataFrame:
        self.corpus = pd.DataFrame()

    @staticmethod
    def chunk_text(text, chunk_size, overlap_size):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            if end > len(text):
                end = len(text)
            chunks.append(text[start:end])
            start += (chunk_size - overlap_size)
        return chunks

    def add_document(self, title: str, link: str, text: str):

        for chunk_number, text_chunk in enumerate(self.chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)):
            new_df = pd.DataFrame([{
                "title": title,
                "link": link,
                "text": text_chunk,
                "chunk_number": chunk_number,
                "embedding": self.model.encode([text_chunk])[0]}])

            self.corpus = pd.concat([self.corpus, new_df], ignore_index=True)

    def get_top_n_results(self, query_text: str, top_n = 5) -> pd.DataFrame:

        query_vector = self.model.encode([query_text], prompt_name="query")[0]

        corpus_copy = self.corpus.copy()
        corpus_copy["dot_product"] = corpus_copy["embedding"].apply(lambda x: np.dot(x, query_vector))
        corpus_copy = corpus_copy.sort_values(by=["dot_product", "chunk_number"], ascending=False)
        return corpus_copy.head(top_n)

    def serialize_corpus(self, out_path: str):
        self.corpus.to_json(out_path)

    def load_corpus(self, in_path: str):
        self.corpus = pd.read_json(in_path)


if __name__ == "__main__":
    a = InformationRetrieval("Snowflake/snowflake-arctic-embed-l")

    print(a.chunk_text("This is a very long sentence.", 4, 2))
