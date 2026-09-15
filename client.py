import requests

BASE = "http://127.0.0.1:8000"

# ===== 1. 查全部 =====
print("📋 当前列表：")
r = requests.get(f"{BASE}/todos")
for item in r.json():
    print(item)

# ===== 2. 添加一条 =====
print("\n➕ 添加一条：")
r = requests.post(f"{BASE}/todos", json={"text": "用 requests 添加的"})
print("状态码:", r.status_code)
print("返回:", r.json())
new_id = r.json()["id"]

# ===== 3. 切换完成状态 =====
print(f"\n🔁 切换 id={new_id} 的状态：")
r = requests.patch(f"{BASE}/todos/{new_id}")
print("返回:", r.json())

# ===== 4. 再看一遍 =====
print("\n📋 再看一遍：")
for item in requests.get(f"{BASE}/todos").json():
    print(item)

# ===== 5. 删除 =====
print(f"\n🗑️ 删除 id={new_id}：")
r = requests.delete(f"{BASE}/todos/{new_id}")
print("返回:", r.json())

# ===== 6. 试试删不存在的 =====
print("\n❓ 删一个不存在的 id=99999：")
r = requests.delete(f"{BASE}/todos/99999")
print("状态码:", r.status_code)
print("返回:", r.json())

# ===== 7. 最终结果 =====
print("\n📋 最终列表：")
for item in requests.get(f"{BASE}/todos").json():
    print(item)