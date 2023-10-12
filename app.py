import datetime
from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient
import hashlib
import jwt

app = Flask(__name__)

SECRET_KEY = "XJDKLSDJSKLDJASDNJSLK3123DJNKLDJAA1231"
client = MongoClient('mongodb+srv://wideskyinme:test@cluster0.ohomgc8.mongodb.net/?retryWrites=true&w=majority')
db = client.sypark

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
        return render_template('main.html')     

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
