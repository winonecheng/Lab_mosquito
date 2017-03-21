from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render


from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage

from .models import User
import re, json
from .dengue_data import data

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
     
def create_row_in_db(id):
    user = User(uid=id, report_date=timezone.now())
    user.save()

def update_user_data(id, message):
    user = User.objects.filter(uid=id).order_by('-report_date')[0]
    if user.state == 0:
        user.temperature = message
        user.state = 1
        user.save()

    elif user.state == 1:
        user.address = message.address
        user.latitude = message.latitude
        user.longitude = message.longitude
        user.state = 2
        user.save()

    else:
        print("update data error!!")

def handle_input_of_temperature(id, message):
    pat = r'^\s*(\d+\.*\d*)\s*'u'(度)'
    str = message.text
    match = re.search(pat,str)
    if match:
        update_user_data(id, float(match.group(1)))
        return 1
    else:
        return 0

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                profile = line_bot_api.get_profile(event.source.user_id)
                try:
                    state = User.objects.filter(uid=profile.user_id).order_by('-report_date')[0].state
                except:
                    state = -1                

                if isinstance(event.message, TextMessage):
                    if "回報" in event.message.text:
                        print(profile.user_id+"要回報")
                        create_row_in_db(profile.user_id)
                        state = 0

                    else:
                        if state == 0:
                            print(profile.user_id+"輸入體溫")
                            if(handle_input_of_temperature(profile.user_id, event.message)):
                                state = 1

                elif isinstance(event.message, LocationMessage):
                    if state == 1:
                        print(profile.user_id+"輸入地點")
                        update_user_data(profile.user_id, event.message)
                        state = 2
                else:
                    pass

                """ handle replay message """
                reply_text = ""
                if state == 0:
                    reply_text = "請問你現在的體溫？\n(ex：27.5度)"
                elif state == 1:
                    reply_text = "請問你的所在地？\n(使用「位置訊息」功能)"
                elif state == 2:
                    reply_text = "回報成功！\n(輸入「回報」 可再次回報)"
                else:
                    reply_text = "嗨，"+profile.display_name+"\n你要回報嗎？\n(輸入「回報」 開始回報)"

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=reply_text)
                )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def map(request):
    json_addressPoints1 = json.dumps(data(1),ensure_ascii=False)
    json_addressPoints2 = json.dumps(data(2),ensure_ascii=False)
#    print(json_addressPoints1)
#    print(json_addressPoints2)
    return render(request, 'mosquito/map.html',{'addressPoints1':json_addressPoints1, 'addressPoints2':json_addressPoints2})
