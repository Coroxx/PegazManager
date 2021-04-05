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
COLORLIST = ['red', 'green', 'lightgreen', 'lightyellow', 'yellow', 'blue', 'cyan',
             'white']


def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text


defaultcolor = random.choice(COLORLIST)

try:
    from pythonping import ping
    import replit
except ModuleNotFoundError:
    replit.clear()
    print(
        colorText(
            "[[red]]You didn't do the installation correctly, let me do it for you..."
        )
    )
    time.sleep(2)

    try:
        os.system("pip install -r requirements.txt")
        replit.clear()
        print(colorText("[[green]]Succes !"))
        time.sleep(2)
    except:
        replit.clear()
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


def close():
    print(colorText('[[red]]\n[-] Exiting...'))
    time.sleep(1)
    replit.clear()
    sys.exit()


def hub():
    global info
    replit.clear()
    print(colorText('[[' + defaultcolor + ']]________                          \n___  __ \___________ ______ ______\n__  /_/ /  _ \_  __ `/  __ `/__  /\n_  ____//  __/  /_/ // /_/ /__  /_\n/_/     \___/_\__, / \__,_/ _____/\n             /____/               \n\nAuthor : @Coroxx on GitHub\nVersion : 1.0\n'))
    try:
        with open('config.json', 'r') as info:
            info = json.load(info)
    except:
        time.sleep(1)
        regenerate = input(colorText(
            '[[red]]\n[!] The config.json file seems to have been deleted, do you want to regenerate it? (y/n) '))
        if bool(re.match(r"OUI|oui|y(?:es)?|Y", regenerate)):
            with open('config.json', 'w') as generate:
                t = {
                }
                json.dump(t, generate)
            hub()
        else:
            close()
    if len(info) == 0:
        create = input(colorText('[[' + defaultcolor + ']]' +
                                 '[?] No SSH configuration is detected, do you want to configure a new one? y/n : '))
        if bool(re.match(r"OUI|oui|y(?:es)?|Y", create)):
            newconfig()
        else:
            close()
    else:
        for infos in info.items():
            good = checkconfig(infos[1])
            if not good:
                brokenconfig(infos[0], infos[1], info)
        print(colorText('[[' + defaultcolor + ']][+] ' +
              str(len(info)) + ' configurations detected !'))
        if os.geteuid() == 0:
            pass
        else:
            print(colorText(
                '[[red]][-] You didn\'t launch this script with root privileges , some features like ping are not avalaibles (sudo python3 main.py)'))
    menu(len(info), info)


def checkconfig(config):
    l = ['password', 'path', 'ip', 'username', 'port']
    result = []
    for element in l:
        try:
            config[f'{element}']
            element = True
            result.append(element)
        except KeyError:
            element = False
            result.append(element)

    if not result[0] and not result[1]:
        return False
    elif not result[2] or not result[3] or not result[4]:
        return False
    return True


def brokenconfig(num, data, globaldata):
    replit.clear()
    print(colorText('[[' + defaultcolor + ']]________                          \n___  __ \___________ ______ ______\n__  /_/ /  _ \_  __ `/  __ `/__  /\n_  ____//  __/  /_/ // /_/ /__  /_\n/_/     \___/_\__, / \__,_/ _____/\n             /____/               \n\nAuthor : @Coroxx on GitHub\nVersion : 1.0\n'))
    try:
        ip = data['ip']
    except KeyError:
        ip = 'MISSING'
    print(colorText(
        '[[' + 'red' + ']]\n[!] Uhh, a configuration seems broken, n°' + num + '\nIP : ' + ip))
    choice = input(colorText(
        '[[' + defaultcolor + ']]\n[1] Reconfigure it\n[2] Delete it\n\n[3] Exit\n\n[?] Choice : '))
    try:
        choice = int(choice)
    except ValueError:
        print(colorText('[[red]]\n[!] Invalid choice !'))
        time.sleep(1)
        brokenconfig(num, data, globaldata)
    if choice >= 4:
        print(colorText('[[red]]\n[!] Invalid choice !'))
        time.sleep(1)
        brokenconfig(num, data, globaldata)
    elif choice == 1:
        del globaldata[f'{num}']
        with open('config.json', 'w') as f:
            json.dump(globaldata, f, indent=4)
        newconfig()
        hub()
    elif choice == 2:
        del globaldata[f'{num}']
        num = 1
        for element in data:
            element = num
            num += 1
        with open('config.json', 'w') as f:
            json.dump(globaldata, f, indent=4)
    elif choice == 3:
        close()
    else:
        print(colorText('[[red]]\n[!] Invalid choice !'))
        time.sleep(1)
        brokenconfig(num, data, globaldata)


def configmenu(data):
    replit.clear()
    print(colorText('[[' + defaultcolor + ']]________                          \n___  __ \___________ ______ ______\n__  /_/ /  _ \_  __ `/  __ `/__  /\n_  ____//  __/  /_/ // /_/ /__  /_\n/_/     \___/_\__, / \__,_/ _____/\n             /____/               \n\nAuthor : @Coroxx on GitHub\nVersion : 1.0\n'))
    choice = input(colorText(
        '[[' + defaultcolor + ']]\n[1] Add a new configuration\n[2] Modify a configuration\n[3] Delete a configuration\n\n[0] Back\n\n[?] Choice : '))
    if choice == '0':
        menu(len(info), info)
    elif choice == '1':
        newconfig()
    elif choice == '2':
        configmodify(data)
    elif choice == '3':
        configdelete(data)
    else:
        print(colorText('[[red]]\n[!] Incorrect choice !'))
        time.sleep(1)
        configmenu(data)


def configdelete(data):
    replit.clear()
    print(
        colorText('[[' + defaultcolor + ']]Which configuration ?\n'))
    for i in range(len(info)):
        l = i + 1
        print(
            colorText('[[' + defaultcolor + ']][' + str(i+1) + '] Configuration : ' + data[f'{l}']['username'] + '@' + data[f'{l}']['ip']))
    choice = input(colorText('[[' + defaultcolor + ']]\n\n[?] Choice : '))
    try:
        choice = int(choice)
    except ValueError:
        print(colorText('[[red]]\n[!] Incorrect choice !'))
        time.sleep(1)
        configmodify(data)
    if choice > len(info):
        print(colorText('[[red]]\n[!] Incorrect choice !'))
        time.sleep(1)
        configdelete(data)
    with open('config.json', 'w') as f:
        del data[f'{choice}']
        json.dump(data, f, indent=4)
    hub()


def configmodify(data):
    replit.clear()
    print(
        colorText('[[' + defaultcolor + ']]Which configuration ?\n'))
    for i in range(len(info)):
        l = i + 1
        print(
            colorText('[[' + defaultcolor + ']][' + str(i+1) + '] Configuration : ' + data[f'{l}']['username'] + '@' + data[f'{l}']['ip']))
    choice = input(colorText('[[' + defaultcolor + ']]\n\n[?] Choice : '))
    try:
        configchoice = int(choice)
    except ValueError:
        print(colorText('[[red]]\n[!] Incorrect choice !'))
        time.sleep(1)
        configmodify(data)
    if configchoice > len(info):
        print(colorText('[[red]]\n[!] Incorrect choice !'))
        time.sleep(1)
        configmodify(data)
    else:
        replit.clear()

    choice = input(colorText(
        '[[' + defaultcolor + ']][1] Modify IP\n[2] Change username \n[3] Change key path (if exists) \n[4] Change password (if defined) \n[5] Change port\n\n[0] Back\n\n[?] Choice : '))
    try:
        choice = int(choice)
        with open('config.json', 'r') as f:
            data = json.load(f)
            f.close()
    except ValueError:
        print(colorText('[[red]]\n[!] Incorrect choice !'))
        time.sleep(1)
        configmodify(data)
    if choice > 6:
        print(colorText('[[red]]\n[!] Incorrect choice !'))
        time.sleep(1)
        configmodify(data)
    elif choice == 0:
        configmenu(data)
    elif choice == 1:
        newip = input(colorText('\nNew IP Adress : '))
        if bool(re.match(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', newip)):
            pass
        else:
            print(colorText('[[red]][!] Incorrect syntax !\n'))
            time.sleep(1)
            replit.clear()
            configmodify(data)
        with open('config.json', 'w') as f:
            data[f'{configchoice}']['ip'] = newip
            json.dump(data, f, indent=4)
    elif choice == 2:
        newusername = input(colorText('\nNew username : '))
        with open('config.json', 'w') as f:
            data[f'{configchoice}']['username'] = newusername
            json.dump(data, f, indent=4)
    elif choice == 3:
        try:
            pathh = data[f'{configchoice}']['path']
            pathh = input(colorText('[[' + defaultcolor + ']]\nNew path : '))
        except KeyError:
            print(
                colorText('[[red]]\n[!] This configuration has no registered path '))
            time.sleep(2)
            hub()
        if (isvalidpath(pathh)):
            data[f'{configchoice}']['path'] = pathh
            json.dump(data, f, indent=4)
        else:
            print(
                colorText('[[red]][!] Invalid path !'))
            time.sleep(1)
            configmodify(data)
    elif choice == 4:
        try:
            passw = data[f'{configchoice}']['password']
            passw = input(
                colorText('[[' + defaultcolor + ']]\nNew password : '))
            data[f'{configchoice}']['password'] = passw
            json.dump(data, f, indent=4)
        except KeyError:
            print(
                colorText('[[red]]\n[!] This configuration has not registred password '))
            time.sleep(2)
            hub()
    elif choice == 5:
        newport = input(colorText('[[' + defaultcolor + ']]\nNew port : '))
        try:
            newport = int(newport)
        except ValueError:
            print(colorText('\n[[red]][!] Invalid port !'))
            time.sleep(1)
            configmodify(data)
        data[f'{configchoice}']['port'] = newport
        json.dump(data, f, indent=4)

    replit.clear()
    hub()


def menu(number, data):
    print('\n')
    for i in range(number):
        l = i + 1
        try:
            response_list = ping(
                data[f'{l}']['ip'], size=40, count=5)
            Online = 'Online'
        except:
            Online = 'Offline'
        if Online == "Online":
            print(
                colorText('[[' + defaultcolor + ']][' + str(i+1) + '] Fast connect to ' + data[f'{l}']['username'] + '@' + data[f'{l}']['ip'] + ' [[green]](Online : ' + pingcolor(round(response_list.rtt_avg_ms)) + '[[green]])[[' + defaultcolor + ']]'))
        else:
            print(
                colorText('[[' + defaultcolor + ']][' + str(i+1) + '] Fast connect to ' + data[f'{l}']['username'] + '@' + data[f'{l}']['ip'] + ' [[red]](Offline)' + '[[' + defaultcolor + ']]'))

    print(colorText('[[magenta]]\n\n\n[99] Edit configurations'))
    choice = input(colorText('[[' + defaultcolor + ']]' + '\n[?] Choice : '))
    try:
        choice = int(choice)
    except ValueError:
        print(colorText('[[red]]\n[!] Invalid choice !'))
        time.sleep(1)
        replit.clear()
        hub()
    print(number)
    if choice == 99:
        configmenu(data)
    elif choice > number:
        print(colorText('[[red]]\n[!] Invalid choice !'))
        time.sleep(1)
        replit.clear()
        hub()
    elif choice <= number:
        replit.clear()
        print(colorText('[[green]][+] Currently connecting to your server...'))
        time.sleep(2)
        replit.clear()
        try:
            data[f'{choice}']['path']
            key = True
        except KeyError:
            key = False
        if key:
            os.system(
                'ssh -i ' + data[f'{choice}']['path'] + ' ' + data[f'{choice}']['username'] + "@" + data[f'{choice}']['ip'])
        else:
            os.system('sshpass -p ' + data[f'{choice}']['password'] + ' ssh' +
                      data[f'{choice}']['username'] + "@" + data[f'{choice}']['ip'])


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
                                  '\n---------------------------------------------\nFirst of all, do you have a ssh key ? Y/N : '))
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
    hub()


if __name__ == "__main__":
    hub()
