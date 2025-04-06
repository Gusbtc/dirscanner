import requests
import argparse
import random
from concurrent.futures import ThreadPoolExecutor

colors = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "light_black": "\033[90m",
    "light_red": "\033[91m",
    "light_green": "\033[92m",
    "light_yellow": "\033[93m",
    "light_blue": "\033[94m",
    "light_magenta": "\033[95m",
    "light_cyan": "\033[96m",
    "bright_white": "\033[97m",
    "reset": "\033[0m"
}

def verifyOnline(url):
    try:
        req = requests.get(url)
        response = req.status_code
        if response != 404:
            print(f"{colors['green']}[+] {url:<50} {'found!':<5} - {response}{colors['reset']}")
            
    except Exception as e:
        print(f'{colors['red']}[-] This website is invalid {e}{colors['reset']}')
    except KeyboardInterrupt:
        print(f'{colors['yellow']}[-] Leaving... {colors['reset']}')
        quit()


def printBanner(args):
    color, value = random.choice(list(colors.items()))
    while color == 'reset':
        color, value = random.choice(list(colors.items()))

    print(rf"""{colors[color]}           ___ _                                          
          /   (_)_ __ ___  ___ __ _ _ __  _ __   ___ _ __ 
         / /\ / | '__/ __|/ __/ _` | '_ \| '_ \ / _ \ '__|
        / /_//| | |  \__ \ (_| (_| | | | | | | |  __/ |   
       /___,' |_|_|  |___/\___\__,_|_| |_|_| |_|\___|_|   
          
{"[+] Target:":<54} {args.url}
{"[+] Threads:":<54} {args.threads}
{"[+] Wordlist:":<54} {args.wordlist}
{colors['reset']}""")

def getArguments():
    parser = argparse.ArgumentParser(
            prog="Dirscanner",
            description="Um escaner que busca por diretórios ocultos em aplicações web usando uma wordlist",
        )

    parser.add_argument('-w', '--wordlist', help='A wordlist que será usada', required=True, metavar='')
    parser.add_argument('-u', '--url', help='A url a ser escaneada', required=True, metavar='')
    parser.add_argument('-t', '--threads', default=30, help='Quantas threads serão usadas (Default: 5)', metavar='', type=int)

    args = parser.parse_args()

    # Verificacoes dos argumentos

    if "http" not in args.url:
        print(f"{colors['red']}[-] Please put a valid URL (http or https){colors['reset']}")
        quit()

    if args.url[-1] != '/':
        args.url += '/'

    try:
        open(args.wordlist)
    except:
        print(f'{colors['red']}[-] Couldn\'t open wordlist file{colors['reset']}')
        quit()

    return args

def main():
    args = getArguments()
    printBanner(args)
    
    targets = []
    with open(args.wordlist, 'r') as wordlist:
        for i in wordlist.readlines():
            targets.append(f"{args.url}{i.strip()}")

    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            executor.map(verifyOnline, targets)

    except KeyboardInterrupt:
        executor.shutdown(wait=False, cancel_futures=True)
        print(f'{colors['yellow']}[-] Leaving... {colors['reset']}')
        quit()

if __name__ == "__main__": 
    main()