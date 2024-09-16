
def load_file(arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Falha ao carregar o arquivo: {e}")

def save_file(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Falha ao salvar o arquivo: {e}")       