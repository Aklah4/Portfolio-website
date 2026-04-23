from flask import current_app, abort


def _projects():
    if current_app.mongo is None:
        abort(503, "Database unavailable")
    return current_app.mongo["projects"]


def get_all_projects():
    docs = _projects().find()
    projects = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        projects.append(doc)
    return projects


def get_project_by_slug(slug):
    doc = _projects().find_one({"slug": slug})
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc


def insert_project(data):
    result = _projects().insert_one(data)
    return str(result.inserted_id)


def delete_project(slug):
    result = _projects().delete_one({"slug": slug})
    return result.deleted_count > 0


def update_project(slug, data):
    result = _projects().update_one({"slug": slug}, {"$set": data})
    return result.matched_count > 0
