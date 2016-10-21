from smart import app
import random


def get_dashboard_apt_list():
    apts = app.mongo.db.residents.distinct("apt_no")
    apts.sort()

    apt_list={}
    for apt in apts:
        # color: 0 red, 1 green
        if apt == 0:
            continue
        color = bool(random.getrandbits(1))
        apt_list[apt]=color

    return apt_list
