import datetime


def currentDate():
    currentTime = datetime.datetime.now()
    currentDate = currentTime.date().strftime("%Y-%m-%d")
    return currentDate
