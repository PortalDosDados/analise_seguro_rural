import os

import pandas as pd
import requests

URL1 = 'https://dados.agricultura.gov.br/dataset/baefdc68-9bad-4204-83e8-f2888b79ab48/resource/97f29a77-4e7e-44bf-99b3-a2d75911b6bf/download/dados_abertos_psr_2006a2015csv.csv'

URL2 = 'https://dados.agricultura.gov.br/dataset/baefdc68-9bad-4204-83e8-f2888b79ab48/resource/54e04a6b-15b3-4bda-a330-b8e805deabe4/download/dados_abertos_psr_2016a2024csv.csv'

URL3 = 'https://dados.agricultura.gov.br/dataset/baefdc68-9bad-4204-83e8-f2888b79ab48/resource/ac7e4351-974f-4958-9294-627c5cbf289a/download/dados_abertos_psr_2025csv.csv'

os.makedirs('data', exist_ok=True)


def baixar(url, nome_arquivo):

    resposta = requests.get(url)

    resposta.raise_for_status()

    with open(nome_arquivo, 'wb') as f:
        f.write(resposta.content)

    print(f"{nome_arquivo} baixado")


baixar(URL1, 'data/psr_2006_2015.csv')
baixar(URL2, 'data/psr_2016_2024.csv')
baixar(URL3, 'data/psr_2025.csv')


def mergear_dados():

    read_opts = dict(sep=";", encoding="ansi", on_bad_lines="skip", engine="python")
    df1 = pd.read_csv("data/psr_2006_2015.csv", **read_opts)
    df2 = pd.read_csv("data/psr_2016_2024.csv", **read_opts)
    df3 = pd.read_csv("data/psr_2025.csv", **read_opts)

    df_total = pd.concat([df1, df2, df3])

    df_total.to_csv('data/seguro_rural_total.csv', index=False)

    print('Dataset consolidado criado')


mergear_dados()
