from flask_cors import CORS
from flask import Flask, render_template, request, Response

from langchain_assistant import chat_assistant

app = Flask(__name__)
CORS(app)
app.secret_key = 'ronaldo'

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    texto_resposta = chat_assistant(prompt)
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)



