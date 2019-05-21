import requests
from bs4 import BeautifulSoup
import os

import telegram

def testSent():
    bot.sendMessage(chat_id=chat_id, text='아직 새 글이 없어요')

mytoken = '123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ'

bot = telegram.Bot(token = mytoken)
chat_id = bot.getUpdates()[-1].message.chat.id

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

targetUser = ""
url = 'https://gallog.dcinside.com/'+targetUser+'/posting'

req = requests.get(url)
req.encoding = 'utf-8'

try:
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    post = soup.find("div", "cont_box").find("li")

    latest = post.find("a").text[1:]
    link = post.find("a").get("href")

except Exception as ex:
    bot.sendMessage(chat_id=chat_id, text='Error Occured!' + ex)

with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+', encoding="UTF-8") as f_read:
    before = f_read.readline()
    try:
        if before != latest:
            bot.sendMessage(chat_id=chat_id, text='새 글이 올라왔어요!: '+latest+"\nLink: "+link)
    except Exception as ex:
        bot.sendMessage(chat_id=chat_id, text='Error Occured!' + ex)
   
with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+', encoding="UTF-8") as f_write:
    f_write.write(latest)
    f_write.close()

