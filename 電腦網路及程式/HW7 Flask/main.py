from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3, os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'dev-secret'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')


# -------------------- 教師登入系統 --------------------
def query_user(username: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
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

    id_, uname, pw_in_db = row
    if password == str(pw_in_db):
        session['teacher_id'] = id_
        session['teacher_username'] = uname
        session['teacher_name'] = uname
        return redirect(url_for('score_page'))
    else:
        return redirect(url_for('index', error='錯誤的密碼'))


@app.post('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# -------------------- 成績輸入系統 --------------------
def db_conn():
    return sqlite3.connect(DB_PATH)

def list_grades():
    conn = db_conn(); c = conn.cursor()
    c.execute("SELECT name, student_id, score FROM grades ORDER BY student_id ASC")
    rows = c.fetchall()
    conn.close()
    return rows

def add_grade(name, student_id, score):
    conn = db_conn(); c = conn.cursor()
    c.execute("INSERT INTO grades (name, student_id, score) VALUES (?, ?, ?)",
              (name, student_id, score))
    conn.commit(); conn.close()

def delete_grade(student_id):
    conn = db_conn(); c = conn.cursor()
    c.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    conn.commit(); conn.close()


@app.get('/score')
def score_page():
    if 'teacher_name' not in session:
        return redirect(url_for('index', error='請先登入'))
    grades = list_grades()
    msg = request.args.get('msg', '')
    return render_template('score.html',
                           teacher=session['teacher_name'],
                           grades=grades, msg=msg)


@app.post('/grades/add')
def grades_add():
    if 'teacher_name' not in session:
        return redirect(url_for('index'))

    name = request.form.get('name', '').strip()
    sid = request.form.get('student_id', '').strip()
    score = request.form.get('score', '').strip()

    if not name or not sid.isdigit() or not score.isdigit():
        return redirect(url_for('score_page', msg='請填正確的姓名/學號/成績'))

    add_grade(name, int(sid), int(score))
    return redirect(url_for('score_page', msg='新增成功'))


@app.post('/grades/delete')
def grades_delete():
    if 'teacher_name' not in session:
        return redirect(url_for('index'))

    sid = request.form.get('delete_student_id', '').strip()
    if not sid.isdigit():
        return redirect(url_for('score_page', msg='請輸入欲刪除的學號（數字）'))

    delete_grade(int(sid))
    return redirect(url_for('score_page', msg=f'已刪除學號 {sid}'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)

