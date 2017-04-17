from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage, FollowEvent, UnfollowEvent, TemplateSendMessage, PostbackEvent
from linebot.models.template import ConfirmTemplate, PostbackTemplateAction, ButtonsTemplate, MessageTemplateAction, URITemplateAction

from .models import User
import re, json, requests
from .dengue_data import data

INITIAL = 0
INFO_DISEASE = 1
INFO_ZAPPER = 2
REPROT = 3
SETTING = 4

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

     
def create_user(id):
    user = User(uid=id, report_date=timezone.now())
    user.save()

def remove_user(id):
    user = User.objects.get(uid=id)
    user.delete()

def update_user_state(id, state):
    user = User.objects.get(uid=id)
    user.state = state
    user.save()

def update_user_address(id, address, lat, lng):
    user = User.objects.get(uid=id)
    user.address = address
    user.latitude = lat
    user.longitude = lng
    user.save()

def update_user_temperature(id,temp):
    user = User.objects.get(uid=id)
    user.temperature = temp
    user.save()

def handle_input_of_temperature(id, message):
    pat = r'^\s*(\d+\.*\d*)\s*'
    str = message
    match = re.search(pat,str)
    if match:
        update_user_temperature(id, float(match.group(1)))
        return 1
    else:
        return 0

def address_to_lat_lng(address):
    key= "AIzaSyA1ug3pDy-rR6btRx88y-K9znjzRTUeHIE"
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}&language=zh-TW".format(address, key)
    response = requests.get(url)
    response_json = response.json()
    if response_json['status'] == "OK":
        return response_json['results'][0]
    else:
        return -1

confirm_address = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text='',
        actions=[
            PostbackTemplateAction(
                label='確認',
                data='confirm_address_true'
            ),
            PostbackTemplateAction(
                label='取消',
                data='confirm_address_false'
            )
        ]
    )
)

confirm_address_type = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text='你要用何種方式?',
        actions=[
            PostbackTemplateAction(
                label='「位置訊息」',
                data='function'
            ),
            PostbackTemplateAction(
                label='文字輸入',
                data='text'
            )
        ]
    )
)

button_setting = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='個人資料設定',
        text='選擇要更改的資料',
        actions=[
            PostbackTemplateAction(
                label='地址',
                data='address'
            ),
            PostbackTemplateAction(
                label='????',
                data='temp'
            ),
        ]
    )
)

@handler.add(MessageEvent, message=TextMessage)
def handle_text_msg(event):
    print(event.message.text)
    profile = line_bot_api.get_profile(event.source.user_id)
    state = User.objects.get(uid=profile.user_id).state

    if state == INITIAL:
        if event.message.text == str(INFO_DISEASE):
            pass
        elif event.message.text == str(INFO_ZAPPER):
            pass
        elif event.message.text == str(REPROT):
            update_user_state(profile.user_id, REPROT)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請問你現在的體溫？\n(ex：27.5度)")
            )
        elif event.message.text == str(SETTING):
            update_user_state(profile.user_id, SETTING)
            line_bot_api.reply_message(
                event.reply_token,
                button_setting
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=profile.display_name+"你好!\n我是台南市的疫情機器人，我提供以下功能：\n\n1 : 即時疫情\n2 : 目前捕蚊燈資訊\n3 : 回報疫情\n4 : 個人資料設定\n\n請輸入對應數字做操作喔！")
            )

    elif state == SETTING:
        confirm_address.alt_text = event.message.text
        confirm_address.template.text = '新地址 : '+event.message.text
        line_bot_api.reply_message(
            event.reply_token,
            confirm_address
        )

        '''
        format_address = address_to_lat_lng(event.message.text)
        if format_address != -1:
            update_user_address(profile.user_id, format_address['formatted_address'], format_address['geometry']['location']['lat'], format_address['geometry']['location']['lng'])
            update_user_state(profile.user_id, INITIAL)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="成功!")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="錯誤!請再次輸入地址!")
            )
        '''

    elif state == REPROT:
        if handle_input_of_temperature(profile.user_id, event.message.text):
            update_user_state(profile.user_id, INITIAL)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="回報成功!")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請問你現在的體溫？\n(ex：27.5度)")
            )
    else:
        pass

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_msg(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    state = User.objects.get(uid=profile.user_id).state
    if state == SETTING:
        confirm_address.alt_text = event.message.address
        confirm_address.template.text = '新地址 : '+ event.message.address
        line_bot_api.reply_message(
            event.reply_token,
            confirm_address
        )

        '''
        update_user_address(profile.user_id, event.message.address, event.message.latitude, event.message.longitude)
        update_user_state(profile.user_id, INITIAL)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="成功!")
        )
        '''

@handler.add(PostbackEvent)
def handle_postback_event(event):
    if event.postback.data == "function":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請使用line「位置訊息」功能，公開你的所在位置")
        )
    elif event.postback.data == "text":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請直接輸入地址")
        )
    elif event.postback.data == "address":
        line_bot_api.reply_message(
            event.reply_token,
            confirm_address_type
        )
    elif event.postback.data == "confirm_address_true":
        format_address = address_to_lat_lng(confirm_address.alt_text)
        print(confirm_address.alt_text)
        if format_address != -1:
            update_user_address(event.source.user_id, format_address['formatted_address'], format_address['geometry']['location']['lat'], format_address['geometry']['location']['lng'])
            update_user_state(event.source.user_id, INITIAL)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="成功!")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="錯誤!請再次輸入地址!")
            )

    elif event.postback.data == "confirm_address_false":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="取消設定")
            )
            update_user_state(event.source.user_id, INITIAL)
    else:
        pass


@handler.add(FollowEvent)
def handle_follow_event(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    create_user(profile.user_id)
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=profile.display_name+"你好! \xF0\x9F\x98\x81 \n我是台南市的疫情機器人，我提供以下功能：\n\n1 : 即時疫情\n2 : 目前捕蚊燈資訊\n3 : 個人資料設定\n\n請輸入對應數字做操作喔！(ok)")
    )
    '''
    print(profile.user_id+"\tfollow the bot.")


@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    remove_user(event.source.user_id)
    print(event.source.user_id+"\tunfollow the bot.\n")


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse()

    else:
        return HttpResponseBadRequest()


def map(request):
    json_addressPoints1 = json.dumps(data(1),ensure_ascii=False)
    json_addressPoints2 = json.dumps(data(2),ensure_ascii=False)
    json_addressPoints3 = json.dumps(data(3),ensure_ascii=False)
    return render(request, 'mosquito/map.html',{'addressPoints1':json_addressPoints1, 'addressPoints2':json_addressPoints2, 'addressPoints3':json_addressPoints3})

