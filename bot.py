import os
import openai
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

start_sequence = "\nVAI_BOT:"
restart_sequence = "\nHuman: "
session_prompt = "The following is a conversation with an AI assistant VAI_BOT. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nVAI_BOT: I am an AI created by OpenAI. How can I help you today?\n"


def ask(question, chat_log=None):
    prompt_text = f"{chat_log}{restart_sequence}: {question}{start_sequence}:" #this is a python f string
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n"]
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None: chat_log = session_prompt 
    return f"{chat_log}{restart_sequence} {question}{start_sequence}{answer}"