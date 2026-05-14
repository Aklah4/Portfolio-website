from datetime import datetime, timezone
from flask import render_template, redirect, url_for, flash, abort, current_app
from .forms import ContactForm
from . import main_bp
from app.mongo_helpers import get_all_projects, get_project_by_slug


@main_bp.route("/")
def index():
    projects = get_all_projects()
    return render_template("index.html", projects=projects)

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        current_app.mongo["contacts"].insert_one({
            "name": form.name.data,
            "email": form.email.data,
            "subject": form.subject.data,
            "message": form.message.data,
            "submitted_at": datetime.now(timezone.utc),
        })
        flash("Your message has been sent!", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", form=form)

@main_bp.route("/projects")
def projects():
    all_projects = get_all_projects()
    return render_template("projects.html", projects=all_projects)

@main_bp.route("/projects/<slug>")
def project_detail(slug):
    project = get_project_by_slug(slug)
    if project is None:
        abort(404)
    return render_template("project_detail.html", project=project)
