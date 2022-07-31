from flask import Flask, render_template, session, g
from blueprints import user_bp, qa_bp
from exts import mail
import config
from flask_migrate import Migrate
from exts import db
from models import UserModel

'''这个是主文件, 项目运行就靠它, 他会调用其他需要的所有文件'''

app = Flask(__name__)
app.register_blueprint(user_bp)  # 注册蓝图
app.register_blueprint(qa_bp)
app.config.from_object(config)  # 引用配置文件
mail.init_app(app)  # 初始化对象
migrate = Migrate(app=app, db=db)  # 数据库ORM模型映射
db.init_app(app)


# 钩子: 这个函数的目的就是定义在请求所有的视图函数之前先干什么
@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # g: flask里面的全局变量 (这个项目中任何一个地方都可以用)
            # 给 g 绑定一个叫做 user 的变量, 他的值是 user 这个变量里面的值
            # setattr(g, 'user', user)  # setattr() 绑定函数
            g.user = user
        except:
            g.user = None


# 请求来了 -> before_request -> 视图函数 -> 视图函数中返回模板 -> context_processor


"""app_context_processor在flask中被称作上下文处理器，
借助app_context_processor我们可以让所有自定义变量在所有模板中全局可访问
函数的返回结果必须是dict，届时dict中的key将作为变量在所有模板中可见"""


# 上下文处理器
@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {}
