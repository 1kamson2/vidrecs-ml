from flask import Flask

app = Flask(__name__)

@app.route("/api/recommendation", methods=["POST"])
def api_recommendation() -> str:
    return "Recommending"

@app.route("/api/train", methods=["POST"])
def api_train() -> str:
    return "Training"
