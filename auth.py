from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

# ========== 密码哈希 ==========
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """把明文密码变成哈希"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """验证密码是否正确"""
    return pwd_context.verify(plain, hashed)


# ========== JWT ==========
SECRET_KEY = "123456789"  # 后面登录要用
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24   # 令牌有效期 24 小时

def create_token(username: str) -> str:
    """根据用户名生成 JWT 令牌"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str:
    """解码 JWT，返回用户名；失败会抛异常"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["sub"]

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """从请求头里取出 JWT，验证并返回用户名"""
    try:
        username = decode_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效或过期的令牌"
        )
    return username