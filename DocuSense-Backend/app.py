import flask
import json

from flask import Flask, request
from flask_cors import CORS

from RAG import RAG

DOCUMENTS_PATH = "./data"
prompt = r"""
<TASK>
You are an expert in answering questions based on documents provided to you. 
Please analyze the documents thoroughly and answer the question(s). 

At the end of your response, provide a citation consisting of the document title and link. 

<QUESTION>
{question}

<DOCUMENTS>
{documents}
""".strip()

# RAG system:
rag = RAG(prompt, DOCUMENTS_PATH)

# Flask app:
app = Flask(__name__)

CORS(app)

def format_sse(data: str, event=None):
    msg = f'data: {data}\n\n'

    if event is not None:
        msg = f'event: {event}\n{msg}'

    return msg


@app.route("/chat", methods=['GET'])
def handle_chat_message():

    # Request params:
    chat_message = request.args.get('chat_message', default="", type=str)
    chat_name = request.args.get('chat_name', default="", type=str)

    if len(chat_message) == 0 or len(chat_name) == 0:
        raise ValueError("Parameter chat_message and chat_name cannot be empty.")

    def stream():
        for msg_part in rag.rag(chat_name, chat_message):
            yield format_sse(event="chunk", data=json.dumps({"text": msg_part}))

        # Yield finish message:
        yield format_sse(event="finish", data=".")

    return flask.Response(stream(), mimetype='text/event-stream')


if __name__ == "__main__":
    # Note: adding debug=True will cause it to reload the model twice:
    app.run(debug=False)
