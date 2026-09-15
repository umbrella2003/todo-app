import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="todo_db",
    user="postgres",
    password="123456"    # 改成你自己的密码
)

# ===== 1. 插入三条数据 =====
with conn.cursor() as cur:
    cur.execute("INSERT INTO todos (text) VALUES (%s)", ("学 Python",))
    cur.execute("INSERT INTO todos (text) VALUES (%s)", ("学 FastAPI",))
    cur.execute("INSERT INTO todos (text) VALUES (%s)", ("学 PostgreSQL",))
    conn.commit()
print("✅ 插入完成")

# ===== 2. 查询全部 =====
print("\n📋 当前所有待办：")
with conn.cursor() as cur:
    cur.execute("SELECT id, text, done FROM todos ORDER BY id")
    for row in cur.fetchall():
        print(row)

# ===== 3. 把 id=1 的改成完成 =====
with conn.cursor() as cur:
    cur.execute("UPDATE todos SET done = TRUE WHERE id = %s", (1,))
    conn.commit()
print("\n✅ 已把 id=1 标记为完成")

# ===== 4. 再看一遍 =====
print("\n📋 再看一遍：")
with conn.cursor() as cur:
    cur.execute("SELECT id, text, done FROM todos ORDER BY id")
    for row in cur.fetchall():
        print(row)

# ===== 5. 删除 id=3 =====
with conn.cursor() as cur:
    cur.execute("DELETE FROM todos WHERE id = %s", (3,))
    conn.commit()
print("\n✅ 已删除 id=3")

# ===== 6. 最终结果 =====
print("\n📋 最终结果：")
with conn.cursor() as cur:
    cur.execute("SELECT id, text, done FROM todos ORDER BY id")
    for row in cur.fetchall():
        print(row)

conn.close()