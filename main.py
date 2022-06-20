from flask import Flask, request, abort
import requests,json
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('')
handler = WebhookHandler('')


def getitem():
    res = requests.get(url="https://fortnite-api.com/shop/br", headers={"x-api-key": '45545e3b-0a80-426b-9105-d1babcbacfc6'}, params={"language": 'ja'})
    data = json.loads(res.text)
    Result = {"featured": [], "daily": [], "special": []}
    if len(data['data']['featured']) > 1:
        for card in data['data']['featured']:
            if card['isSpecial']:
                Result['special'].append(card)
            else:
                Result['featured'].append(card)
    if len(data['data']['daily']) > 1:
        for card in data['data']['daily']:
            if card['isSpecial']:
                Result['special'].append(card)
            else:
                Result['daily'].append(card)

    finaltext = ''
    for i in Result['featured']:
        finaltext += str(i['items'][0]['name']) + ' ' + '値段:' + str(i['finalPrice']) + 'Vbucks' + '\n'
    for i in Result['daily']:
        finaltext += str(i['items'][0]['name']) + ' ' + '値段:' + str(i['finalPrice']) + 'Vbucks' + '\n'
    for i in Result['special']:
        finaltext += str(i['items'][0]['name']) + ' ' + '値段:' + str(i['finalPrice']) + 'Vbucks' + '\n'
    return finaltext


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'アイテムショップ':
        sendtxt = getitem()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(sendtxt)))


if __name__ == "__main__":
    app.run()
