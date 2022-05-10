from pymongo import MongoClient
from getTime import currentDate
import schedule
import time
cluster = MongoClient("mongodb://localhost:27017/")
db = cluster["CGUScholar"]


def count_userIDinlabel():
    print('start userID in label counter')
    today = currentDate()
    print(today)
    getlabelname = list(db.LabelDomain.find(
        {"updateTime": {"$regex": today}}))
    if len(getlabelname) == 0:
        return
    for label in getlabelname:
        todayrecord = {}
        userIDlength = len(label['userID'])
        if userIDlength == 0:
            continue
        todayrecord['updateTime'] = today
        todayrecord['userIDcount'] = userIDlength
        
        if db.Statistical_data.count_documents({'_id': label['_id']}, limit=1) != 0:
            print(label['_id'] + ' update ' + str(todayrecord['userIDcount']))
            insertrecord = {'$push': {'countRecord': {'$each': [todayrecord]}}}
            db.Statistical_data.update_one({'_id': label['_id']}, insertrecord)
        else:
            insertrecord = {'_id':label['_id'],'countRecord': [todayrecord]}
            db.Statistical_data.insert_one(insertrecord)
            print(label['_id'] + ' insert ' + str(todayrecord['userIDcount']))
    return


schedule.every().day.at('23:59').do(count_userIDinlabel)
if __name__ == '__main__':
    while 1:
        schedule.run_pending()
        time.sleep(59)
