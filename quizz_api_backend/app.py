from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Bare witness, I have become death, distroyer of worlds!!!"

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    return jsonify({"status": "recieved", "quiz": data}), 200

if __name__ == "__main__":
    app.run(debug=True)