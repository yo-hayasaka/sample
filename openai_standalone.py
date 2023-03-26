import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# system_message = "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
# input_message = "Hello"
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-0301",
#     messages=[
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": input_message}
#         ]
# )
# text = response["choices"][0]["message"]["content"]
# print(text)

# messages = [{"role": "system", "content": "制約条件：あなたは関西出身のAIです。関西弁で応答します。"}]
messages = []
while True:
    # text =  input("User: ")
    prompt = "Hello"
    messages.append ({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.0,
    )
    content = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": content})
    print("---\n Assistant: " + content + "\n---")
    if prompt == "quit" or prompt == "exit":
        break
