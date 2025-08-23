# app/app.py
from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from .matcher import compare_resume_with_jd

app = Flask(__name__)
TMP = Path("tmp"); TMP.mkdir(exist_ok=True)

@app.route("/", methods=["GET"])
def root():
    # serve static/index.html
    return send_from_directory("../static", "index.html")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    # expects <input name="resume"> and <textarea name="jd">
    if "resume" not in request.files:
        return jsonify({"error": "missing file 'resume'"}), 400
    f = request.files["resume"]
    jd_text = (request.form.get("jd") or "").strip()
    if not jd_text:
        return jsonify({"error": "missing JD text"}), 400

    resume_path = TMP / "resume.pdf"
    f.save(resume_path)

    result = compare_resume_with_jd(str(resume_path), jd_text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
