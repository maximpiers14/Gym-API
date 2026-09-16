from flask import Blueprint, jsonify
import database

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("health")
def health():
    return jsonify({"status":"ok"}), 200

# ---------------------------
# API ROUTES FOR EXERCISES
# ---------------------------

@api.route("/exercises", methods = ["GET"])
def get_exercises():
    exercises = database.get_all_exercises()
    return jsonify(exercises), 200