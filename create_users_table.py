import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="todo_db",
    user="postgres",
    password="123456"    # ⚠️ 改成你的密码
)

with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()

print("✅ users 表创建成功！")

# 看一下表结构
with conn.cursor() as cur:
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'users'
    """)
    for row in cur.fetchall():
        print(row)

conn.close()