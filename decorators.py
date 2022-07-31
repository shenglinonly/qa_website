from flask import g, redirect, url_for
from functools import wraps

"""装饰器文件, 专门存放自定义的装饰器"""

"""装饰器, 具体可看高级开发课件"""
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)  # 这个func就是正常的试图函数
        else:
            return redirect(url_for('user.login'))

    return wrapper
