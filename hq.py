import discord
import webbrowser
from termcolor import colored
import datetime
import logging
import os
#import Google_Search
import time
from datetime import datetime
from pytz import timezone
from lomond import WebSocket
from unidecode import unidecode
import colorama
import requests
import json
import websocket
import re
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed
import aniso8601
from websocket import create_connection

webhook_url="https://discordapp.com/api/webhooks/735870760048001108/8mNnJmeOFnF_NUYY7s_zI7ZGSUjOVz8qoEAb7ZS-jBKgxVXQ15cbAc7Sj-hMK9OWeR04"

we="https://discordapp.com/api/webhooks/735870760048001108/8mNnJmeOFnF_NUYY7s_zI7ZGSUjOVz8qoEAb7ZS-jBKgxVXQ15cbAc7Sj-hMK9OWeR04"


try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")


try:
    hq = Webhook(we)
except:
    print("Invalid WebHook Url!")
    

def show_not_on():
    colorama.init()
    # Set up logging
    logging.basicConfig(filename="data.log", level=logging.INFO, filemode="w")

    # Read in bearer token and user ID
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            BEARER_TOKEN = settings[0].split("=")[1]
        except IndexError as e:
            logging.fatal(f"Settings read error: {settings}")
            raise e

    print("getting")
    main_url = f"https://api-quiz.hype.space/shows/now?type="
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "x-hq-client": "Android/1.3.0"}
    # "x-hq-stk": "MQ==",
    # "Connection": "Keep-Alive",
    # "User-Agent": "okhttp/3.8.0"}

    try:
        response_data = requests.get(main_url).json()
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)

    if "broadcast" not in response_data or response_data["broadcast"] is None:
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            print("Show not on.")
            tim = (response_data["nextShowTime"])
            tm = aniso8601.parse_datetime(tim)
            x =  tm.strftime("%H:%M")
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            x_in = x_ind.strftime("%H:%M:%S [%d/%m/%Y] ")
    
            prize = (response_data["nextShowPrize"])
            time.sleep(5)
            embed=Embed(title="<:emoji_20:696173211058044968> HQ Trivia",description=f"**__Stay Tuned Next For Next HQ Match__**<a:emoji_31:698185982935040041> \n**Next Game Show Prize <a:emoji_27:698185546845126737> <a:emoji_27:698185546845126737>{prize} <a:emoji_36:698187083117887616> **",color=0x00FFF6)
            embed.add_field(name=f"Next HQ Time In India🇮🇳",value="{}".format(x_in),inline=False)
            embed.set_image(url="https://cdn.discordapp.com/attachments/649457795875209265/672845602824126494/Nitro_2.gif")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/621954596402888724/699979122256117760/tenor.gif")
            embed.set_footer(text="",icon_url="https://cdn.discordapp.com/attachments/699654459264860291/714657857152221275/696173211058044968.png")
            hq.send(content="**Connected To HQ Socket|<:emoji_40:702495647990939729>**",embed=embed)   
            #hook.send(f"**Next Show Prize ---{NextShowPrize} **")



def show_active():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    return response_data['active']


def get_socket_url():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()

    socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "x-hq-client": "iPhone8,2"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)
            #hook.send(f"{message_data}")
           # print(message_data)

            if message_data['type'] == 'question':
                question = message_data['question']
                qcnt = message_data['questionNumber']
                Fullcnt = message_data['questionCount']

                print(f"\nQuestion number {qcnt} out of {Fullcnt}\n{question}")
                #hook.send(f"**\nQuestion number {qcnt} out of {Fullcnt}\n{question}**")
                #open_browser(question)
                answers = [unidecode(ans["text"]) for ans in message_data["answers"]]
                print(f"\n{answers[0]}\n{answers[1]}\n{answers[2]}\n")
                real_question = str(question).replace(" ","+")
                google_query = "https://google.com/search?q="+real_question
                real_answers = str(answers).replace(" ","+")
                google_q = "https://google.com/search?q="+real_answers
                #real_answers = str(answers).replace(" ","+")
               # google_q = "https://google.com/search?q="+real_answers
                #embed=discord.Embed(title=f"**\n{qcnt}. {question}**",description=f"**\nOption :one:\n{answers[0]}\n\nOption :two:\n{answers[1]}\n\nOption :three:\n{answers[2]}**",color=0xff5733)
                #hook.send(embed=embed)
                option1=f"{answers[0]}"
                option2=f"{answers[1]}"
                option3=f"{answers[2]}"
                r = requests.get("http://www.google.com/search?q=" + question) 
                soup = BeautifulSoup(r.text, 'html.parser')
                linkElements = soup.select('.r a') 
                linkToOpen = min(10, len(linkElements)) 
                for i in range(linkToOpen): 
                      webbrowser.open('https://www.google.com/'+linkElements[i].get('href')) 
                response = soup.find_all('a') 
                r = requests.get("http://www.google.com/search?q=" + question + option1 + option2 + option3) 
                soup = BeautifulSoup(r.text, 'html.parser') 
                linkElements = soup.select('.r a') 
                linkToOpen = min(10, len(linkElements)) 
                for i in range(linkToOpen): 
                      webbrowser.open('https://www.google.com/'+linkElements[i].get('href')) 
                response = soup.find_all('a') 
                res = str(r.text)
                
                countoption1 = res.count(option1)
                countoption2 = res.count(option2)
                countoption3 = res.count(option3)
                maxcount = max(countoption1, countoption2, countoption3)
                sumcount = countoption1+countoption2+countoption3
                print("/n")
                if countoption1 == maxcount:
                	print(f"A {answers[0]}")
                elif countoption2 == maxcount:
                	print(f"B {answers[1]}")
                else:
                	print(f"C {answers[2]}")              
                if countoption1 == maxcount:
                    embed2=discord.Embed(title=f"**<:emoji_24:696323975311261766> HQ Trivia Question {qcnt} out of {Fullcnt}**",description=f"**[{question}]({google_query})**\n**<a:emoji_66:715435468732497940> Google Search Results! 🔎:**\n\n**__Answer Choice ❶__**\n**[{answers[0]}]({google_q}): {countoption1}** <a:emoji_green:703812286107877456>\n\n**__Answer Choice ❷__**\n**[{answers[1]}]({google_q}): {countoption2}** \n\n**__Answer Choice ❸__**\n**[{answers[2]}]({google_q}): {countoption3}**")
                   # embed2.set_author(name = f"HQ Trivia Question {qcnt} out of {Fullcnt}")
                    embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/621954596402888724/704303796616167555/images_27.jpeg")
                    embed2.set_footer(text="",icon_url="https://cdn.discordapp.com/attachments/699654459264860291/714657857152221275/696173211058044968.png")
                    hook.send(embed=embed2)
                elif countoption2 == maxcount:
                    embed2=discord.Embed(title=f"**<:emoji_24:696323975311261766> HQ Trivia Question {qcnt} out of {Fullcnt}**",description=f"**[{question}]({google_query})**\n**<a:emoji_66:715435468732497940> Google Search Results! 🔎:**\n\n**__Answer Choice ❶__**\n**[{answers[0]}]({google_q}): {countoption1}** \n\n**__Answer Choice ❷__**\n**[{answers[1]}]({google_q}): {countoption2}** <a:emoji_green:703812286107877456>\n\n**__Answer Choice ❸__**\n**[{answers[2]}]({google_q}): {countoption3}**")
                    #embed2.set_author(name = f"HQ Trivia Question {qcnt} out of {Fullcnt}")
                    embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/621954596402888724/704303796616167555/images_27.jpeg")
                    embed2.set_footer(text="",icon_url="https://cdn.discordapp.com/attachments/699654459264860291/714657857152221275/696173211058044968.png")
                    hook.send(embed=embed2)
                else:
                    embed2=discord.Embed(title=f"**<:emoji_24:696323975311261766> HQ Trivia Question{qcnt} out of {Fullcnt}**",description=f"**[{question}]({google_query})**\n**<a:emoji_66:715435468732497940> Google Search Results! 🔎:**\n\n**__Answer Choice ❶__**\n**[{answers[0]}]({google_q}): {countoption1}** \n\n**__Answer Choice ❷__**\n**[{answers[1]}]({google_q}): {countoption2}** \n\n**__Answer Choice ❸__**\n**[{answers[2]}]({google_q}): {countoption3}** <a:emoji_green:703812286107877456>")
                  #  embed2.set_author(name = f"HQ Trivia Question {qcnt} out of {Fullcnt}")
                    embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/621954596402888724/704303796616167555/images_27.jpeg")
                    embed2.set_footer(text="",icon_url="https://cdn.discordapp.com/attachments/699654459264860291/714657857152221275/696173211058044968.png")
                    hook.send(embed=embed2)

            elif message_data["type"] == "questionSummary":

                answer_counts = {}
                correct = ""
                for answer in message_data["answerCounts"]:
                    ans_str = unidecode(answer["answer"])

                    if answer["correct"]:
                        correct = ans_str
                advancing = message_data['advancingPlayersCount']
                eliminated = message_data['eliminatedPlayersCount']
                #nextcheck = message_data['nextCheckpointIn']

                print(colored(correct, "blue"))
                print(advancing)
                print(eliminated)
                #hook.send(f"**Correct Answer -- {correct}**")
                #hook.send(f"**Advancing -- {advancing}      Eliminating --- {eliminated}**")
                embd=discord.Embed(title="**Answer Status:-** ",description=f"**{qcnt}: [{question}]({google_query})**\n**Correct Answer:- {correct}** <a:emoji_67:715533775802466437>")
                embd.add_field(name=f"**Advancing Players** ",value=f"**{advancing}**",inline=True)
                embd.add_field(name=f"**Eliminated  Players** ",value=f"**{eliminated}** ",inline=True)
                #embd.add_field(name=f"❓ **Next CheckPoint:** ",value=f"**{nextcheck}**", inline=True)
                #embd.set_thumbnail(url="https://is3-ssl.mzstatic.com/image/thumb/Purple113/v4/13/82/d5/1382d5b4-ecea-b99c-0622-e701fa5325ac/HQAppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/246x0w.png")
                embd.set_footer(text=f"",icon_url="https://cdn.discordapp.com/attachments/699654459264860291/714657857152221275/696173211058044968.png")
                hook.send(embed=embd)

            elif message_data["type"] == "gameSummary":
                 winn = message_data['numWinners']
                 prize = message_data["prize"])     
                 embed=discord.Embed(title=f"**__📌 Game Results! 📌__**", description=f"**Winners Announced By HQ Trivia <:emoji_24:696323975311261766>**",color=0xA4FF00)
                 embed.add_field(name="**__🎉 Winners 🎉__**", value=f"**🎊 {winn} 🎊**", inline=True)
                 embed.add_field(name="**__💰 Winnig Amount 💰__**", value=f"**🥳 {prizeMoney} 🥳**", inline=True)
                 embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/709231606430171196/715022507668799528/giphy.gif")
                 embed.set_footer(text=f"",icon_url="https://cdn.discordapp.com/attachments/699654459264860291/714657857152221275/696173211058044968.png")
                 hook.send(embed=embed)




"""
def open_browser(question):

    main_url = "https://www.google.co.in/search?q=" + question
    webbrowser.open_new(main_url)
"""

def get_auth_token():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            auth_token = settings[0].split("=")[1]
        except IndexError:
            print('No Key is given!')
            return 'NONE'

        return auth_token

while True:
    if show_active():
        url = get_socket_url()
        print('Connected to Socket : {}'.format(url))
        embed=Embed(title="**Hi 👋,Guyss I'm HQ WebSocket <:emoji_20:696173211058044968>**",description="**Now I'm Ready To Run 😋**",color=0x004EFF)
        hook.send(content="**Connected To HQ Socket|<:emoji_40:702495647990939729>**",embed=embed)
    

        token = get_auth_token()
        if token == 'NONE':
            print('Please enter a valid auth token.')
        else:
            connect_websocket(url, token)

    else:
        show_not_on()
        time.sleep(3600)
