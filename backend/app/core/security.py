import bcrypt

def hash_password(password: str) -> str:
    """
    注册时将明文密码变为 bcrypt 哈希，存到数据库的 password_hash
    """
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    """ 
    登录时验证用户输入的密码是否与数据库哈希匹配
    """
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        return False