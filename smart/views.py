from smart import app,login_manager
from flask import Response, redirect, url_for, request, session, render_template
import flask_login
from flask_login import login_required, login_user, logout_user
from smart import residents
from smart.user import User


# some protected url
@app.route('/')
@login_required
def home():
    current_user = flask_login.current_user
    app.logger.info(current_user)
    current_usage = residents.get_last_month_total_usage(current_user, 0)
    monthly_usage = residents.get_monthly_water_usage(current_user)
    weekly_usage = residents.get_weekly_water_usage(current_user)
    return render_template('index.html', usage=dict(current=current_usage, monthly=monthly_usage, weekly=weekly_usage))


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        resident = app.mongo.db.residents.find_one({"email": username})
        app.logger.info("username: " + username + " password " + password, "entered")
        app.logger.info(app.mongo)
        app.logger.info(app.mongo.db)
        app.logger.info(resident)
        app.logger.info(type(resident['_id']))

        if resident and resident['primary'] and resident['password'] == password:
            app.logger.info("Login Success")
            # if password == "sumit":
            user = User(resident['_id'], resident['name'])
            login_user(user)
            session['username'] = username
            # print("success")
            # next = request.args.get('next')
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            # if not next_is_valid(next):
            #    return flask.abort(400)

            # return redirect(next or url_for('home'))
            #return redirect(request.args.get("next"))
            return redirect(url_for('home'))
        else:
            error = 'Invalid username/password'

    return render_template('login.html', error=error)


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('login'))


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    app.logger.info("load user id: " + userid.__str__())
    return User.get(userid)

