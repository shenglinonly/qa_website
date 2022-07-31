from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
db = SQLAlchemy()

"""这个文件的目的就是存放一些需要反复调用的东西, 这样就不用每个文件都import一下Mail呀SQLAlchemy呀什么的,然后才能获取到对象
 只需要import一下这个文件, 然后直接调用这个文件里面的mail呀db呀对象"""
