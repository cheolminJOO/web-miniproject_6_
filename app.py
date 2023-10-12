from flask import Flask, render_template, url_for, request, redirect
import random
from pymongo import MongoClient

app=Flask(__name__)

client = MongoClient('mongodb+srv://sparta:test@cluster0.t100elz.mongodb.net/?retryWrites=true&w=majority')
db = client['todo_db']
collection = db['todos']


@app.route("/todolist", methods = ["GET", "POST"])
def home():
    if (request.method == "POST"):
        todo_name = request.form["todo_name"]
        cur_id = random.randint(1, 1000)
        todo = {
            'id': cur_id,
            'name': todo_name,
            'checked': False,
        }
        collection.insert_one(todo)
        
    todos = list(collection.find({}))
    return render_template("index.html", items=todos)

@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    todo = collection.find_one({'id': todo_id})
    if todo:
        todo['checked'] = not todo['checked']
        collection.update_one({'id': todo_id}, {"$set": {'checked': todo['checked']}})
    return redirect(url_for('home'))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    collection.delete_one({'id': todo_id})
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)