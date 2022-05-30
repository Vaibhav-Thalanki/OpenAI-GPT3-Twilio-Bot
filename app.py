from unittest import result
from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from gpt import ask, append_interaction_to_chat_log
from sqlconnect import create_db_connection, execute_query, read_query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret2!'


@app.route('/vaibotsql', methods=['POST'])
def bot():
    connection = create_db_connection("localhost", "root", "", "PURPLESLATE")
    normal_english_query = request.values['Body']
    chat_log = session.get('chat_log')
    sql_query = ask(normal_english_query, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(
        normal_english_query, sql_query, chat_log)
    msg = MessagingResponse()
    if("select" in sql_query.lower()):
        result = read_query(connection, sql_query)
        print(str(result))
        msg.message(str(result))
    else:
        execute_query(connection, sql_query)
        msg.message(sql_query)
    return str(msg)


if __name__ == '__main__':
    app.run(debug=True)
