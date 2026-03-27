import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from logic import get_build, reroll_perk
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

PERK_DESCRIPTIONS = json.loads(
    (Path(__file__).resolve().parent / "perk_descriptions.json").read_text(encoding="utf-8")
)
DEFAULT_DESCRIPTION = "Description unavailable for this perk right now."

app = Flask(
    __name__,
    template_folder="../Templates",
    static_folder="../Static",
    static_url_path="/static",
)

def get_pool(mode):
    if mode == "any":
        return survivor_perks
    if mode == "exhaustion":
        return exhaustion_perks
    if mode == "healing":
        return healing_perks
    if mode == "team":
        return team_perks
    if mode == "stealth":
        return stealth_perks
    if mode == "chase":
        return chase_perks
    if mode == "generator":
        return generator_perks
    if mode == "aura":
        return aura_perks
    if mode == "anti_tunnel":
        return anti_tunnel_perks
    if mode == "killer":
        return killer_perks
    return survivor_perks

def serialize_build(build):
    return [
        {
            "name": perk_name,
            "description": PERK_DESCRIPTIONS.get(perk_name, DEFAULT_DESCRIPTION),
        }
        for perk_name in build
    ]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    payload = request.get_json(silent=True) or {}
    build = get_build(get_pool(payload.get("mode")))
    return jsonify(serialize_build(build))

@app.route("/reroll-one", methods=["POST"])
def reroll_one():
    payload = request.get_json(silent=True) or {}
    current_build = payload.get("current_build", [])
    perk_index = payload.get("index")

    if not isinstance(current_build, list) or len(current_build) != 4:
        return jsonify({"error": "A full build is required to reroll a perk."}), 400

    if not isinstance(perk_index, int):
        return jsonify({"error": "A valid perk index is required."}), 400

    try:
        updated_build = reroll_perk(get_pool(payload.get("mode")), current_build, perk_index)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify(serialize_build(updated_build))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
