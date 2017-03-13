from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from .models import User

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
     
def create_row_in_db(id):
    user = User(uid=id)
    user.save()

def update_user_data(id, data):
    user = User.objects.filter(uid=id).reverse()[0]
    if user.state == 0:
        user.temperature = data
        user.state = 1
        user.save()
    elif user.state == 1:
        user.address = data
        user.state = 2
        user.save()
    else:
        print("update data error!!")

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
                if isinstance(event.message, TextMessage):
                    profile = line_bot_api.get_profile(event.source.user_id)
                    reply_text = ""

                    if "回報" in event.message.text:
                        print(profile.user_id+"要回報")
                        create_row_in_db(profile.user_id)
                        reply_text = "嗨，"+profile.display_name+"\n請問你現在的體溫?"

                    else:
                        state = -1
                        try:
                            state = User.objects.filter(uid=profile.user_id).reverse()[0].state
                            
                        except:
                            reply_text = "嗨，"+profile.display_name+"\n你要回報嗎?"

                        if state == 0:
                            print(profile.user_id+"輸入體溫")
                            update_user_data(profile.user_id, event.message.text)
                            reply_text = "請問你的所在地?"
                        elif state == 1:
                            print(profile.user_id+"輸入地點")
                            update_user_data(profile.user_id, event.message.text)
                            reply_text = "回報成功！"
                        elif state == 2:
                        	reply_text = "你要再次回報嗎?"

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
