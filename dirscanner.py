import requests

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

    url = input('Coloque a url alvo: ')
    wordlist = input('Coloque o caminho do arquivo da wordlist: ')
    print()

    # Verificar se a wordlist existe e se nos conseguimos abrir o arquivo
    try:
        open(wordlist, "r")
    except:
        print('Nao foi possivel abrir este arquivo.')
        quit()

    # Se o fim da URL passada nao tiver com um / nos colocamos
    if url[-1] != "/":
        url = url + "/"

    if "http" not in url:
        print(f'''
    Use um formato valido para URL: 
    http://exemplo.com OU https://exemplo.com''')

    # Verificar se a URL passada é válida e está online
    try:
        requests.get(url)
    except:
        print('\nSite nao encontrado ou esta offline ou o link é inválido.')
        quit()

    with open(wordlist, "r") as lista:
        print(f'Procurando por diretorios escondidos em {url}')
        print(f'Usando a wordlist {wordlist} \n')
        for i in lista.readlines():
            link = url + i.replace('\n', '')
            requisicao = requests.get(link)
            #print(f'Testando: {link}')
            if requisicao.status_code != 404:
                print(f'Link encontrado [{requisicao.status_code}]: {link}')
except:
    print('\nSaindo...')
    quit()