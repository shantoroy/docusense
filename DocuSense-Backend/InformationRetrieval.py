import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer

# Break the text into this size:
CHUNK_SIZE = 2048

# Keep a bit of context for overlap:
CHUNK_OVERLAP = 128

class InformationRetrieval:

    def __init__(self, model_name: str):
        # Store model name:
        self.model_name = model_name

        # Text embedding model:
        self.model = SentenceTransformer(self.model_name)

        # DataFrame:
        self.corpus = pd.DataFrame()

    # Given a text string, split into chunks of size but after iterating, keep the overlap size:
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

    # Add a document into the system:
    def add_document(self, title: str, link: str, text: str):

        for chunk_number, text_chunk in enumerate(self.chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)):
            new_df = pd.DataFrame([{
                "title": title,
                "link": link,
                "text": text_chunk,
                "chunk_number": chunk_number,
                "embedding": self.model.encode([text_chunk])[0]}])

            self.corpus = pd.concat([self.corpus, new_df], ignore_index=True)

    # Return the top n results given a query (default 5):
    def get_top_n_results(self, query_text: str, top_n = 5) -> pd.DataFrame:

        query_vector = self.model.encode([query_text], prompt_name="query")[0]

        corpus_copy = self.corpus.copy()
        corpus_copy["dot_product"] = corpus_copy["embedding"].apply(lambda x: np.dot(x, query_vector))
        corpus_copy = corpus_copy.sort_values(by=["dot_product", "chunk_number"], ascending=False)
        return corpus_copy.head(top_n)

    # Save corpus to disk:
    def serialize_corpus(self, out_path: str):
        self.corpus.to_json(out_path)

    # Load from file if saved:
    def load_corpus(self, in_path: str):
        self.corpus = pd.read_json(in_path)
