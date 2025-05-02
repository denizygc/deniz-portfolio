from flask import Blueprint, render_template

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/')
def list_projects():
    return render_template('projects/project_list.html')

@projects_bp.route('/<project_name>')
def project_detail(project_name):
    return render_template('projects/project_detail.html', name=project_name.replace('-', ' ').title())
