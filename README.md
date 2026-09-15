# 我的待办清单 API

用 FastAPI + PostgreSQL 做的待办清单项目。

## 功能
- 添加待办
- 查看全部
- 切换完成状态
- 删除待办

## 运行方式
1. 装依赖：`pip install fastapi uvicorn psycopg[binary]`
2. 启动：`python -m uvicorn api:app --reload`
3. 打开文档：http://127.0.0.1:8000/docs
4.http://127.0.0.1:8000/