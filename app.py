from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
from flask import request
#__name__ refers to this file 
app = Flask(__name__)
#sqlite:///test.db specifies the location of the database (just in the project folder)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
#initialize the database with settings from our app
db = SQLAlchemy(app)

class Todo(db.Model):
    #primary key column of table in database
    id = db.Column(db.Integer, primary_key=True)
    #column of table in database (inferably the "todo" column) that contains content no larger than 200 characters per cell.
    content = db.Column(db.String(200), nullable=False)
    #anytime a new row is created, this column is filled with the current date and time.
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #returns the object representation. every time a new element is added it returns Task and then it's id.
    def __repr__(self):
        return '<Task %r>' % self.id

#decorator registers a view function for a given url rule. (an index, like /index)
#methods option is by default just GET. now we can GET from this route as well as POST and send data to our database.
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        #in index.html text field is named "content", so this gets whatever is in the text field.
        taskContent = request.form['content']
        newTask = Todo(content=taskContent)

        try:
            #add newTask to a new cell
            db.session.add(newTask)
            db.session.commit()
            #refresh the page?
            return redirect("/")
        except:
            return "There was an issue adding your task"

    else:
        #looks at database contents in the order they were created and returns all of them
        tasks = Todo.query.order_by(Todo.date_created).all()
        #render_template allows for templates in the templates folder to be used to give 
        #general structure to all indexes of a website. just fill in with unique information/
        #structure of a particular index.
        #also, notice "for task in tasks" in index.html. this is the second argument.
        return render_template("index.html", tasks=tasks)

#id of entity passed here in decorator. note "/delete/{{task.id}}" in index.html.
#also remember that the tasks/their id's are accessible through the html because 
#when they are rendered the tasks are passed as an argument and all are rendered 
#using jinja template engine.
@app.route("/delete/<int:id>")
def delete(id):
    taskToDelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        #already have the task in the database, just have to edit it.
        task.content = request.form["content"]
        
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "there was an issue commiting that change"
    else:
        return render_template("update.html", task=task)

if __name__ == "__main__":
    #runs the application on local development server. not meant for production. 
    app.run(debug=True)