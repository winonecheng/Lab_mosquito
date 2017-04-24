import re, requests
from mosquito.models import Dengue 
from datetime import datetime


file = requests.get("https://raw.githubusercontent.com/winonecheng/Lab_mosquito/master/mosquito/static/mosquito/10501011050119.txt")
pat = r'(\d+)/(\d+)/(\d+)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+).*?(\d+\.\d+)\s*(\d+\.+\d+)'
for line in file.text.splitlines():
    match = re.search(pat, line)
    if match:
    	date = datetime(year=int(match.group(1)), month=int(match.group(2)), day=int(match.group(3)))
    	dengue = Dengue(address=match.group(4)+match.group(5)+match.group(6), latitude=match.group(8), longitude=match.group(7), date=date)
    	dengue.save()
    	print(match.group(1)+match.group(2)+match.group(3))