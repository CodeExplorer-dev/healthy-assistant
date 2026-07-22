from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest, RegisterResponse


# 所有认证接口统一使用 /api/v1/auth 前缀。
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
) -> RegisterResponse:
    # 简单项目不校验邮箱格式，但去除空格并统一小写，
    # 防止 Test@Example.com 与 test@example.com 被重复注册。
    email = payload.email.strip().lower()

    # Field(min_length=1) 会在清理前校验，因此额外处理全空格账号。
    if not email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="账号不能为空",
        )

    # 先检查账号是否已存在，给出明确的业务错误。
    existing_user = db.scalar(select(User).where(User.email == email))
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="该账号已注册",
        )

    user = User(
        email=email,
        # 只保存 bcrypt 哈希，绝不保存明文密码。
        password_hash=hash_password(payload.password),
        nickname=payload.nickname,
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        # 并发请求可能同时通过前面的查询；
        # 最终仍由数据库的唯一索引阻止重复账号。
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="该账号已注册",
        ) from None

    # 提交后刷新对象，获取数据库生成的 id 等字段。
    db.refresh(user)

    # 响应不包含密码或 password_hash。
    return RegisterResponse(
        id=user.id,
        email=user.email,
        nickname=user.nickname,
    )