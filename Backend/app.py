from flask import Flask, jsonify, render_template, request
from logic import get_build
from perks import (
    anti_tunnel_perks,
    aura_perks,
    chase_perks,
    exhaustion_perks,
    generator_perks,
    healing_perks,
    killer_perks,
    stealth_perks,
    survivor_perks,
    team_perks,
)

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
    elif mode == "team":
        pool = team_perks
    elif mode == "stealth":
        pool = stealth_perks
    elif mode == "chase":
        pool = chase_perks
    elif mode == "generator":
        pool = generator_perks
    elif mode == "aura":
        pool = aura_perks
    elif mode == "anti_tunnel":
        pool = anti_tunnel_perks
    elif mode == "killer":
        pool = killer_perks
    else:
        pool = survivor_perks

    build = get_build(pool)
    return jsonify(build)

if __name__ == "__main__":
    app.run(debug=True)
