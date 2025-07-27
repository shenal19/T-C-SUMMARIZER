from flask import Flask, render_template, request
from summarizer import get_relevant_clauses, extract_text_from_pdf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = {}
    if request.method == "POST":
        text = ""

        if request.files.get("tnc_file"):
            file = request.files["tnc_file"]
            if file:
                text = extract_text_from_pdf(file)
        else:
            text = request.form.get("tnc_text")

        if text:
            result = get_relevant_clauses(text)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
