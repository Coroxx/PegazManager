import os
import sys
import time
import json
import random
import re
import socketserver
import socket
import paramiko


# Pegaz, an intelligent SSH Session Manager
# Entirely coded by @coroxx on github


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

try:
    from pythonping import ping
except:
    os.system("clear")
    print(
        colorText(
            "[[red]]You didn't do the installation correctly, let me do it for you..."
        )
    )
    time.sleep(2)

    try:
        os.system("pip install -r requirements.txt")
        os.system("clear")
        print(colorText("[[green]]Succes !"))
        time.sleep(2)
    except:
        os.system("clear")
        time.sleep(1)
        print(
            colorText(
                "[[red]]Uh, an error has occurred, please report the problem on github."
            )
        )


def pingcolor(text):
    ping = int(text)
    if ping <= 100:
        return colorText('[[green]]{} ms').format(text)
    elif ping >= 100 and ping <= 250:
        return colorText('[[yellow]]{} ms').format(text)
    else:
        return colorText('[[red]]{} ms').format(text)


def exit():
    print(colorText('[[red]]\n[-] Exiting...'))
    time.sleep(1)
    os.system('clear')
    sys.exit()


def hub():
    global info
    os.system('clear')
    print(colorText('[[' + defaultcolor + ']]________                          \n___  __ \___________ ______ ______\n__  /_/ /  _ \_  __ `/  __ `/__  /\n_  ____//  __/  /_/ // /_/ /__  /_\n/_/     \___/_\__, / \__,_/ _____/\n             /____/               \n\nAuthor : @Coroxx on GitHub\nVersion : 1.0\n'))
    try:
        with open('config.json', 'r') as info:
            info = json.load(info)
    except:
        time.sleep(1)
        regenerate = input(colorText(
            '[[red]]\n[!] The config.json file seems to have been deleted, do you want to regenerate it? (y/n) '))
        if bool(re.match(r"OUI|oui|y(?:es)?|Y", regenerate)):
            os.system('touch config.json')
            with open('config.json', 'w') as generate:
                t = {
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
    menu(len(info), info)


def config():
    pass


def menu(number, data):
    print('\n')
    for i in range(number):
        l = i + 1
        try:
            response_list = ping(data[f'{l}']['ip'], size=40, count=5)
            Online = 'Online'
        except:
            Online = 'Offline'
        if Online == "Online":
            print(
                colorText('[[' + defaultcolor + ']][' + str(i+1) + '] Fast connect to ' + data[f'{l}']['ip'] + ' [[green]](Online : ' + pingcolor(round(response_list.rtt_avg_ms)) + '[[green]])[[' + defaultcolor + ']]'))
        else:
            print(
                colorText('[[' + defaultcolor + ']][' + str(i+1) + '] Fast connect to ' + data[f'{l}']['ip'] + ' [[red]](Offline)' + '[[' + defaultcolor + ']]'))

    print(colorText('[[' + defaultcolor + ']]\n[99] Edit configurations'))
    choice = input(colorText('[[' + defaultcolor + ']]' + '\n[?] Choice : '))
    try:
        choice = int(choice)
    except ValueError:
        print(colorText('[[red]]\n[!] Invalid choice !'))
        menu(len(info), info)
    if choice == 99:
        config()
    elif choice > number:
        print(colorText('[[red]]\n[!] Invalid choice !'))
        menu(len(info), info)
    elif choice < number:
        os.system('clear')
        print(colorText('[[green]][+] Currently connecting to your server...'))
        time.sleep(2)
        os.system('clear')
        os.system(
            'ssh -i ' + data[f'{choice}']['path'] + ' ' + data[f'{choice}']['username'] + "@" + data[f'{choice}']['ip'])


def isvalidpath(path):
    if os.path.exists(path):
        return True
    else:
        return False


def newconfig():
    ip = input(colorText('[[' + defaultcolor + ']]' + '\nServer IP : '))
    if bool(re.match(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', ip)):
        pass
    else:
        print(colorText('[[red]][!] Incorrect syntax !\n'))
        newconfig()
    port = input(colorText('[[' + defaultcolor + ']]' +
                           '\nPort (Enter for default 22) : '))
    if port == '':
        port = '22'
    else:
        try:
            int(port)
        except ValueError:
            print(colorText('[[red]][!] Incorrect syntax !\n'))
            newconfig()
        pass
    keyquestion = input(colorText('[[' + defaultcolor + ']]' +
                                  '\n----------------------------\nFirst of all, do you have a ssh key ? Y/N : '))
    if bool(re.match(r"OUI|oui|y(?:es)?|Y", keyquestion)):
        key = True
    else:
        key = False

    if key:
        path = input(colorText('[[' + defaultcolor + ']]' + '\nPath : '))

        if isvalidpath(path):
            print(colorText('[[green]][+] File detected !\n'))
        else:
            incorrect = True
            while incorrect:
                print(
                    colorText('[[red]][-] Invalid path / Invalid location, try again'))
                path = input(
                    colorText('[[' + defaultcolor + ']]' + '\nPath : '))
                if isvalidpath(path):
                    break
                else:
                    continue
    print(colorText('[[' + defaultcolor + ']]' + '\n--Credentials--\n'))
    username = input(
        colorText('[[' + defaultcolor + ']]' + 'Username (Press enter for root) : '))
    if username == '':
        username = 'root'
    if not key:
        password = input(
            colorText('[[' + defaultcolor + ']]' + 'Password : '))
        time.sleep(1)
    print(colorText('[[' + 'green' + ']]' +
                    '[+] Testing your credentials...'))
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key:
            ssh.connect(ip, port=port, username=username,
                        key_filename=path)
            password = False
        else:
            ssh.connect(ip, port=port, username=username,
                        password=password)
        time.sleep(1)
        print(colorText('[[green]]\n[+] Succes !'))
    except:
        print(colorText('[[' + 'red' + ']]' +
              '\n[-] Incorrect credentials, try again...'))
        if key:
            verbose = input(colorText(
                '[[' + defaultcolor + ']]\nDo you want to make a verbose try ? Y/N : '))
            if bool(re.match(r"OUI|oui|y(?:es)?|Y", verbose)):
                os.system('ssh -vvv -i' + path + ' ' + username + '@' + ip)
        time.sleep(1)
        newconfig()
    with open('config.json', 'r') as f:
        data = json.loads(f.read())
        if key:
            data[len(info)+1] = {
                "type": "key",
                "ip": ip,
                "port": port,
                "username": username,
                "path": path,
            }
        else:
            data[len(info)+1] = {
                "type": "password",
                "ip": ip,
                "port": port,
                "username": username,
                "password": password
            }
        with open("config.json", 'w') as f:
            f.write(json.dumps(data,
                    indent=4, separators=(',', ': ')))
    sys.exit()


if __name__ == "__main__":
    hub()
