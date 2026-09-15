import psycopg

# 把数据库配置集中放在这里
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "todo_db",
    "user": "postgres",
    "password": "123456"    # ⚠️ 改成你自己的密码
}


class TodoDB:
    """把数据库操作封装成一个类"""

    def _connect(self):
        # 每次操作都开一个新连接，用完就关，最简单最安全
        return psycopg.connect(**DB_CONFIG)

    def add(self, text):
        """添加待办，返回新记录的 id"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO todos (text) VALUES (%s) RETURNING id",
                    (text,)
                )
                new_id = cur.fetchone()[0]
            conn.commit()
        return new_id

    def list_all(self):
        """返回所有待办，每行是 (id, text, done)"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, text, done FROM todos ORDER BY id")
                return cur.fetchall()

    def toggle(self, todo_id):
        """切换完成状态，返回 True 表示改到了数据"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE todos SET done = NOT done WHERE id = %s",
                    (todo_id,)
                )
                affected = cur.rowcount
            conn.commit()
        return affected > 0

    def delete(self, todo_id):
        """删除，返回 True 表示删到了数据"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
                affected = cur.rowcount
            conn.commit()
        return affected > 0