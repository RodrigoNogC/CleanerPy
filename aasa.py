import pandas as pd
import re

# Lê a planilha Excel usando a engine 'xlrd'
planilha = pd.read_excel('OI FIBRA 01042024.xlsx')

# Função para extrair o logradouro, número do logradouro e CEP
def extrair_dados(texto):
    # Expressão regular para encontrar o logradouro e número
    padrao_logradouro = r'([^\d]+) (\d+)'
    match_logradouro = re.match(padrao_logradouro, texto)

    if match_logradouro:
        logradouro = match_logradouro.group(1).strip()
        numero_logradouro = match_logradouro.group(2)
    else:
        logradouro = None
        numero_logradouro = None

    # Expressão regular para encontrar o CEP
    padrao_cep = r'\b\d{8}\b'
    match_cep = re.search(padrao_cep, texto)

    if match_cep:
        cep = match_cep.group()
    else:
        cep = None

    return logradouro, numero_logradouro, cep

# Aplica a função a cada linha da planilha e cria novas colunas
planilha['Logradouro'], planilha['Numero Logradouro'], planilha['CEP'] = zip(*planilha['Endereço'].apply(extrair_dados))

# Salva a planilha com os novos dados
planilha.to_excel('OI FIBRA 01042024.xlsx', index=False)