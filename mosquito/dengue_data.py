import re, requests

def data(n):
    addressPoints = []
    if n==1:
        #file = open(static("mosquito/10501011050119.txt"),'r',encoding = 'utf8')
        file = requests.get("https://raw.githubusercontent.com/winonecheng/Lab_mosquito/master/mosquito/static/mosquito/10501011050119.txt")
        pat = r'([\u4e00-\u9fa5]+里).*?(\d+\.\d+)\s*(\d+\.+\d+)'
        #print(file.text)
        for line in file.text.splitlines():
            match = re.search(pat, line)
            if match:
                addressPoints.append([match.group(1),match.group(2),match.group(3)])
    elif n==2:
#        file = open(static("mosqutio/aaa.csv"),'r',encoding = 'utf8')
        file = requests.get("https://raw.githubusercontent.com/winonecheng/Lab_mosquito/master/mosquito/static/mosquito/aaa.csv")
        pat = r'(\d*\.\d*),(\d*\.\d*)'
        for line in file.text.splitlines():
            match = re.search(pat, line)
            if match:
                addressPoints.append([match.group(2),match.group(1)])
    else:
        pass
    #print(addressPoints)
    return addressPoints