from flask import Flask, request, jsonify
import random
import pandas as pd
from transformers import pipeline

app = Flask(__name__)

# ======================
# LOAD MODEL
# ======================
def pandas_model(question):

    df = {"Actors": ["Brad Pitt", "Leonardo Di Caprio", "George Clooney"], "Number of movies": ["87", "53", "69"]}
    table = pd.DataFrame.from_dict(df)

    # pipeline model
    # Note: you must to install torch-scatter first.
    tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")

    # result
    return (tqa(table=table, query=question)['cells'][0])


@app.route("/pandas_predict", methods=["POST"])
def pandas_predict():
    # Implementation for pandas prediction
    question = request.json["text"]

    return jsonify({
        "text": question,
        "prediction": None,
        "label": "Example label",
        "message": pandas_model(question)
    })


if __name__ == "__main__":
    # =========================================================
    # FLASK SERVER CONFIGURATION
    # =========================================================
    #app.run(host="0.0.0.0", port=5000, debug=True)

    # host="127.0.0.1" (par défaut)
    # -> accessible uniquement depuis ta machine locale

    # host="0.0.0.0"
    # -> permet d’exposer le serveur sur toutes les interfaces réseau
    # -> accessible depuis d’autres machines sur le même réseau local (LAN)

    # port=5000 (par défaut)
    # -> port standard de Flask

    # tu peux le modifier par exemple :
    # port=8000 ou port=3000 selon ton besoin

    # exemple d’accès :
    # http://127.0.0.1:5000 (local uniquement)
    # http://192.168.1.25:5000 (réseau local si host=0.0.0.0)
    app.run(debug=True)
