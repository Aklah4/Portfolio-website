from flask import jsonify, current_app
from . import api_bp


@api_bp.route("/projects", methods=["GET"])
def get_projects():
    projects = list(current_app.mongo["projects"].find())
    for project in projects:
        project["_id"] = str(project["_id"])
    return jsonify(projects)


@api_bp.route("/projects/<slug>", methods=["GET"])
def get_project(slug):
    project = current_app.mongo["projects"].find_one({"slug": slug})
    if project is None:
        return jsonify({"status": "error", "message": "Project not found"}), 404
    project["_id"] = str(project["_id"])
    return jsonify(project)


@api_bp.route("/skills", methods=["GET"])
def get_skills():
    return jsonify({"status": "success", "data": []})
