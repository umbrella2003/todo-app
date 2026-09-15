import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="todo_db",
    user="postgres",
    password="123456"    # ⚠️ 改成你的密码
)

with conn.cursor() as cur:
    # 加一列 user_id，允许空（因为老数据没有归属）
    cur.execute("""
        ALTER TABLE todos
        ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id)
    """)
    conn.commit()

print("✅ todos 表加了 user_id 列")

conn.close()