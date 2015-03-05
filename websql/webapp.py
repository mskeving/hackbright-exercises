from flask import Flask, render_template, request
import hackbright_app

# Creating an instance of the Flask class 
app = Flask(__name__)

# @app.route("/") is a decorator stating that once we go to the specified URL
# we initialize the function def get_github()  
# render_template returns the contents of the html file as a string
@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("student")

    row = hackbright_app.get_student_grades(student_github)
    print row
    if row:
        html = render_template("student_info.html", first_name=row[0][0],
                                                    last_name=row[0][1],
                                                    projects=row)
    else:
        row = hackbright_app.get_student_by_github(student_github)
        return render_template("student_info_bare.html", first_name=row[0],
        last_name=row[1], github=row[2]) #send error message if this happens
    return html

@app.route("/project_title")
def get_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project")
    row = hackbright_app.get_grades_by_project(project_title)
    return render_template("project_info.html", project_title=project_title,
                                                projects=row)

# Link from get_github.html ("/") takes you here
@app.route("/new_student")
def make_student():
    message = ""
    hackbright_app.connect_to_db()
    #arguments coming from form on new_student.html
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")

    # When page first loads, no first_name etc. 
    if first_name and last_name and github:
        #insert student data in db
        hackbright_app.make_new_student(first_name, last_name, github)
        message = "You successfully added: %s %s" % (first_name, last_name)
        #todo: add success message that student was added 
    #essentially refresh page after submit with empty text boxes
    return render_template("new_student.html", message=message) 
    #To alter html page, pass variable in return statement


if __name__ == "__main__":
    app.run(debug=True) #allows flask to keep running even after making changes
