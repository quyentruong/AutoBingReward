import json
import os
from datetime import datetime


def readjson(file):
    if not os.path.isfile(file):
        f = open(file, 'w')
        json.dump(dict(), f)
        f.close()
        # return readjson(file)
    with open(file) as json_data_file:
        data = json.load(json_data_file)
    return data


def writejson(file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile)


def toStrtime(datetime_):
    return datetime_.strftime("%a, %d %b %Y %H:%M:%S")


def toDatetime(strtime):
    return datetime.strptime(strtime, "%a, %d %b %Y %H:%M:%S")
