from smart import app
from flask_login import UserMixin


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
        resident = app.mongo.db.residents.find_one({"_id": int(userid)})
        app.logger.info(resident)
        if resident:
            return User(resident['_id'], resident['name'])
        else:
            return None
