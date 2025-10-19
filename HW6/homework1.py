import sqlite3, os

# --- 固定連線到正確 DB（你的絕對路徑） ---
DB = os.path.join(os.path.dirname(__file__), "ID_data.db")
if not os.path.exists(DB):
    raise FileNotFoundError(f"❌ 找不到資料庫：{DB}\n請確認檔案路徑正確。")
print(f"✅ 成功連線資料庫：{DB}")

def get_conn():
    return sqlite3.connect(DB)

# --- 身分證驗證核心 ---
def id_valid(id_str: str) -> bool:
    table = {
        'A':10,'B':11,'C':12,'D':13,'E':14,'F':15,'G':16,'H':17,
        'I':34,'J':18,'K':19,'L':20,'M':21,'N':22,'O':35,'P':23,
        'Q':24,'R':25,'S':26,'T':27,'U':28,'V':29,'W':32,'X':30,
        'Y':31,'Z':33
    }
    s = (id_str or "").strip().upper()
    # 長度/型別基本檢查
    if len(s) != 10 or s[0] not in table or not s[1:].isdigit():
        return False

    # ❶ 第二碼僅允許 {1,2,8,9}：本國男/女、外籍男/女
    if s[1] not in {'1', '2', '8', '9'}:
        return False

    n = table[s[0]]
    digits = [n // 10, n % 10] + [int(x) for x in s[1:]]   # 共 11 位
    weights = [1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1]            # 共 11 個權重

    return sum(d*w for d, w in zip(digits, weights)) % 10 == 0

def find_last_digit(id9: str):
    if not id9 or not id9[0].isalpha():
        return None
    for d in range(10):
        if id_valid(id9 + str(d)):
            return d
    return None

# --- DB schema/欄位健檢 ---
def ensure_columns(cur):
    cols = {row[1] for row in cur.execute("PRAGMA table_info('ID_table')")}
    for name in ("country", "gender", "citizenship"):
        if name not in cols:
            cur.execute(f"ALTER TABLE ID_table ADD COLUMN {name} TEXT")

# --- Step 1: 補上驗證碼 ---
def fill_check_digit(cur) -> int:
    cur.execute("SELECT id FROM ID_table WHERE LENGTH(id)=9")
    need = [r[0] for r in cur.fetchall()]
    filled = 0
    for pid in need:
        last = find_last_digit(pid)
        if last is not None:
            cur.execute("UPDATE ID_table SET id=? WHERE id=?", (pid+str(last), pid))
            filled += 1
    return filled

# --- Step 2: 刪除假身分證（一次刪除所有錯誤資料） ---
def delete_invalid_ids(cur) -> int:
    # 先正規化，避免大小寫/空白造成誤判
    cur.execute("UPDATE ID_table SET id = UPPER(TRIM(id))")

    # 🔸 先一次取出所有 ID（不要邊查邊刪）
    cur.execute("SELECT id FROM ID_table")
    all_ids = [r[0] for r in cur.fetchall()]

    # 🔸 判斷哪些是無效的
    to_del = [(pid,) for pid in all_ids if not id_valid(pid)]

    # 🔸 一次刪除所有無效資料
    if to_del:
        cur.executemany("DELETE FROM ID_table WHERE id = ?", to_del)

    # 🔸 回傳刪除筆數
    return len(to_del)

# --- Step 3: 標註含意（含 citizenship 規則） ---
def annotate_meanings(cur) -> int:
    cur.execute("SELECT id FROM ID_table")
    kept = [r[0] for r in cur.fetchall() if id_valid(r[0])]
    updated = 0
    for pid in kept:
        gender = "male" if pid[1] == "1" else "female"

        sec = pid[1]  # 第二碼
        thr = pid[2]  # 第三碼

        if thr == "6":
            citizenship = "foreigner"       # 原為外國人入籍
        elif thr == "7":
            citizenship = "no citizenship"    # 無戶籍國民
        elif thr == "8":
            citizenship = "hk mac"          # 港澳居民
        elif thr == "9":
            citizenship = "china"           # 大陸地區居民
        else:
            citizenship = "taiwan"          # 在台本籍國民 (0–5)

        cur.execute("SELECT region FROM country WHERE sign=?", (pid[0],))
        region = (cur.fetchone() or [None])[0]

        cur.execute("""
            UPDATE ID_table
               SET country=?, gender=?, citizenship=?
             WHERE id=?""", (region, gender, citizenship, pid))
        updated += 1
    return updated

# --- Step 4: 互動查詢（補上你缺的函式） ---
def interactive_lookup(cur):
    while True:
        pid = input("請輸入身分證字號：").upper().strip()
        if not id_valid(pid):
            print("❌ 無效的身分證字號，請重新輸入。\n")
            continue
        gender = "男性" if pid[1] == "1" else "女性"
        cur.execute("SELECT region FROM country WHERE sign=?", (pid[0],))
        region = (cur.fetchone() or [None])[0]
        print(f"✅ {pid} 為真實身分證，代表 {region} {gender} 台灣出生之本籍國民")
        break

def main():
    with get_conn() as conn:
        cur = conn.cursor()

        ensure_columns(cur); conn.commit()

        conn.execute("BEGIN")
        filled = fill_check_digit(cur); conn.commit()
        print(f"補上驗證碼：{filled} 筆")

        conn.execute("BEGIN")
        removed = delete_invalid_ids(cur); conn.commit()
        print(f"移除假身分證：{removed} 筆")

        conn.execute("BEGIN")
        updated = annotate_meanings(cur); conn.commit()
        print(f"標註含意（country/gender/citizenship）：{updated} 筆")

        interactive_lookup(cur)

if __name__ == "__main__":
    main()

