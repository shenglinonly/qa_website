import wtforms
from wtforms.validators import length, email, EqualTo, InputRequired
from models import EmailCaptchaModel, UserModel

"""这是一个表单校验文件, 
专门用来校验某些变量的格式对不对呀, 或者是校验两个变量相不相等呀
比如说密码是不是3到6位呀, 或者是用户登录时输入的账户密码和注册时数据库存储的账户密码是不是对应一致的
"""


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])

    # 只要这个类调用validate这个方法, 这些验证都会进行
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            print('邮箱验证码错误')
            raise wtforms.ValidationError('邮箱验证码错误')

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            print('邮箱已存在')
            raise wtforms.ValidationError('邮箱已存在')


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=20)])
    content = wtforms.StringField(validators=[length(min=6)])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])
