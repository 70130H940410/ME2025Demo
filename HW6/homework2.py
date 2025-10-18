#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Homework 2: Sign up / Sign in system (Python + SQLite)
- Connects to users.db
- (a) Sign up with validations (name, gmail email, strong password, no sequential patterns)
- (b) Sign in with error handling and "forgot password? Y/N" flow
Author: ChatGPT
"""

# ----------------------------------------------------------- 匯入模組區 -----------------------------------------------------------
import os
import re
import sqlite3
import sys
from typing import Tuple


# ----------------------------------------------------------- 資料庫設定 / 連線工具 -----------------------------------------------------------
# 備註：
# 1) DB 檔名依題目可自訂，這裡使用 users.db（與程式同資料夾）
# 2) SQLite 若檔案不存在，連線時會自動建立
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")

def get_conn():
    """取得 SQLite 連線物件"""
    return sqlite3.connect(DB_PATH)

def ensure_schema():
    """
    建表（若不存在則建立）：
    - users(name, email唯一, password)
    """
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.commit()


# ----------------------------------------------------------- 驗證規則（Email / 密碼） -----------------------------------------------------------
# Email 僅允許 XXX@gmail.com 之格式（依題目要求）
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@gmail\.com$")

def validate_email(email: str) -> bool:
    """Email 檢查：必須符合 XXX@gmail.com"""
    return EMAIL_REGEX.match(email) is not None

def has_upper(s: str) -> bool:
    """是否包含大寫字母"""
    return any(c.isupper() for c in s)

def has_lower(s: str) -> bool:
    """是否包含小寫字母"""
    return any(c.islower() for c in s)

def has_special(s: str) -> bool:
    """
    是否包含特殊字元
    說明：將「非英數字」視為特殊字元（含底線）
    """
    return any(not c.isalnum() for c in s)

def is_sequential(s: str) -> bool:
    """
    是否為明顯連號 / 連續字串：
    例：'123', '4567', 'abc', 'cde', 'zyx' ...
    補充：同時也排除常見弱密碼片段（qwerty、password 等）
    """
    if len(s) < 3:
        return False

    # 僅針對英數連續片段檢查
    runs = re.findall(r"[A-Za-z0-9]+", s)
    for run in runs:
        if len(run) < 3:
            continue
        vals = []
        for ch in run:
            if ch.isdigit():
                vals.append(ord(ch))          # '0'..'9'
            else:
                vals.append(ord(ch.lower()))  # 'a'..'z'
        asc = all(vals[i+1] - vals[i] == 1 for i in range(len(vals)-1))
        desc = all(vals[i] - vals[i+1] == 1 for i in range(len(vals)-1))
        if asc or desc:
            return True

    # 常見弱密碼片段（可自行擴充）
    weak_patterns = ("123456", "abcdef", "qwerty", "password")
    if any(p in s.lower() for p in weak_patterns):
        return True

    return False

def validate_password(pw: str) -> Tuple[bool, str]:
    """
    密碼規則（依題目）：
    1) 長度 ≥ 8
    2) 含大寫 + 小寫英文字母
    3) 含特殊字元
    4) 不可連號（如 123..、abc..）或弱密碼片段
    回傳：(是否通過, 不通過時的提示字串)
    """
    if len(pw) < 8:
        return False, "密碼必須超過8個字元，請重新輸入。"
    if not has_upper(pw):
        return False, "密碼需包含大寫字母，請重新輸入。"
    if not has_lower(pw):
        return False, "密碼需包含小寫字母，請重新輸入。"
    if not has_special(pw):
        return False, "密碼需包含特殊字元（如 !@#$/_* 等），請重新輸入。"
    if is_sequential(pw):
        return False, "密碼不可為連號或常見弱密碼（如 123、abc、qwerty），請重新輸入。"
    return True, ""


# ----------------------------------------------------------- 互動輸入小工具 -----------------------------------------------------------
def prompt_nonempty(prompt: str) -> str:
    """
    要求使用者必填（非空字串）
    範例：
      name = prompt_nonempty("輸入姓名: ")
    """
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("此欄位不得為空，請重新輸入。")


# ----------------------------------------------------------- (a) 註冊流程：sign_up() -----------------------------------------------------------
def sign_up():
    """
    註冊流程：
    1) 姓名（必填）
    2) Email（必須 XXX@gmail.com）
    3) 密碼（需符合上方密碼規則）
    4) 顯示確認字串 -> Y 儲存 / N 取消
       - 若 email 已存在 -> 詢問是否更新
       - 若 email 不存在 -> 直接新增
    """
    conn = get_conn()
    cur = conn.cursor()

    # (1) 姓名
    name = prompt_nonempty("輸入姓名: ")

    # (2) Email 驗證
    while True:
        email = prompt_nonempty("輸入 Email（必須為 XXX@gmail.com）: ")
        if validate_email(email):
            break
        print("Email 格式不符，重新輸入。")

    # (3) 密碼驗證
    while True:
        pw = prompt_nonempty("輸入密碼: ")
        ok, msg = validate_password(pw)
        if ok:
            break
        print(msg)

    # (4) 確認是否儲存
    print(f"save {name} | {email} | {pw} | Y / N ?")
    confirm = input().strip().upper()
    if confirm != "Y":
        print("已取消儲存，返回主選單。")
        conn.close()
        return

    # (5) 寫入 / 更新
    cur.execute("SELECT id FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    if row:
        print("Email 已存在，是否更新此 Email 資訊？(Y/N)")
        if input().strip().upper() == "Y":
            cur.execute(
                "UPDATE users SET name = ?, password = ? WHERE email = ?",
                (name, pw, email)
            )
            conn.commit()
            print("✅ 已更新使用者資訊。")
        else:
            print("已取消更新。")
    else:
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, pw)
        )
        conn.commit()
        print("✅ 已新增使用者。")

    conn.close()


# ----------------------------------------------------------- (b) 登入流程：sign_in() -----------------------------------------------------------
def sign_in():
    """
    登入流程：
    1) 先輸入 姓名 + Email
       - 查無 -> 顯示「名字或 Email 錯誤」並返回主選單提示
       - 查有 -> 進入密碼驗證
    2) 密碼驗證
       - 錯誤 -> 提示「忘記密碼 Y/N?」；Y 導到 sign_up（讓使用者重新註冊/更新）
       - 正確 -> 顯示登入成功
    """
    conn = get_conn()
    cur = conn.cursor()

    # (1) 基本身份核對
    name = prompt_nonempty("輸入姓名: ")
    email = prompt_nonempty("輸入 Email: ")

    cur.execute("SELECT password FROM users WHERE name = ? AND email = ?", (name, email))
    row = cur.fetchone()

    if not row:
        print("名字或 Email 錯誤。")
        print("(a) sign up / (b) sign in")
        conn.close()
        return

    db_pw = row[0]

    # (2) 密碼驗證
    while True:
        pw = prompt_nonempty("輸入密碼: ")
        if pw == db_pw:
            print("🎉 登入成功！")
            break
        else:
            print("密碼錯誤，忘記密碼 Y / N ?")
            choice = input().strip().upper()
            if choice == "Y":
                print("導向註冊模式...")
                conn.close()
                sign_up()
                break
            else:
                # 這行保留你的提示語氣：提醒使用者題目要求的三大限制
                print("請重新輸入密碼。至少包括三條限制( 字數8以上、包含大小寫英文和特殊字元、不可以連號...)")


# ----------------------------------------------------------- 主程式入口：main() -----------------------------------------------------------
def main():
    """
    主選單：
    (a) Sign up
    (b) Sign in
    (q) 離開
    """
    ensure_schema()

    print("=" * 48)
    print("  Homework 2: Sign up / Sign in (SQLite + Python)  ")
    print("=" * 48)

    while True:
        try:
            mode = input("請選擇模式 (a) Sign up / (b) Sign in / (q) 離開: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n收到中斷，系統結束。")
            break

        if mode == "a":
            try:
                sign_up()
            except Exception as e:
                print(f"發生錯誤：{e}")
        elif mode == "b":
            try:
                sign_in()
            except Exception as e:
                print(f"發生錯誤：{e}")
        elif mode == "q":
            print("系統結束，再見！")
            break
        else:
            print("輸入無效，請重新選擇。")


# ----------------------------------------------------------- Python 直跑保護 -----------------------------------------------------------
if __name__ == "__main__":
    # 確保以程式所在目錄為工作目錄（避免 DB 路徑混亂）
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        pass
    main()

