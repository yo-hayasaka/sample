import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import openai

load_dotenv()
app = App(token=os.environ["SLACK_BOT_TOKEN"])
openai.api_key = os.environ["OPENAI_API_KEY"]
chatbot_id = os.environ["CHATBOT_ID"]

# メンションされたら動作
@app.event("app_mention")
def chatgpt_reply(event, say):
    input_message = event["text"]
    thread_ts = event.get("thread_ts") or None
    channel = event["channel"]
    input_message = input_message.replace(chatbot_id, "") # ChatbotのアカウントIDの＠を削除, hogehogeをアプリのIDに変換
    print("prompt: " + input_message)
    system_message = "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_message}
            ]
    )
    text = response["choices"][0]["message"]["content"]
    print("ChatGPT: " + text)
    if thread_ts is not None:
        parent_thread_ts = event["thread_ts"]
        say(text=text, thread_ts=parent_thread_ts, channel=channel)
    # else:
    #     say(text=text, channel=channel) 
    else: # スレッドじゃないときもスレッドに返すときはこれ
        response = app.client.conversations_replies(channel=channel, ts=event["ts"])
        thread_ts = response["messages"][0]["ts"]
        say(text=text, thread_ts=thread_ts, channel=channel)

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()