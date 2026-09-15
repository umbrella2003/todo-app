import psycopg

# 注意：password 换成你安装时设的密码！
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="todo_db",
    user="postgres",
    password="123456"
)

print("连接成功！")

# 查一下 PostgreSQL 版本
with conn.cursor() as cur:
    cur.execute("SELECT version()")
    print(cur.fetchone())

conn.close()