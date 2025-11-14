import requests
import pandas as pd
from datetime import datetime
import os.path
import glob
import shutil
from dateutil.relativedelta import relativedelta


data_atual = datetime.today()
dia_hoje = datetime.today().strftime('%d')
mes_hoje = datetime.today().strftime('%m')
ano_hoje = datetime.today().strftime('%Y')
data_hoje = datetime.today().strftime('%Y-%m-%d')
diretorio = "/home/wanderson/API/diario_de_bordo/col"

url = f"http://newmonitor.virtua.com.br/repositorio/rels/gmud/GMUD_{ano_hoje}_{mes_hoje}_REL.XLS.zip"
arquivo_zip = f'relatorio_gmud_{data_hoje}.zip'
arquivo_final = f"gmud_rel.csv"
arquivo_xls = f"GMUD_{ano_hoje}_{mes_hoje}_REL.XLS"
arquivo_csv = f"GMUD_{ano_hoje}_{mes_hoje}_REL.XLS.csv"

prox_mes_ano = data_atual + relativedelta(months=1)
prox_mes = prox_mes_ano.strftime('%m')
prox_ano = prox_mes_ano.strftime('%Y')

arquivo_zip_f = f'relatorio_gmud_{prox_ano}_{prox_mes}.zip'
arquivo_xls_f = f"GMUD_{prox_ano}_{prox_mes}_REL.XLS"
arquivo_csv_f = f"GMUD_{prox_ano}_{prox_mes}_REL.XLS.csv"
url_prox_mes = f"http://newmonitor.virtua.com.br/repositorio/rels/gmud/GMUD_{prox_ano}_{prox_mes}_REL.XLS.zip"


cidades = ["Macei","Aquiraz","Arapiraca","Eusebio","Fortaleza","Juazeiro do Norte","Sobral","Cabedelo",\
"Campina Grande","João Pessoa","Caruaru","Jaboatão dos Guararapes","Olinda","Paulista",\
"Petrolina","Recife","Parnaiba","Teresina","Timon","Mossor","Natal","Parnamirim"]


for z in glob.glob(f"{diretorio}/*.csv"):
    print (z)
    df = pd.read_csv(z, on_bad_lines='skip', encoding="latin-1")

    # df = pd.concat([df, df])

print (df)


# def baixar_arquivo_por_link(link, nome_arquivo):
#     while True:
#         response = requests.get(link)
#         if response.status_code == 200:
#             with open(nome_arquivo, 'wb') as file:
#                 file.write(response.content)
#             print(f'O arquivo {nome_arquivo} foi baixado com sucesso.')
#             break

#         elif response.status_code == 404:
#             print(f'{nome_arquivo} ainda não existe. Código de status: {response.status_code}')
#             break

#         else:
#             print(f'Erro ao baixar o {nome_arquivo}. Código de status: {response.status_code}')
#             continue



# def tratamento():
#     df = pd.DataFrame()

#     arquivos_zip = glob.glob(os.path.join(diretorio, '*.zip'))


#     for x in arquivos_zip:
#         shutil.unpack_archive(f"{x}", diretorio)

#         os.remove(x)

#     arquivos_xls = glob.glob(os.path.join(diretorio, '*.XLS'))
#     for y in arquivos_xls:
#         os.rename(y, f"{y}.csv")


#     df1 = pd.read_csv(f"{diretorio}/{arquivo_csv}", on_bad_lines='skip', encoding="latin-1")
#     df1 = df1.columns[0]
#     df1 = str(df1)

#     os.remove(f"{diretorio}/{arquivo_csv}")
#     os.remove(f"{diretorio}/{arquivo_csv_f}")

#     with open (f"{diretorio}/log.txt", "a") as file:
#         hora = datetime.today().strftime('%H:%M')
#         file.write(f"{data_hoje} - {hora} -> {df1}\n")




# baixar_arquivo_por_link(url,f"{diretorio}/{arquivo_zip}")
# baixar_arquivo_por_link(url_prox_mes,f"{diretorio}/{arquivo_zip_f}")

# tratamento ()