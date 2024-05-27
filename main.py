import openai
import os
from dotenv import find_dotenv, load_dotenv
import gradio as gr

load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo"

# def CallChatGPT(question):
#     response=client.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": question}],
#         max_tokens=500
#     )
#     return response['choices'][0]['message']['content'].strip()

def chatbot(message, history):
        history_openai_format = []
        for human, assistant in history:
                history_openai_format.append({"role": "user", "content": human})
                history_openai_format.append({"role": "assistant", "content": assistant})
        history_openai_format.append({"role": "user", "content": message})

        response = openai.chat.completions.create(
            model=model,
            # messages=[
            #     {"role": "user", "content": input_text}
            # ],
            messages=history_openai_format,
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stream=True
        )
        # print(response.choices[0].message.content)
        partial_message = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message = partial_message + chunk.choices[0].delta.content
                yield partial_message
        # return response.choices[0].message.content


# q = input('Ask question to AI Bot: ')    
# answer = chatbot(q)
# print(answer)

# gui=gr.Interface(
#     fn=chatbot,
#     inputs='text',
#     outputs='text',
#     title='chatbot',
#     description='ask me anything'
#     )
                 
# gui.launch()
gr.ChatInterface(chatbot).launch()

