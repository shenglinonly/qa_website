from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from decorators import login_required
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from sqlalchemy import or_

'''这是一个蓝图里面的视图函数文件, 
qa的意思就是question和answer
这里面主要是写问答页面的逻辑功能
如发布问答, 评论等
'''

"""声明蓝图, 
并且取个名字, 一般蓝图的名字就是文件名(q'a), 
__name__: 固定写法
url_prefix:这个是说明这个蓝图是在什么url之后(或者是说这个蓝图的前缀url), 就是这个蓝图里面的所有视图函数都默认在这个url之后
最后把这个蓝图给的一个变量(bp), 之后就用这个变量来注册路由了
"""
bp = Blueprint('qa', __name__, url_prefix='/')


# 直接把问答页面当成首页
@bp.route('/')
def index():
    questions = QuestionModel.query.order_by(db.text('-create_time')).all()
    return render_template('index.html', questions=questions)


@bp.route('/question/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            flash('标题或者内容格式有误')
            return redirect(url_for('qa.public_question'))


@bp.route('/question/<int:question_id>')
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template('detail.html', question=question)


@bp.route('/answer/<int:question_id>', methods=['POST'])
@login_required
def answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer_model = AnswerModel(content=content, author=g.user, question_id=question_id)
        db.session.add(answer_model)
        db.session.commit()
        return redirect(url_for('qa.question_detail', question_id=question_id))
    else:
        flash('表单验证失败 !')
        return redirect(url_for('qa.question_detail', question_id=question_id))


@bp.route('/search')
def search():
    # /search?q=xxx
    q = request.args.get('q')
    # filter_by: 直接使用字段名称
    # filter: 使用模型.字段名称
    questions = QuestionModel.query.filter(or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q))).order_by(db.text('-create_time'))
    return render_template('index.html', questions=questions)
