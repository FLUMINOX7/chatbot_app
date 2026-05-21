import tensorflow as tf
from flask import Flask, request, jsonify
import numpy as np
import pickle
import random
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense, Input
from transformers import AutoTokenizer


app = Flask(__name__)

# ======================
# LOAD MODEL
# ======================
def build_model(num_words=10000, maxlen=128):

    inputs = Input(shape=(maxlen,))

    x = Embedding(input_dim=num_words, output_dim=128)(inputs)

    x = SimpleRNN(64, return_sequences=True)(x)

    x = SimpleRNN(32)(x)

    outputs = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=inputs, outputs=outputs)

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    return model


tokenizer = AutoTokenizer.from_pretrained("almanach/camembert-large")

MAXLEN = 128

model = build_model(num_words=tokenizer.vocab_size, maxlen=MAXLEN)
model.load_weights("model_allocine.weights.h5")

# ======================
# PHRASES DYNAMIQUES
# ======================
positive_phrases = [
    "Le modèle est confiant dans une opinion positive.",
    "Cela ressemble fortement à un avis favorable.",
    "Sentiment globalement enthousiaste détecté.",
]

negative_phrases = [
    "Le texte exprime clairement une opinion négative.",
    "Le modèle détecte une forte polarité négative.",
    "Sentiment défavorable identifié avec confiance.",
]

# ======================
# PREPROCESS TEXT
# ======================
def preprocess(texte):
    token = tokenizer(
        texte,
        padding="max_length",
        truncation=True,
        max_length=MAXLEN,
        return_tensors="np"
    )

    return token["input_ids"] 

# ======================
# ROUTE PREDICTION
# ======================
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json["text"]

    seq = preprocess(data)
    pred = model.predict(seq)[0][0]

    if pred >= 0.5:
        label = "Positif"
        phrase = random.choice(positive_phrases)
    else:
        label = "Négatif"
        phrase = random.choice(negative_phrases)

    # jsonify() transforme un dictionnaire Python en JSON valide HTTP
    return jsonify({
        "text": data,
        "prediction": float(pred),
        "label": label,
        "message": phrase
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
