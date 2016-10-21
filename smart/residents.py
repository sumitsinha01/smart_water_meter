from smart import app
import datetime

monthNames = ["January", "February", "March", "April", "May", "June", \
             "July", "August", "September", "October", "November", "December"];


# returns total usage in last delta number of months
# delta : no of months
# delta = 0 : current month
def get_last_month_total_usage(user, delta):
    # userid = int(user.get_id())
    # resident = app.mongo.db.residents.find_one({'_id': userid})
    # app.logger.info(user.get_id())
    # app.logger.info(resident)
    # apt_no = resident['apt_no']
    apt_no = user.apt_no
    today = datetime.datetime.today()
    if delta > 0:
        end_date = datetime.datetime(today.year, today.month, 1)
    else:
        end_date = today
    month = end_date.month - delta
    if month < 0:
        month = 0
        year = end_date.year - 1
    else:
        year = end_date.year
    start_date = datetime.datetime(year, month, 1)
    if delta == 0:
        start_date -= datetime.timedelta(days=1)
    app.logger.info(end_date)
    app.logger.info(start_date)
    if apt_no == 0:
        # association user: fetch complete bulding data
        usage_details = app.mongo.db.usage.find({'date': {"$lt": end_date, "$gt": start_date}}).sort("date")
    else :
        usage_details = app.mongo.db.usage.find( \
            {'apt_no': apt_no, 'date': {"$lt": end_date, "$gt": start_date}}).sort("date")
    sum = 0
    for usage in usage_details:
        sum += usage['vol']
    return sum


def get_monthly_water_usage(user):
    # userid = int(user.get_id())
    # resident = app.mongo.db.residents.find_one({'_id': userid})
    # app.logger.info(resident)
    # apt_no = resident['apt_no']
    apt_no = user.apt_no
    monthly_usage = {}

    end_date = datetime.datetime.today()
    delta_date = end_date - datetime.timedelta(6 * 365 / 12)
    # delta_date = end_date - datetime.timedelta(days=2)
    start_date = datetime.datetime(delta_date.year, delta_date.month, 1)
    if apt_no == 0:
        # association user: fetch complete bulding data
        usage_details = app.mongo.db.usage.find({'date': {"$lt": end_date, "$gt": start_date}}).sort("date")
    else:
        usage_details = app.mongo.db.usage.find({'apt_no': apt_no, 'date': {"$lt": end_date, "$gt": start_date}}).sort("date")
    for usage in usage_details:
        month = usage['date'].month
        year = usage['date'].year
        vol = usage['vol']
        key = datetime.date(year, month , 1)
        if key in monthly_usage.keys():
                monthly_usage[key] += vol
        else:
            monthly_usage[key] = vol

    return monthly_usage


def get_weekly_water_usage(user):
    # userid = int(user.get_id())
    # resident = app.mongo.db.residents.find_one({'_id': userid})
    # app.logger.info(resident)
    # apt_no = resident['apt_no']
    apt_no = user.apt_no
    weekly_usage = {}
    days =[]

    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=6)
    app.logger.info(start_date.__str__() + " " + end_date.__str__())
    if apt_no == 0:
        # association user: fetch complete bulding data
        usage_details = app.mongo.db.usage.find({'date': {"$lt": end_date, "$gt": start_date}}).sort("date")
    else :
        usage_details = app.mongo.db.usage.find({'apt_no': apt_no, 'date': {"$lt": end_date, "$gt": start_date}}).sort("date")
    for i in range(7):
        weekday = (start_date + datetime.timedelta(days=i)).weekday()
        weekly_usage[weekday] = 0

    for usage in usage_details:
        weekday = usage['date'].weekday()
        day = usage['date'].day
        vol = usage['vol']
        if weekday in weekly_usage.keys():
            weekly_usage[weekday] += vol
        else:
            weekly_usage[weekday] = vol

        if day not in days:
            days.append(day)

    app.logger.info(days)

    return weekly_usage

