import logging
from sys import stdout

from requests.api import get
import telegram
import requests
from telegram.ext import Updater, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from bs4 import BeautifulSoup

updater = Updater(token='1929229077:AAHRgq6DpnEdLnFi33MBP6d3a1--5owpwqw', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ohayo! I'm a Academic explanatory dictionary bot, enter /help to see all commands")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def find_pattern(soup):
    if soup.find(class_="znach") == None:
        return 1
    else:
        return 0

def get_explanation(word):
    response = requests.get("http://sum.in.ua/?swrd="+ word.lower())
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(word, "and it's len", len(word))
    if find_pattern(soup) == 1:
        result = soup.find(itemprop="articleBody").p.get_text()
    else:
        print(soup.find(class_="znach").find(class_="mark").next_sibling)
        result = soup.find(class_="znach").find(class_="mark").next_sibling
    result = "<b>" + word.upper() + "</b>" + result[result.find(","):]
    # print(result)
    return result

def explain(update, context):
    command = ' '.join(context.args)
    # print(soup.find(class_="znach").find(class_="mark").get_text())
    # print(soup.find(class_="znach").find(class_="mark").next_sibling)
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_explanation(command), parse_mode=telegram.ParseMode.HTML)

explain_handler = CommandHandler('explain', explain)
dispatcher.add_handler(explain_handler)

def inline_explain(update, context):
    query = update.inline_query.query
    if not query:
        return
    print("query:", query)
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.lower(),
            title='Explain',
            description='Ukrainian meaning of this word',
            input_message_content=InputTextMessageContent(get_explanation(query), parse_mode=telegram.ParseMode.HTML)
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

inline_explain_handler = InlineQueryHandler(inline_explain)
dispatcher.add_handler(inline_explain_handler)

updater.start_polling()