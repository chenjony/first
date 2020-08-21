from flask import Flask, request, abort, Response

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import logging



app = Flask(__name__)

CHANNELID = '1654823183'
ACCESS_TOKEN = 'XPOfZbJNhoj9zPIl9r1Cg4Dn8th5tVUAPy1VY0Jr67oEH9ZnJV80nw+3aKQEj7XIgaHTLI9OF9gDwojxVAmVRTES2/uOsG86q8q06JvJ7d8i97jUlVS5z0r76YCPDruJuBofxf63Mnuhfz88IDBLowdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '037b81dd90bf03f43eaf4fbd06d8f5c6'


line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)



@app.route("/", methods=['GET','POST'])
def _test():
    print(request.data)
    return Response('ok')



@app.route("/callback", methods=['GET', 'POST'])
def callback():
    if request.method=='POST':
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)
        app.logger.info("Request: " + body)

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    return_msg = "We got msg: %s from user id: %s" % (event.message.text, event.source.user_id)
    app.logger.info("Response:" + return_msg)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(return_msg)
    )

if __name__ == "__main__":
    app.debug = True
    log_handler = logging.FileHandler('testserver.log')
    app.logger.addHandler(log_handler)
    app.run(host='127.0.0.1', port=8080)