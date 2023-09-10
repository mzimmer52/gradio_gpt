import gradio as gr
import random
import time
import openai
import config

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def create_messages(history):
        lst = sum((history), [])
        print(lst)
        final = []
        for i in range(len(lst)):
            if i % 2 == 0:
                final.append({"role": "user", "content": lst[i]})
            else:
                final.append({"role": "assistant", "content": lst[i]})
        return final[:-1]


    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):

        print(history)
        print(create_messages(history))
        
        result = openai.ChatCompletion.create(model = 'gpt-3.5-turbo',
                                       api_key = config.key,
                                       messages = create_messages(history))
        result = result['choices'][0]['message']['content']

        history[-1][1] = ""
        for character in result:
            history[-1][1] += character
            time.sleep(0.00001)
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)
    
demo.queue()
demo.launch()