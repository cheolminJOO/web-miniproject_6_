from flask import Flask, render_template, url_for, request, redirect
from bson.objectid import ObjectId 
from pymongo import MongoClient

app=Flask(__name__)

client = MongoClient('') # 몽고db userid/password
db = client['todo_db']
collection = db['todos']



@app.route("/todolist", methods = ["GET", "POST"])
def home():
    if (request.method == "POST"):
        todo_name = request.form["todo_name"]
        todo = {
            'id': ObjectId(),
            'name': todo_name,
            'checked': False,
        }
        collection.insert_one(todo)
        
    todos = list(collection.find({}))
    return render_template("index.html", items=todos)

@app.route("/checked/<string:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    todo = collection.find_one({'id': ObjectId(todo_id)})
    if todo:
        todo['checked'] = not todo['checked']
        collection.update_one({'id': ObjectId(todo_id)}, {"$set": {'checked': todo['checked']}})
    return redirect(url_for('home'))

@app.route("/delete/<string:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    collection.delete_one({'id': ObjectId(todo_id)})
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
