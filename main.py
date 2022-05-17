import os
import time

from requests import get, post
from lxml import html
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Back, Style

UI = """

      ____ _   _________  ____________  _______
     / __ \ | / / __/ _ \/_  __/  _/  |/  / __/
    / /_/ / |/ / _// , _/ / / _/ // /|_/ / _/  
    \____/|___/___/_/|_| /_/ /___/_/  /_/___/ 
                                  
    Type Option                                        
    [1] Thia clip
    [2] Asian sex
    [3] Japanese
    [4] Exit
                                           \n"""

os.system("title PornHook : By Timmy")
os.system("cls")
webhookurl = input("\n[>]Webhook Link: ")
os.system("cls")
time.sleep(1)

print(UI)
menu=input("[!]Choose a option: ")
if menu=="1": 
    weblink = "คลิปไทย"
    
elif menu=="2":
    weblink = "asiansexdiary"
    
elif menu=="3":
    weblink = "japanese-av"

elif menu =="4":
    os.system("cls")
    exit(0)

collection = list()
webhook_url = f"{webhookurl}"
source = html.fromstring(get(f"https://kingofhup.com/หมวดหมู่/{weblink}").content)
max = int(source.xpath("//a[@class='page-link']/text()")[-2])
export = weblink

def fetch(page: int):
    doc = html.fromstring(
        get(f"https://kingofhup.com/หมวดหมู่/{weblink}?page={page}").content
    )
    print(f"[{Fore.GREEN}Success{Fore.RESET}] {Fore.YELLOW}fetched video from page {page} {Fore.RESET}")
    image = doc.xpath("//div[@class='card p-1']/v-lazy-image/@src")
    title = doc.xpath("//div[@class='card p-1']/v-lazy-image/@title")
    url = [
        "https://kingofhup.com" + path
        for path in doc.xpath("//div[@class='position-relative']/a/@href")
    ]
    print(f"[{Fore.GREEN}Success{Fore.RESET}] {Fore.YELLOW}fetched {len(url)} videos from page {page} {Fore.RESET}")
    for title, image, url in zip(title, image, url):
        path = html.fromstring(get(url, timeout=25).content)
        video = path.xpath("//div[@class='col-12']/iframe/@src")
        if video != []:
            video = str(video[0])
            print(f"[{Fore.GREEN}Success{Fore.RESET}] {Fore.YELLOW}fetched video {video} from page {page} {Fore.RESET}")
            collection.append([video, title, image])

with ThreadPoolExecutor(max_workers=max) as executor:
    for number in range(max):
        executor.submit(fetch, number + 1)
executor.shutdown(wait=True)
for item in collection:
    status = post(
        webhook_url,
        json={
            "content": None,
            "username": "CAT MEOW#1916",
            "avatar_url": "https://files.catbox.moe/iv4jzq.jpg",
            "embeds": [
                {
                    "author": {
                        "name": item[1],
                        "url": "https://kingofhup.com",
                        "icon_url": "https://files.catbox.moe/iv4jzq.jpg",
                    },
                    "description": "[ [ดูคลิปเต็ม](" + item[0] + ") ]",
                    "colour": "16699392",
                    "image": {"url": item[2]},
                    "footer": {
                        "text": "CAT MEOW#1916",
                    },
                }
            ],
        },
    ).status_code
    print(f"[{Fore.GREEN}Upload{Fore.GREEN}] {Fore.YELLOW}{item[0]}{Fore.RESET} : [{status}]")
    sleep(1.75)