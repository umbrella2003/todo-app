from db import TodoDB

db = TodoDB()

# 1. 添加
new_id = db.add("用类重构测试")
print("✅ 添加成功，新 id =", new_id)

# 2. 查询
print("\n📋 当前列表：")
for row in db.list_all():
    print(row)

# 3. 切换完成状态
db.toggle(new_id)
print("\n✅ 已切换 id =", new_id)

# 4. 再查
print("\n📋 再看一遍：")
for row in db.list_all():
    print(row)

# 5. 删除
db.delete(new_id)
print("\n✅ 已删除 id =", new_id)

# 6. 最终结果
print("\n📋 最终结果：")
for row in db.list_all():
    print(row)