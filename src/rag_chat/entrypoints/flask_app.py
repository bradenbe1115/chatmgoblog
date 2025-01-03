from flask import Flask, jsonify, request
from rag_chat import bootstrap

from rag_chat.service_layer.services import generate_chat_response_with_context

app = Flask(__name__)
chat = bootstrap.bootstrap_chatgpt4_mini()

@app.route("/gen_chat_with_context", methods=["GET"])
def gen_chat_with_context():
    question = request.json["question"]
    context = request.json["context"]

    try:
        answer = generate_chat_response_with_context(question=question, context = context, chat=chat)
    except:
        return {}, 400
    
    return {"response": answer, "question": question, "context": context}, 200