import requests
import pandas as pd
from datetime import datetime
import os.path
import glob
import shutil
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()

data_atual = datetime.today()
dia_hoje = datetime.today().strftime('%d')
mes_hoje = datetime.today().strftime('%m')
ano_hoje = datetime.today().strftime('%Y')
data_hoje = datetime.today().strftime('%Y-%m-%d')
diretorio = os.getenv("DIRETORIO")
url = os.getenv("URL")



url = f"{url}/repositorio/rels/gmud/GMUD_{ano_hoje}_{mes_hoje}_REL.XLS.zip"
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
url_prox_mes = f"{url}/repositorio/rels/gmud/GMUD_{prox_ano}_{prox_mes}_REL.XLS.zip"


cidades = ["Maceió","Aquiraz","Arapiraca","Eusebio","Fortaleza","Juazeiro do Norte","Sobral","Cabedelo",\
            "Campina Grande","João Pessoa","Caruaru","Jaboatão dos Guararapes","Olinda", "Paulista",\
            "Petrolina","Recife","Parnaiba","Teresina","Timon","Mossoro","Natal","Parnamirim", \
            "- SGO - Maceió","- SGO - Arapiraca","- SGO - Fortaleza",\
            "- SGO - Cabedelo","- SGO - Campina Grande","- SGO - João Pessoa","- SGO - Caruaru",\
            "- SGO - Jaboatão dos Guararapes","- SGO - Olinda", "- SGO - Paulista",\
            "- SGO - Recife","- SGO - Teresina","- SGO - Natal","- SGO - Parnamirim"]


def baixar_arquivo_por_link(link, nome_arquivo):
    while True:
        response = requests.get(link)
        if response.status_code == 200:
            with open(nome_arquivo, 'wb') as file:
                file.write(response.content)
            print(f'O arquivo {nome_arquivo} foi baixado com sucesso.')
            break

        elif response.status_code == 404:
            print(f'{nome_arquivo} ainda não existe. Código de status: {response.status_code}')
            break

        else:
            print(f'Erro ao baixar o {nome_arquivo}. Código de status: {response.status_code}')
            continue



def tratamento():
    df = pd.DataFrame()

    arquivos_zip = glob.glob(os.path.join(diretorio, '*.zip'))

    for x in arquivos_zip:
        shutil.unpack_archive(f"{x}", diretorio)
        os.remove(x)

    arquivos_xls = glob.glob(os.path.join(diretorio, '*.XLS'))
    for y in arquivos_xls:
        os.rename(y, f"{y}.csv")


    df_z = pd.DataFrame()
    for z in glob.glob(f"{diretorio}/*REL*.csv"):

        df = pd.read_csv(z, delimiter="\t", encoding='latin-1', skiprows=1,index_col=False)
        df_z = pd.concat([df_z, df])


    df_filtrado = pd.DataFrame()
    for i in cidades:
        filtro = df_z['CIDADE'].str.contains(f"^{i}$", case=False)
        df_filtrado = pd.concat([df_filtrado, df_z[filtro]])


    df_filtrado = df_filtrado.replace(to_replace=r'^- SGO - ', value='', regex=True)
    print (df_filtrado)



    # df_filtrado = df_filtrado.drop_duplicates(subset="TICKET", keep='first')
    df_filtrado.to_csv(f"{diretorio}/{arquivo_final}", index=False,encoding="latin-1") 
    df_filtrado = pd.read_csv(f"{diretorio}/{arquivo_final}",encoding="latin-1")

  
     
# if os.path.isfile(f"{diretorio}/{arquivo_zip}") == True:
#     print (f"{diretorio}/{arquivo_zip} existe, realizando o tratamento...")
#     tratamento ()

# else:
    # print (f"{diretorio}/{arquivo_zip} não existe, realizando o download... em seguida o tratamento")
baixar_arquivo_por_link(url,f"{diretorio}/{arquivo_zip}")
baixar_arquivo_por_link(url_prox_mes,f"{diretorio}/{arquivo_zip_f}")

tratamento ()


    
