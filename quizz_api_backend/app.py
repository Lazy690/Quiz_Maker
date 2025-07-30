from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import json

app = Flask(__name__)
QUIZ_DIR = "quizzes"
QUIZ_FILE = os.path.join(QUIZ_DIR, "current_quiz.json")

@app.route("/")
def home():
    return "Bare witness, I have become death, distroyer of worlds!!!"

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    with open(QUIZ_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "recieved", "quiz": data}), 200

@app.route("/quizz")
def display_quizz():
    if not os.path.exists(QUIZ_FILE):
        return "no quiz data found", 404

    with open(QUIZ_FILE, "r") as f:
        quiz_data = json.load(f)
    
    return render_template("quiz_page.html", quiz=quiz_data)

def load_current_quiz():
    with open(QUIZ_FILE, "r") as f:
        return json.load(f)
    
@app.route('/submit-answers', methods=['POST'])
def submit_answers():
    submitted_data = request.form
    total_score = 0

    for key in submitted_data:
        try:
            total_score += int(submitted_data[key])
        except ValueError:
            pass

    # Load current quiz
    current_quiz = load_current_quiz()
    result_text = "No result found."

    for answer in current_quiz['answers'].values():
        cond = answer.get('conditions', {})
        try:
            min_score = int(cond.get('from', 0))
            max_score = int(cond.get('to', 0))
        except ValueError:
            continue

        if min_score <= total_score <= max_score:
            result_text = answer.get('text', 'No result text provided.')
            break

    return render_template('result_page.html', score=total_score, result=result_text)


if __name__ == "__main__":
    app.run(debug=True)