"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    title_and_grade = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html", 
                            first=first, 
                            last=last, 
                            github=github,
                            title_and_grade=title_and_grade)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html") 

@app.route("/add-student")
def display_add_student_form():
    """Display form to user asking for information about student to add."""

    return render_template("student-add.html")

@app.route("/add/student", methods=['POST'])
def student_add():
    """Add a student.""" 
    
    github = request.form.get('github')
    fname = request.form.get('fname')
    lname = request.form.get('lname')

    hackbright.make_new_student(fname, lname, github)

    return render_template("addition_confirmation.html", first=fname, last=lname, github=github)

@app.route("/project")
def display_project_info():
    """Display information about a project. 
    List the title, description, and maximum grade for a project.

    Also list students who have done that project."""

    title = request.args.get('project')
    title, description, max_grade = hackbright.get_project_by_title(title)
    student_github_grade = hackbright.get_grades_by_title(title)
    list_of_github_ids = []
    list_of_grades = []
    project_details = {}
    for item in student_github_grade:
        github_id = item[0]
        list_of_github_ids.append(github_id)
        project_details[github_id] = project_details.get(github_id, [])
        grade = item[1]
        list_of_grades.append(grade)
        project_details[github_id].append(grade)
    list_of_names = []
    for github_id in list_of_github_ids:
        name = hackbright.get_student_by_github(github_id)[0]+' '+hackbright.get_student_by_github(github_id)[1]
        list_of_names.append(name)
        project_details[github_id].append(name)


    return render_template("project_info.html", title=title, description=description, 
                            max_grade=max_grade, 
                            project_details=project_details)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
