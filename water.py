from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_pymongo import PyMongo
import flask_login
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
import logging
from logging.handlers import RotatingFileHandler
import datetime

app = Flask(__name__)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)
app.config['MONGO2_DBNAME'] = 'swm'

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#mongodb connection
mongo = PyMongo(app, config_prefix='MONGO2')

handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)  
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', \
#             'November', 'December']


def get_monthly_water_usage(user):
    id = user.id
    resident = mongo.db.residents.find_one({'_id':user.id})
    app.logger.info(resident)
    apt_no = resident['apt_no']
    monthly_usage = {}

    end_date = datetime.datetime.today()
    delta_date = end_date - datetime.timedelta(6*365/12)
    # delta_date = end_date - datetime.timedelta(days=2)
    start_date = datetime.datetime(delta_date.year,delta_date.month,1)
    usage_details = mongo.db.usage.find({'apt_no':apt_no, 'date': {"$lt": end_date, "$gt": start_date}}).sort("date")
    for usage in usage_details:
        month = usage['date'].month
        vol = usage['vol']
        if month in monthly_usage.keys():
            monthly_usage[month] += vol
        else:
            monthly_usage[month] = vol

    return monthly_usage


# silly user model
class User(UserMixin):

    def __init__(self, id, name):
        app.logger.info("Init id: " + id.__str__() + " name: " + name)
        self.id = id
        self.name = name
        self.active = True

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        app.logger.info("is Active id: " + id.__str__() + " name: " + self.name)
        return self.active

    def is_anonymous(self):
        app.logger.info("is_anonymous id: " + id.__str__() + " name: " + self.name)
        return False

    def is_authenticated(self):
        app.logger.info("is_authenticated id: " + id.__str__() + " name: " + self.name)
        return True
    
    def __repr__(self):
        return "%d/%s" % (self.id, self.name)
        
    def get(userid):
        app.logger.info("User.get id: " + userid.__str__())
        app.logger.info(type(userid))
        resident = mongo.db.residents.find_one({"_id":int(userid)})
        app.logger.info(resident)
        if resident:
            return User(resident['_id'], resident['name'])
        else:
            return None


# create some users with ids 1 to 20       
# users = [User(id) for id in range(1, 21)]

# def get_water_usage(user):
#    mongo.db.find({'_id':user.get_id(), 'date':})

# some protected url
@app.route('/')
@login_required
def home():
    error = None
    water_usage=get_monthly_water_usage(flask_login.current_user)
    return render_template('index.html', usage=water_usage)


 
# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        resident = mongo.db.residents.find_one({"email":username})
        app.logger.info("username: " + username  + " password " + password, "entered")
        app.logger.info(mongo)
        app.logger.info(mongo.db)
        app.logger.info(resident)
        app.logger.info(type(resident['_id']))

        if resident and resident['primary'] and resident['password'] == password:
            app.logger.info("Login Success")
        #if password == "sumit":
            user = User(resident['_id'],resident['name'])
            login_user(user)
            session['username'] = username
            #print("success")
            next = request.args.get('next')
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            #if not next_is_valid(next):
            #    return flask.abort(400)

            #return redirect(next or url_for('home'))
            return redirect(request.args.get("next"))
        else:
            error = 'Invalid username/password'
    
    return render_template('login.html', error=error)



# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    app.logger.info("load user id: " + userid.__str__())
    return User.get(userid)
    

if __name__ == "__main__":
    #logger
    logger=logging.getLogger(__name__)

    
    app.run()