import codecs
import csv
import requests
from fastapi import status


def validateURL(url):
    r = requests.head(url)
    if r.status_code == status.HTTP_404_NOT_FOUND:
        return False
    return True


def fetchCSV(url):
    response = requests.get(url)
    text = codecs.iterdecode(response.iter_lines(), 'utf-8')
    reader = csv.reader(text, delimiter=',')
    headers = next(reader)
    intCols = ['discount', 'likes_count', 'id']
    floatCols = ['current_price', 'raw_price']
    for line in reader:
        rowDict = {}
        for key, value in zip(headers, line):
            if value == '':
                rowDict[key] = None
            elif value == 'true':
                rowDict[key] = True
            elif value == 'false':
                rowDict[key] = False
            elif key in intCols:
                rowDict[key] = int(value)
            elif key in floatCols:
                rowDict[key] = float(value)
            else:
                rowDict[key] = value
        yield rowDict
