import os
import psycopg

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "todo_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "123456"),
}

class TodoDB:
    """把数据库操作封装成一个类"""

    def _connect(self):
        # 每次操作都开一个新连接，用完就关，最简单最安全
        return psycopg.connect(**DB_CONFIG)

# ========== 下面是用户相关的方法 ==========

    def create_user(self, username, password_hash):
        """创建用户，返回 True 成功，False 表示用户名已存在"""
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                        (username, password_hash)
                    )
                conn.commit()
            return True
        except psycopg.errors.UniqueViolation:
            return False

    def get_user(self, username):
        """按用户名查，返回 (id, username, password_hash) 或 None"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, username, password_hash FROM users WHERE username = %s",
                    (username,)
                )
                return cur.fetchone()

    def add(self, text, user_id, due_date=None, category="其他"):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO todos (text, user_id, due_date, category) VALUES (%s, %s, %s, %s) RETURNING id",
                    (text, user_id, due_date, category)
                )
                new_id = cur.fetchone()[0]
            conn.commit()
        return new_id

    def list_all(self, user_id, category=None, keyword=None):
        with self._connect() as conn:
            with conn.cursor() as cur:
                sql = "SELECT id, text, done, due_date, category FROM todos WHERE user_id = %s"
                params = [user_id]

                if category and category != "全部":
                    sql += " AND category = %s"
                    params.append(category)

                if keyword:
                    sql += " AND text ILIKE %s"
                    params.append(f"%{keyword}%")

                sql += " ORDER BY id"

                cur.execute(sql, params)
                return cur.fetchall()

    def toggle(self, todo_id, user_id):
        """切换状态，只能改自己的"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE todos SET done = NOT done WHERE id = %s AND user_id = %s",
                    (todo_id, user_id)
                )
                affected = cur.rowcount
            conn.commit()
        return affected > 0

    def delete(self, todo_id, user_id):
        """删除，只能删自己的"""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM todos WHERE id = %s AND user_id = %s",
                    (todo_id, user_id)
                )
                affected = cur.rowcount
            conn.commit()
        return affected > 0