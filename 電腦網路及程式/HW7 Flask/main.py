# ============================================================
# main.py
# 功能：教師登入、成績輸入系統 + 照片上傳與顯示功能
# ============================================================

from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3, os, time
from werkzeug.utils import secure_filename
from uuid import uuid4

# ------------------------------------------------------------
# 基本 Flask 設定
# ------------------------------------------------------------
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'dev-secret'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')

# ============================================================
# [照片上傳設定區]
# ============================================================

# 照片儲存資料夾：static/uploads/
UPLOAD_DIR = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)   # 若無資料夾則自動建立

# 允許的圖片副檔名
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# 上傳檔案大小限制（5MB）
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# 驗證檔案副檔名是否合法
def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# ============================================================
# [教師登入系統區]
# ============================================================

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
    """顯示登入頁"""
    if 'teacher_name' in session:
        return redirect(url_for('score_page'))
    error = request.args.get('error', '')
    return render_template('login.html', error=error)


@app.post('/login')
def login_form():
    """登入驗證"""
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
    """登出教師帳號"""
    session.clear()
    return redirect(url_for('index'))


# ============================================================
# [成績輸入系統區]
# ============================================================

def db_conn():
    return sqlite3.connect(DB_PATH)

def list_grades():
    """列出所有成績，依學號遞增排序"""
    conn = db_conn(); c = conn.cursor()
    c.execute("SELECT name, student_id, score FROM grades ORDER BY student_id ASC")
    rows = c.fetchall()
    conn.close()
    return rows

def add_grade(name, student_id, score):
    """新增學生成績"""
    conn = db_conn(); c = conn.cursor()
    c.execute("INSERT INTO grades (name, student_id, score) VALUES (?, ?, ?)",
              (name, student_id, score))
    conn.commit(); conn.close()

def delete_grade(student_id):
    """刪除指定學號的學生"""
    conn = db_conn(); c = conn.cursor()
    c.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    conn.commit(); conn.close()


# ============================================================
# [主畫面：成績頁 + 顯示已上傳照片]
# ============================================================

@app.get('/score')
def score_page():
    """顯示成績表 + 圖片牆"""
    if 'teacher_name' not in session:
        return redirect(url_for('index', error='請先登入'))
    grades = list_grades()
    msg = request.args.get('msg', '')

    # 讀取 static/uploads 中的圖片清單
    try:
        file_names = [f for f in os.listdir(UPLOAD_DIR) if allowed_file(f)]
    except FileNotFoundError:
        file_names = []
    gallery = [url_for('static', filename=f'uploads/{f}') for f in sorted(file_names, key=str.lower)]

    return render_template('score.html',
                           teacher=session['teacher_name'],
                           grades=grades,
                           msg=msg,
                           gallery=gallery)


# ============================================================
# [照片上傳功能區]
# ============================================================

@app.post('/upload_photo')
def upload_photo():
    """接收照片上傳並儲存於 static/uploads，再返回成績頁顯示"""
    if 'teacher_name' not in session:
        return redirect(url_for('index'))

    file = request.files.get('photo')
    if not file or file.filename == '':
        return redirect(url_for('score_page', msg='請選擇一張圖片'))
    if not allowed_file(file.filename):
        return redirect(url_for('score_page', msg='檔案格式僅限 png/jpg/jpeg/gif/webp'))

    # 使用安全檔名並加入時間戳避免覆蓋
    base = secure_filename(file.filename)
    ext = base.rsplit('.', 1)[1].lower()
    uniq = f"{int(time.time())}_{uuid4().hex[:6]}.{ext}"
    save_path = os.path.join(UPLOAD_DIR, uniq)

    # 儲存檔案
    file.save(save_path)
    return redirect(url_for('score_page', msg='上傳成功'))


# ============================================================
# [新增 / 刪除 成績路由]
# ============================================================

@app.post('/grades/add')
def grades_add():
    """接收新增成績表單"""
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
    """接收刪除學號表單"""
    if 'teacher_name' not in session:
        return redirect(url_for('index'))

    sid = request.form.get('delete_student_id', '').strip()
    if not sid.isdigit():
        return redirect(url_for('score_page', msg='請輸入欲刪除的學號（數字）'))

    delete_grade(int(sid))
    return redirect(url_for('score_page', msg=f'已刪除學號 {sid}'))


# ============================================================
# 主程式啟動
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)


