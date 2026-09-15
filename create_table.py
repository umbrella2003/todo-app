import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="todo_db",
    user="postgres",
    password="123456"    # 改成你自己的密码
)

# 建表
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()

print("表 todos 创建成功！")

# 看看表结构
with conn.cursor() as cur:
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'todos'
    """)
    for row in cur.fetchall():
        print(row)

conn.close()