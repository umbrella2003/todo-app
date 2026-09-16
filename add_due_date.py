import psycopg
import os

conn = psycopg.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    dbname=os.getenv("DB_NAME", "todo_db"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "123456"),  # ⚠️ 改密码
)

with conn.cursor() as cur:
    cur.execute("""
        ALTER TABLE todos
        ADD COLUMN IF NOT EXISTS due_date DATE
    """)
    conn.commit()

print("✅ todos 表加了 due_date 列")

conn.close()