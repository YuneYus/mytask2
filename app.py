
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#my app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False #this is to make
#sure it doesnt show the database to the user rather make their own data each
#when you deploy it 
db = SQLAlchemy(app)

#data
class MyTask(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(100), nullable=False)
    complete=db.Column(db.Integer, default=0)
    created=db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"task {db.id}"
#this is step 1, used to be inside of if __name__ == "__main__":
with app.app_context():
    db.create_all()
    
    
@app.route("/", methods=["POST", "GET"])
def index():
    #add task
    if request.method =="POST":
        currenttask = request.form["content"]
        new_task = MyTask(content=currenttask)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"error{e}")
            return f"error{e}"
    #see all current tasks
    
    else:
        task = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", task= task)
  

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    
    except Exception as e:
        print(f"error{e}")
        return f"error{e}"
    
   #update a task 
@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id:int):
    update_task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        update_task.content = request.form["content"]
        
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"error {e}")
            return f"error {e}"
    else:
        return render_template("update.html", task=update_task)



if __name__ == "__main__":
    app.run(debug=True)