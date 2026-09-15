from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from db import TodoDB
from fastapi.staticfiles import StaticFiles
from auth import hash_password, verify_password, create_token, get_current_user

app = FastAPI(title="待办清单 API")
db = TodoDB()


# 请求体格式：POST /todos 时，body 里传 {"text": "xxx"}
class TodoIn(BaseModel):
    text: str
class UserIn(BaseModel):
    username: str
    password: str


@app.post("/register")
def register(user: UserIn):
    hashed = hash_password(user.password)
    ok = db.create_user(user.username, hashed)
    if not ok:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return {"ok": True, "username": user.username}

@app.get("/todos")
def list_todos(username: str = Depends(get_current_user)):
    # 先把 username 转成 user_id
    row = db.get_user(username)
    user_id = row[0]

    rows = db.list_all(user_id)
    return [
        {"id": r[0], "text": r[1], "done": r[2]}
        for r in rows
    ]


@app.post("/todos")
def add_todo(item: TodoIn, username: str = Depends(get_current_user)):
    row = db.get_user(username)
    user_id = row[0]

    new_id = db.add(item.text, user_id)
    return {"id": new_id, "text": item.text, "done": False}


@app.patch("/todos/{todo_id}")
def toggle_todo(todo_id: int, username: str = Depends(get_current_user)):
    row = db.get_user(username)
    user_id = row[0]

    ok = db.toggle(todo_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="待办不存在")
    return {"ok": True}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, username: str = Depends(get_current_user)):
    row = db.get_user(username)
    user_id = row[0]

    ok = db.delete(todo_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="待办不存在")
    return {"ok": True}
    
@app.post("/login")
def login(user: UserIn):
    # 1. 查用户
    row = db.get_user(user.username)
    if row is None:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    user_id, username, password_hash = row

    # 2. 验证密码
    if not verify_password(user.password, password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 3. 生成令牌
    token = create_token(username)
    return {"access_token": token, "token_type": "bearer"}
    # 把 static 文件夹挂到根路径，提供网页
app.mount("/", StaticFiles(directory="static", html=True), name="static")