from flask  import Flask, render_template, url_for, request, redirect
import random
from pymongo.mongo_client import MongoClient # pymongo 안에 있는 MongoClient 가지고 오기

client = MongoClient("mongodb://localhost:27017") # 데이터베이스 연결
db = client.local # 사용할 데이터베이스 선택
collection = db.todo # collection 선택


# rows = collection.find_one() # 문서를 전 부 다 가지고 온다. 반복문을 이용해서 가지고 올 수 있다.

# for row in rows:

#     print(row)  # 결과 출력

app=Flask(__name__)

todos = [
    {
        'id' : 1,
        'name' : 'Write SQL',
        'checked' : False,
    },
        {
        'id' : 1,
        'name' : 'Write Python',
        'checked' : True,
    },
]

@app.route("/todolist", methods = ["GET", "POST"])
def home():
    if (request.method == "POST"):
        todo_name = request.form["todo_name"]
        cur_id = random.randint(1, 1000)
        collection.insert_one({
            'id' : cur_id,
            'name' : todo_name,
            'checked' : False,
        })
        todos = list(collection.find({}))
    return render_template("index.html", items=todos)

@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    
    collection.update_one({'id': todo_id}, {'$set': {'checked': True}})
    return redirect(url_for('home'))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):

    collection.delete_one({'id': todo_id})
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
