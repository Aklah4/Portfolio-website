import os
from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
from . import admin_bp
from app.db import db
from app.models import Contact
from flask_login import login_required, login_user, logout_user, current_user
from app.models import AdminUser
from slugify import slugify
from app.mongo_helpers import (
    get_all_projects, get_project_by_slug,
    insert_project, update_project, delete_project,
)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}


def _allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _save_image(file):
    if not file or not file.filename:
        return None
    if not _allowed(file.filename):
        return None
    result = cloudinary.uploader.upload(file, folder="portfolio/projects")
    return result["secure_url"]


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("admin/login.html")

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("admin.login"))



@admin_bp.route("/dashboard")
@login_required
def dashboard():
    count = Contact.query.count()
    project_count = len(get_all_projects())
    return render_template("admin/dashboard.html", count=count, project_count=project_count)


@admin_bp.route('/users', methods=['GET'])
@login_required
def read():
    # Renamed variable to 'contacts' for clarity in your template
    contacts = Contact.query.all()
    return render_template('admin/users.html', contacts=contacts)

@admin_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    contact = db.get_or_404(Contact, id)

    if request.method == 'POST':
        contact.name = request.form.get('name')
        contact.email = request.form.get('email')
        contact.subject = request.form.get('subject')
        contact.message = request.form.get('message')

        db.session.commit()
        flash("Contact updated!", "info")
        return redirect(url_for('admin.read'))

    return render_template('admin/edit.html', user=contact)

@admin_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    contact = db.get_or_404(Contact, id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted.", "danger")
    return redirect(url_for('admin.read'))


# ── Project management ──────────────────────────────────────────────────────

@admin_bp.route("/projects")
@login_required
def projects_list():
    projects = get_all_projects()
    return render_template("admin/projects.html", projects=projects)


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def project_new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = request.form.get("slug", "").strip() or slugify(title)
        tech_raw = request.form.get("tech_stack", "")
        tech_stack = [t.strip() for t in tech_raw.split(",") if t.strip()]
        image_url = _save_image(request.files.get("image"))

        data = {
            "title": title,
            "slug": slug,
            "description": request.form.get("description", "").strip(),
            "tech_stack": tech_stack,
            "live_url": request.form.get("live_url", "").strip(),
            "github_url": request.form.get("github_url", "").strip(),
            "image_url": image_url or "",
            "featured": bool(request.form.get("featured")),
        }

        insert_project(data)
        flash("Project created!", "success")
        return redirect(url_for("admin.projects_list"))

    return render_template(
        "admin/project_form.html",
        project=None,
        action_url=url_for("admin.project_new"),
    )


@admin_bp.route("/projects/edit/<slug>", methods=["GET", "POST"])
@login_required
def project_edit(slug):
    project = get_project_by_slug(slug)
    if project is None:
        flash("Project not found.", "danger")
        return redirect(url_for("admin.projects_list"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        new_slug = request.form.get("slug", "").strip() or slugify(title)
        tech_raw = request.form.get("tech_stack", "")
        tech_stack = [t.strip() for t in tech_raw.split(",") if t.strip()]
        new_image = _save_image(request.files.get("image"))

        data = {
            "title": title,
            "slug": new_slug,
            "description": request.form.get("description", "").strip(),
            "tech_stack": tech_stack,
            "live_url": request.form.get("live_url", "").strip(),
            "github_url": request.form.get("github_url", "").strip(),
            "image_url": new_image if new_image else project.get("image_url", ""),
            "featured": bool(request.form.get("featured")),
        }

        update_project(slug, data)
        flash("Project updated!", "success")
        return redirect(url_for("admin.projects_list"))

    return render_template(
        "admin/project_form.html",
        project=project,
        action_url=url_for("admin.project_edit", slug=slug),
    )


@admin_bp.route("/projects/delete/<slug>", methods=["POST"])
@login_required
def project_delete(slug):
    if delete_project(slug):
        flash("Project deleted.", "danger")
    else:
        flash("Project not found.", "danger")
    return redirect(url_for("admin.projects_list"))