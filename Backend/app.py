from flask import Flask, jsonify, render_template, request
from logic import get_build
from perks import survivor_perks, exhaustion_perks, healing_perks

app = Flask(
    __name__,
    template_folder="../Templates",
    static_folder="../Static",
    static_url_path="/static",
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    mode = request.json.get("mode")

    if mode == "any":
        pool = survivor_perks
    elif mode == "exhaustion":
        pool = exhaustion_perks
    elif mode == "healing":
        pool = healing_perks
    else:
        pool = survivor_perks

    build = get_build(pool)
    return jsonify(build)

if __name__ == "__main__":
    app.run(debug=True)
