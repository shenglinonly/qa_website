from .user import bp as user_bp
from .qa import bp as qa_bp


"""
python软件包与普通文件夹的不同就是他有这个文件
这个文件的作用就是可以把文件当模块使用
普通文件引用: from blueprint.qa import bp as qa_bp
python软件包: from blueprint import qa_bp 
就是只要在init文件说明一下(就像上面那样)之后, 其他文件就可以直接引用某个文件里面的某个函数或者变量
"""
