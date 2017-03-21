import re, csv
from django.contrib.staticfiles.templatetags.staticfiles import static

def data(n):
    addressPoints = []
    if n==1:
        file = open(static("mosquito/10501011050119.txt"),'r',encoding = 'utf8')
        pat = r'([\u4e00-\u9fa5]+里).*?(\d+\.\d+)\s*(\d+\.+\d+)'
        for line in file:
            match = re.search(pat, line)
            if match:
                addressPoints.append([match.group(1),match.group(2),match.group(3)])
    elif n==2:
        file = open(static("mosqutio/aaa.csv"),'r',encoding = 'utf8')
        for line in csv.DictReader(file):
            addressPoints.append([line['long'], line['lat']])
    else:
        pass
    print(addressPoints)
    return addressPoints
