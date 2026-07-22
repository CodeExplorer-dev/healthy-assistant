from pydantic import BaseModel, Field, field_validator


class RegisterRequest(BaseModel):
    # 简单项目：仅要求账号不为空，不校验邮箱格式。
    email: str = Field(min_length=1, max_length=255)

    # bcrypt 最多处理 72 字节，注册阶段提前限制。
    password: str = Field(min_length=8, max_length=72)

    # 昵称可选。
    nickname: str | None = Field(default=None, max_length=50)

    @field_validator("password")
    @classmethod
    def password_must_fit_bcrypt(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("密码不能超过 72 个 UTF-8 字节")
        return value


class RegisterResponse(BaseModel):
    id: int
    email: str
    nickname: str | None