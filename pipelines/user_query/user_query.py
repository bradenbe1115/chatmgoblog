from flask import Flask, jsonify, request
import bootstrap

from embed.service_layer.services import embed_content
from content_index.service_layer import services as content_index_services

app = Flask(__name__)
embed_deps, content_index_deps = bootstrap.bootstrap()

@app.route("/user_query", methods=["GET"])
def user_query():

    user_query = request.json["user_query"]
    
    embedded_text = embed_content(chunker=embed_deps["chunker"], embedder=embed_deps["embedder"], text_data=[{"query":user_query}], text_field_name="query")

    results = content_index_services.get_similar_mgoblog_content(uow=content_index_deps["uow"], embeddings=[x["embedded"] for x in embedded_text], top_n_results=30)[0]
    
    return jsonify([x.__dict__ for x in results]), 200