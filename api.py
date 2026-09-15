from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import TodoDB

app = FastAPI(title="待办清单 API")
db = TodoDB()


# 请求体格式：POST /todos 时，body 里传 {"text": "xxx"}
class TodoIn(BaseModel):
    text: str


# ============ 接口 1：列出全部 ============
@app.get("/todos")
def list_todos():
    rows = db.list_all()
    # 把元组转成字典，方便前端识别
    return [
        {"id": r[0], "text": r[1], "done": r[2]}
        for r in rows
    ]


# ============ 接口 2：添加一条 ============
@app.post("/todos")
def add_todo(item: TodoIn):
    new_id = db.add(item.text)
    return {"id": new_id, "text": item.text, "done": False}


# ============ 接口 3：切换完成状态 ============
@app.patch("/todos/{todo_id}")
def toggle_todo(todo_id: int):
    ok = db.toggle(todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="待办不存在")
    return {"ok": True}


# ============ 接口 4：删除一条 ============
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    ok = db.delete(todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="待办不存在")
    return {"ok": True}