from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from datetime import datetime
import sqlite3
import logging
import re
import os

app = Flask(__name__)
app.secret_key = "exam2-secret"   # 為了 session，要有一個 key


# 啟動時先確保有 users 這張表
def ensure_users_table():
    # ✅ 固定指向 shopping_system 裡的資料庫
    db_path = os.path.join(os.path.dirname(__file__), 'shopping_data.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email    TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

ensure_users_table()


# 路徑修改
def get_db_connection():
    # 題目 h: 期望將資料寫入 shopping_data.db
    # ✅ 這裡改成固定讀取「shopping_system」裡面的資料庫
    db_path = os.path.join(os.path.dirname(__file__), 'shopping_data.db')

    # 看清楚 Flask 實際在用哪顆 db
    print("👉 Flask 正在使用的資料庫位置：", os.path.abspath(db_path))

    # 檢查檔案是否存在
    if not os.path.exists(db_path):
        logging.error(f"Database file not found at {db_path}")
        return None

    # 連線資料庫
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn  # 【補齊空缺程式碼】一定要把連線傳回去


# 補齊空缺程式碼
@app.route('/')
def page_login_root():
    # 題目 g: 註冊後進入登入頁面
    return render_template('page_login_.html')


# ==============================
# 註冊頁面（Python 75% → 1. 註冊頁面 + 功能 30%）
# ==============================
@app.route('/page_register', methods=['GET', 'POST'])
def page_register():
    if request.method == 'POST':
        data = request.get_json()

        # ----------------------------
        # a. 可輸入帳號、密碼、信箱
        # ----------------------------
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        email    = data.get('email', '').strip()

        if not username or not password or not email:
            return jsonify({"status": "error", "message": "請完整輸入帳號、密碼、信箱"})

        # 連線資料庫
        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "error", "message": "資料庫不存在或無法連線"})

        cursor = conn.cursor()

        # ----------------------------
        # b. 帳號是主鍵 → 必須先檢查是否已存在
        # ----------------------------
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existed = cursor.fetchone()

        if existed:
            conn.close()
            return jsonify({"status": "error", "message": "此名稱已被使用"})

        # ----------------------------
        # c. 密碼: 至少包含 2 條限制 (字數 8 以上、包含大小寫英文…)
        # ----------------------------
        failed_rules = []

        if len(password) < 8:
            failed_rules.append("密碼至少要 8 碼")

        if not re.search(r'[A-Z]', password):
            failed_rules.append("需包含大寫英文")

        if not re.search(r'[a-z]', password):
            failed_rules.append("需包含小寫英文")

        if not re.search(r'[0-9!@#$%^&*()_+]', password):
            failed_rules.append("需包含數字或特殊字元")

        if len(failed_rules) > 2:
            conn.close()
            return jsonify({
                "status": "error",
                "message": "密碼不符合規則，請重新輸入：" + "；".join(failed_rules)
            })

        # ----------------------------
        # d. 信箱: 必須為 XXX@gmail.com 格式
        # ----------------------------
        if not re.match(r'^[^@]+@gmail\.com$', email):
            conn.close()
            return jsonify({"status": "error", "message": "Email 格式不符請重新輸入"})

        # ----------------------------
        # h. 都OK → 寫入 shopping_data.db 的 users
        # ----------------------------
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, password, email)
            )
            conn.commit()
        except sqlite3.Error as e:
            conn.close()
            return jsonify({"status": "error", "message": f"寫入資料庫失敗: {e}"})
        conn.close()

        # ----------------------------
        # f. 規則全部符合之後，跳出 alert 顯示: 註冊成功
        # g. 註冊後進入登入頁面（前端自己導）
        # ----------------------------
        return jsonify({"status": "success", "message": "註冊成功"})

    # GET → 回傳註冊畫面
    return render_template('page_register.html')


def login_user(username, password):
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                return {"status": "success", "message": "Login successful"}
            else:
                return {"status": "error", "message": "Invalid username or password"}
        except sqlite3.Error as e:
            logging.error(f"Database query error: {e}")
            return {"status": "error", "message": "An error occurred"}
        finally:
            conn.close()
    else:
        return {"status": "error", "message": "Database connection error"}


@app.route('/page_login', methods=['GET', 'POST'])
def page_login():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            result = login_user(username, password)
            if result["status"] == "success":
                session['username'] = username
            return jsonify(result)
        return render_template('page_login_.html')
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)




