import json, os

FILE = "todos.json"

class TodoApp:
    def __init__(self):
        self.todos = self._load()

    def _load(self):
        if not os.path.exists(FILE):
            return []
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save(self):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def add(self, text):
        self.todos.append(text)
        self._save()
        print(f"已添加：{text}")

    def list_all(self):
        if not self.todos:
            print("暂无待办")
            return
        for i, t in enumerate(self.todos):
            print(f"{i}. {t}")

    def run(self):
        while True:
            cmd = input("命令 (add/list/quit): ")
            if cmd == "add":
                self.add(input("内容: "))
            elif cmd == "list":
                self.list_all()
            elif cmd == "quit":
                self._save()
                break

TodoApp().run()