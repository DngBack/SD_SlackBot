import slack
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

filepath = 'Image.jpg'

message_counts = {}


def pureimg(data1):
        data1 = '[{"text": "", "image_url": "'+data1+'"}]'
        data1 = [json.loads(data1[1:-1])]
        return data1


# @slack_event_adapter.on('message')
# def message(payload): 
#     event = payload.get('event', {})
#     channel_id = event.get('channel')
#     user_id = event.get('user')
#     text = event.get('text')

#     if BOT_ID != user_id:
#         client.chat_postMessage(channel= "#chatbottest" , text="Hello world!")


@app.route('/message-count', methods=['POST'])
def message_count():
    data = request.form 
    print(data)
    channel_id = data.get('channel_id')

    # client.chat_postMessage(channel=channel_id , text=text)

    # response = client.files_upload(channel=channel_id, file='Image1.jpg', timeout=10)
    # payoff = response['file']['permalink']

    # client.chat_postMessage(channel=channel_id, attachments=pureimg(payoff))
    client.chat_postMessage(channel=channel_id , text="There is an image.")


@app.route('/give_image', methods=['POST'])
def give_image():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id , text="I got an messsage.")
    message = "You want to create image about " + text
    client.chat_postMessage(channel=channel_id , text=message)

    image_url = "https://filmdaily.co/wp-content/uploads/2020/05/cat-memes-lede-1536x1052.jpg"
    attachments = [{"title": "Cat", "image_url": image_url}]
    client.api_call("chat.postMessage", text='postMessage test',
                attachments=attachments)

    # response = client.files_upload(channel=channel_id, file='Image1.jpg', timeout=5000)
    # payoff = response['file']['permalink']

    # client.chat_postMessage(channel=channel_id, attachments=pureimg(payoff))

    client.chat_postMessage(channel=channel_id , text="There is an image.")
    client.chat_postMessage(channel=channel_id , text="-------------------")
    return Response(), 200

if __name__ == '__main__': 
    app.run(debug=True)
