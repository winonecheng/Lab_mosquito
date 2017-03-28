from .views import line_bot_api
from .models import User
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

def push(address_filter, msg):
    push_uid = [];
    for obj in User.objects.filter(address__contains=address_filter):
        push_uid.append(obj.uid)

    try:
        line_bot_api.multicast(push_uid,TextSendMessage(text=msg))
    except LineBotApiError as e:
        print(e.status_code)
        print(e.error.message)
        print(e.error.details)
