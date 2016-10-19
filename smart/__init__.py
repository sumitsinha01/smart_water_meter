from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)
app.config['MONGO2_DBNAME'] = 'swm'

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# mongodb connection
mongo = PyMongo(app, config_prefix='MONGO2')
app.mongo = mongo

handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

import smart.views

# month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', \
#             'November', 'December']


# def get_monthly_water_usage(user):
#     id = user.id
#     resident = mongo.db.residents.find_one({'_id': user.id})
#     app.logger.info(resident)
#     apt_no = resident['apt_no']
#     monthly_usage = {}
#
#     end_date = datetime.datetime.today()
#     delta_date = end_date - datetime.timedelta(6 * 365 / 12)
#     # delta_date = end_date - datetime.timedelta(days=2)
#     start_date = datetime.datetime(delta_date.year, delta_date.month, 1)
#     usage_details = mongo.db.usage.find({'apt_no': apt_no, 'date': {"$lt": end_date, "$gt": start_date}}).sort("date")
#     for usage in usage_details:
#         month = usage['date'].month
#         vol = usage['vol']
#         if month in monthly_usage.keys():
#             monthly_usage[month] += vol
#         else:
#             monthly_usage[month] = vol
#
#     return monthly_usage

# # silly user model
# class User(UserMixin):
#     def __init__(self, id, name):
#         app.logger.info("Init id: " + id.__str__() + " name: " + name)
#         self.id = id
#         self.name = name
#         self.active = True
#
#     def is_active(self):
#         # Here you should write whatever the code is
#         # that checks the database if your user is active
#         app.logger.info("is Active id: " + id.__str__() + " name: " + self.name)
#         return self.active
#
#     def is_anonymous(self):
#         app.logger.info("is_anonymous id: " + id.__str__() + " name: " + self.name)
#         return False
#
#     def is_authenticated(self):
#         app.logger.info("is_authenticated id: " + id.__str__() + " name: " + self.name)
#         return True
#
#     def __repr__(self):
#         return "%d/%s" % (self.id, self.name)
#
#     def get(userid):
#         app.logger.info("User.get id: " + userid.__str__())
#         app.logger.info(type(userid))
#         resident = mongo.db.residents.find_one({"_id": int(userid)})
#         app.logger.info(resident)
#         if resident:
#             return User(resident['_id'], resident['name'])
#         else:
#             return None
#

# create some users with ids 1 to 20       
# users = [User(id) for id in range(1, 21)]

# def get_water_usage(user):
#    mongo.db.find({'_id':user.get_id(), 'date':})




