import json
import openai
from sqlconnect import create_db_connection, execute_query, read_query

# for openAI API authentication
with open('GPT_SECRET_KEY.json') as f:
    data = json.load(f)
openai.api_key = data["API_KEY"]

chat_log = "This is a bot named VAI_BOT. Type in plain english, it will be converted to MySQL query and executed......\n"

restart_sequence = "Human: Write a SQL Query to "
start_sequence = "VAI_BOT:"


def ask(question, chat_log):
    prompt_text = f"{chat_log}{restart_sequence}: {question}{start_sequence}:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = "What do you want to do? Type in plain english, it will be converted to SQL query and executed..\n"
    return f"{chat_log}{restart_sequence} {question}{start_sequence}{answer}"
