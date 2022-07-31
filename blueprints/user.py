from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
import string
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

"""这个视图文件主要写用户方面的, 比如登录, 注册等"""
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                # print(1)
                return redirect('/')
            else:
                # print(2)
                flash('邮箱和密码不匹配')
                return redirect(url_for('user.login'))
        else:
            # print(3)
            flash('邮箱和密码格式错误')
            return redirect(url_for('user.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data  # wtf是这么用的就这么用呗
            password = form.password.data
            username = form.username.data
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.register'))


@bp.route('/captcha', methods=['POST'])
def get_captcha():
    # 用户邮箱
    email = request.form.get('email')
    # 生成验证码
    letters = string.ascii_letters + string.digits
    captcha = ''.join(random.sample(letters, 4))
    if email:
        message = Message(
            subject='邮箱验证码',
            recipients=[email],
            body=f'【盛林科技】 您正在注册盛林科技官网, 验证码: {captcha}, 请不要告诉他人'
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
            # code: 200, 成功的 正常的请求
        return jsonify({'code': 200})
    else:
        # code: 400, 客户端错误
        return jsonify({'code': 400, 'message': '请先传递邮箱'})


@bp.route('/logout')
def logout():
    # 清除session所有的数据
    session.clear()
    return redirect(url_for('user.login'))
