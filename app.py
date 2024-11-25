from flask_cors import CORS
from flask import Flask, render_template, request, Response

#from langchain_assistant import chat_assistant
#from ira_retrieval_chain import chat_assistant
from avi_chain_adaptor import AVIChainAdaptor

app = Flask(__name__)
CORS(app)
app.secret_key = 'ronaldo'

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    chaina_adaptor = AVIChainAdaptor()
    texto_resposta = chaina_adaptor.invoke(prompt)
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)



