import datetime
from flask import Flask, render_template, request, redirect, jsonify, url_for
from pymongo import MongoClient
import hashlib
import jwt
from bson.objectid import ObjectId 

app = Flask(__name__)

SECRET_KEY = "XJDKLSDJSKLDJASDNJSLK3123DJNKLDJAA1231"
client = MongoClient('mongodb+srv://wideskyinme:test@cluster0.ohomgc8.mongodb.net/?retryWrites=true&w=majority')
db = client.sypark
collection = db['todos']

# 메인 페이지
@app.route('/')
def index():
    return render_template('login.html')

# 회원가입
@app.route('/signup', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    existing_user = db.users.find_one({'user_id': id_receive})
    if existing_user is not None:
        return jsonify({'message': '이미 존재하는 아이디입니다.'})
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    user = {
        'user_id': id_receive,
        'user_password': pw_hash
    }
    db.users.insert_one(user)
    return jsonify({'message': '회원가입에 성공했습니다.'})

# 로그인
@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    user = db.users.find_one({'user_id': id_receive, 'user_password': pw_hash})
    if user is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'message': '로그인에 성공했습니다.', 'result': 'success', 'token': access_token})
    else:
        return jsonify({'message': '존재하지 않는 아이디이거나 비밀번호가 틀립니다.', 'result': 'fail'})
    
#로그인 후 main페이지로 이동
@app.route('/call_main')
def after_login():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_id = payload["id"]
        return redirect(url_for('home', user_id=user_id))  # user_id를 함께 전달

    except jwt.ExpiredSignatureError:
        return redirect("/call_login")  
    except jwt.exceptions.DecodeError:
        return redirect("/call_login")

@app.route('/call_login')
def call_login():
    return render_template('login.html')

@app.route('/call_register')
def call_register():
    return render_template('register.html')

# todolist

@app.route("/todolist", methods=["GET", "POST"])
def home():
    token_receive = request.cookies.get('mytoken')
    user_id = None

    if token_receive:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_id = payload["id"]
        except jwt.ExpiredSignatureError:
            pass  
        except jwt.exceptions.DecodeError:
            pass  

    if request.method == "POST":
        todo_name = request.form["todo_name"]
        todo = {
            'id': ObjectId(),
            'name': todo_name,
            'checked': False,
            'user_id': user_id  
        }
        collection.insert_one(todo)

    todos = list(collection.find({'user_id': user_id})) 
    return render_template("index.html", items=todos, user_id=user_id)


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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)