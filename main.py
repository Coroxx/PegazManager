import os
import sys
import time
import json
import random
import re


COLORS = {
    "black": "\u001b[30;1m",
    "red": "\u001b[31;1m",
    "green": "\u001b[32m",
    "lightgreen": "\u001b[38;5;82m",
    "lightyellow": "\u001b[38;5;226m",
    "yellow": "\u001b[33;1m",
    "blue": "\u001b[34;1m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "yellow-background": "\u001b[43m",
    "black-background": "\u001b[40m",
    "cyan-background": "\u001b[46;1m",
}
COLORLIST = ['red', 'green', 'lightgreen', 'lightyellow', 'yellow', 'yellow', 'blue', 'magenta', 'cyan',
             'white']


def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text


defaultcolor = random.choice(COLORLIST)


def pingcolor(text):
    ping = int(text)
    if ping <= 100:
        return colorText('[[green]] {} ms').format(text)
    elif ping >= 100 and ping <= 250:
        return colorText('[[yellow]] {} ms').format(text)
    else:
        return colorText('[[red]] {} ms').format(text)


def exit():
    print(colorText('[[red]]\n[-] Exiting...'))
    time.sleep(1)
    os.system('clear')
    sys.exit()


def hub():
    os.system('clear')
    print(colorText('[[' + defaultcolor + ']]________                          \n___  __ \___________ ______ ______\n__  /_/ /  _ \_  __ `/  __ `/__  /\n_  ____//  __/  /_/ // /_/ /__  /_\n/_/     \___/_\__, / \__,_/ _____/\n             /____/               \n\nAuthor : @Coroxx on GitHub\nVersion : 1.0\n'))
    try:
        with open('config.json', 'r') as info:
            info = json.load(info)
            info = info['data']
    except:
        time.sleep(1)
        regenerate = input(colorText(
            '[[red]]\n[!] The config.json file seems to have been deleted, do you want to regenerate it? (y/n) '))
        if bool(re.match(r"OUI|oui|y(?:es)?|Y", regenerate)):
            os.system('touch config.json')
            with open('config.json', 'w') as generate:
                t = {
                    "data": [

                    ]
                }
                json.dump(t, generate)
            hub()
        else:
            exit()
    if len(info) == 0:
        create = input(colorText('[[' + defaultcolor + ']]' +
                                 '[?] No SSH configuration is detected, do you want to configure a new one? y/n : '))
        if bool(re.match(r"OUI|oui|y(?:es)?|Y", create)):
            newconfig()
        else:
            exit()
    else:
        print(colorText('[[' + defaultcolor + ']][+] ' +
              str(len(info)) + ' configurations detected !'))


def newconfig():
    pass


if __name__ == "__main__":
    hub()
