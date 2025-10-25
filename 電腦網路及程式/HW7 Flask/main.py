from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3, bcrypt, os

# 指定 templates / static 目錄（預設即為 'templates' 與 'static'）
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'dev-secret'  # demo 用，正式請改成環境變數

# 讓 DB 路徑總是以當前檔案所在資料夾為基準
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')

def query_user(username: str):
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 你的 teachers 就是兩欄：username, password
    c.execute("""
        SELECT rowid AS id, username, password
        FROM teachers
        WHERE username = ?
    """, (username,))
    row = c.fetchone()
    conn.close()
    return row

@app.get('/')
def index():
    # 若已登入，直接去成績頁；否則顯示登入頁
    if 'teacher_name' in session:
        return redirect(url_for('score_page'))
    error = request.args.get('error', '')
    return render_template('login.html', error=error)

@app.post('/login')
def login_form():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    if not username or not password:
        return redirect(url_for('index', error='請輸入帳號與密碼'))

    row = query_user(username)
    if not row:
        return redirect(url_for('index', error='錯誤的名稱'))

    id_, uname, pw_in_db = row  # 這裡對應上面 SELECT 的三個欄位

    # 你的 DB 是明文密碼 → 直接字串比對
    if password == str(pw_in_db):
        session['teacher_id'] = id_
        session['teacher_username'] = uname
        session['teacher_name'] = uname  # 沒有 display_name，就用帳號當顯示名
        return redirect(url_for('score_page'))
    else:
        return redirect(url_for('index', error='錯誤的密碼'))

@app.get('/score')
def score_page():
    if 'teacher_name' not in session:
        return redirect(url_for('index', error='請先登入'))
    return render_template('score.html', teacher=session.get('teacher_name'))

@app.post('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # python main.py -> http://localhost:5000
    app.run(debug=True, port=5000)

