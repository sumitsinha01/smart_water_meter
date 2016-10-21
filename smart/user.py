from smart import app
from flask_login import UserMixin


# silly user model
class User(UserMixin):
    def __init__(self, usr):
        self.id = usr['_id']
        self.name = usr['name']
        self.password = usr['password']
        self.apt_no = usr['apt_no']
        self.mobile = usr['mobile']
        self.email = usr['email']
        self.primary = usr['primary']
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

    def is_association(self):
        return self.id == 0

    def get(userid):
        app.logger.info("User.get id: " + userid.__str__())
        app.logger.info(type(userid))
        resident = app.mongo.db.residents.find_one({"_id": int(userid)})
        app.logger.info(resident)
        if resident:
            return User(resident)
        else:
            return None
