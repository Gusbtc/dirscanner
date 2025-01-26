import requests
import threading

try:
    print('''
    ██████████    ███                                                                                  
    ░░███░░░░███  ░░░                                                                                   
    ░███   ░░███ ████  ████████      █████   ██████   ██████   ████████   ████████    ██████  ████████ 
    ░███    ░███░░███ ░░███░░███    ███░░   ███░░███ ░░░░░███ ░░███░░███ ░░███░░███  ███░░███░░███░░███
    ░███    ░███ ░███  ░███ ░░░    ░░█████ ░███ ░░░   ███████  ░███ ░███  ░███ ░███ ░███████  ░███ ░░░ 
    ░███    ███  ░███  ░███         ░░░░███░███  ███ ███░░███  ░███ ░███  ░███ ░███ ░███░░░   ░███     
    ██████████   █████ █████        ██████ ░░██████ ░░████████ ████ █████ ████ █████░░██████  █████    
    ░░░░░░░░░░   ░░░░░ ░░░░░        ░░░░░░   ░░░░░░   ░░░░░░░░ ░░░░ ░░░░░ ░░░░ ░░░░░  ░░░░░░  ░░░░░  

Github do criador: https://github.com/Gusbtc\n''')

    url = input('Coloque a URL alvo: ')

    if "http" not in url:
        print(f'''
Use um formato válido para URL: 
http://exemplo.com OU https://exemplo.com''')
        quit()

    wordlist = input('Coloque o caminho do arquivo da wordlist: ')
    threads = input('Quantas threads você vai querer rodar? (default = 5): ')
    if threads == "":
        threads = 5
    else:
        threads = int(threads)
    print()

    # Verificar se a wordlist existe
    try:
        with open(wordlist, "r") as lista:
            linhas = lista.readlines()
            qtdLinhas = len(linhas)
    except:
        print('Não foi possível abrir este arquivo.')
        quit()

    # Adicionar barra ao final da URL, se necessário
    if url[-1] != "/":
        url += "/"

    # Verificar se a URL é válida e está online
    try:
        requests.get(url)
    except:
        print('\nSite não encontrado, está offline ou o link é inválido.')
        quit()

    # Função para verificar links
    def verificarOnline(sublist, url):
        for i in sublist:
            link = url + i.strip()
            try:
                requisicao = requests.get(link)
                if requisicao.status_code != 404:
                    print(f'Link encontrado [{requisicao.status_code}]: {link}')
            except requests.RequestException:
                pass

    print(f'Procurando por diretórios escondidos em {url}')
    print(f'Usando a wordlist {wordlist} (contém {qtdLinhas} linhas) ')
    print(f'Usando {threads} threads\n')

    # Divisão da lista entre as threads
    tamanho = qtdLinhas // threads
    threadList = []

    for i in range(threads):
        inicio = i * tamanho
        if i == threads - 1:
            fim = qtdLinhas
        else:
            fim = (i + 1) * tamanho

        sublist = linhas[inicio:fim]

        thread = threading.Thread(target=verificarOnline, args=(sublist, url))
        thread.start()
        threadList.append(thread)

    # Aguardar todas as threads terminarem
    for thread in threadList:
        thread.join()

except KeyboardInterrupt:
    print('\nSaindo...')
    quit()
except Exception as erro:
    print(f"Ocorreu um erro inesperado:\n {erro}")
