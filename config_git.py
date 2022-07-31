"""配置文件"""

# 数据库配置
HOSTNAME = ''
PORT = ''
DATABASE = ''
USERNAME = ''
PASSWORD = ''
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

# session加密字段
SECRET_KEY = ''

# 邮箱配置
# 项目中用的QQ邮箱
MAIL_SERVER = ''
MAIL_PORT = ''
MAIL_USE_TLS = ''
MAIL_USE_SSL = ''
MAIL_DEBUG = ''
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''
