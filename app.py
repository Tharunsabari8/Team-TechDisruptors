from flask import Flask, request, render_template, redirect, url_for
import json
from boolean_query_generator import generate_boolean_query, search_database

# Load the initial database
with open("data.json") as f:
    database = json.load(f)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        user_query = request.form["query"]
        boolean_query = generate_boolean_query(user_query)
        results = search_database(boolean_query, database)
    return render_template("index.html", results=results)

@app.route("/feedback", methods=["POST"])
def feedback():
    study_id = request.form["study_id"]
    feedback = request.form["feedback"]

    # Load existing feedback data
    try:
        with open("feedback.json", "r") as f:
            feedback_data = json.load(f)
    except FileNotFoundError:
        feedback_data = []

    # Append new feedback
    feedback_data.append({"study_id": study_id, "feedback": feedback})

    # Save feedback data
    with open("feedback.json", "w") as f:
        json.dump(feedback_data, f, indent=4)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
