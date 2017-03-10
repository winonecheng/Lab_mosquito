from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from .models import User

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
     

def upload_to_db(str):
	user = User(location=str)
	user.save()
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
                if isinstance(event.message, TextMessage):
                	profile = line_bot_api.get_profile(event.source.user_id)
                	reply_text = ""
                	if "回報" in event.message.text:
                		print(profile.user_id+"要回報")
                		reply_text = "嗨，"+profile.display_name+"\n請問你現在的體溫?"

	                if "體溫" in event.message.text:
	                	print(profile.user_id+"輸入體溫")
	                	reply_text = "請問你的所在地?"

	                if "地點" in event.message.text:
	                	print(profile.user_id+"輸入地點")
	                	reply_text = "回報成功！"

                	line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
