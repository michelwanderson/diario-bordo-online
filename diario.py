import pandas as pd
import streamlit as st
from datetime import datetime
import os
from io import BytesIO
from dotenv import load_dotenv


#streamlit run diario.py --server.port=6510

load_dotenv()
diretorio = os.getenv("DIRETORIO")



st.set_page_config(
    page_title="Diário ONline",
    page_icon=":clipboard:",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("Diário ONline de Bordo NE 📌")


with st.sidebar:
    data_escolhida = st.date_input("Escolha Data: ", value="today", min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, kwargs=None,
                                   format="DD/MM/YYYY", label_visibility="visible")

    st.divider()


df = pd.read_csv(f"{diretorio}/gmud_rel.csv", encoding="latin-1", dtype={'TICKET': str})
df = df.rename(columns={'NIVEL_INFRA': 'NÍVEL INFRA',
                        'ESCOPO_TECNICO': 'ESCOPO TÉCNICO',
                        'SOLUCAO': 'SITUAÇÃO',
                        'DT_INI_PREVISTO': 'DATA',
                        'USUARIO_ABERTURA': 'RESP. ABERTURA'
                        })

# Deixando a coluna DATA no padrão
df['DATA'] = pd.to_datetime(df['DATA']).dt.strftime('%d-%m-%Y')


# Deixando a data escolhida no padrão
data_escolhida = data_escolhida.strftime('%d-%m-%Y')





def colorize(val):
    if val == 'Realizada totalmente' or val == 'Sucesso':
        return 'background-color: green; color: white;'
    elif val == 'Realizado Rollback':
        return 'background-color: red; color: white;'
    else:
        return ''




df = df[['DATA', 'TICKET', 'CIDADE', 'OBJETIVO', 'NÍVEL INFRA',
         'NATUREZA', 'RESP. ABERTURA', 'AVALIACAO', 'ESCOPO TÉCNICO', 'SITUAÇÃO']]
df_filtrado_data = df.loc[(df['DATA'] == data_escolhida)]


# Mudando o status da coluna SITUAÇÃO em vazio para aguardando status
df_filtrado_data.loc[:, 'SITUAÇÃO'] = df_filtrado_data['SITUAÇÃO'].fillna("Aguardando Ações")


# Ajustando os nomes dos resposáveis
# df_filtrado_data.loc[:, 'RESP. ABERTURA'] = df_filtrado_data['RESP. ABERTURA'].apply(lambda x: ' '.join(x.split()[:2]))
df_filtrado_data.loc[:, 'RESP. ABERTURA'] = df_filtrado_data['RESP. ABERTURA'].apply(lambda x: ' '.join([x.split()[0], x.split()[-1]]))
df_filtrado_data.loc[:, 'RESP. ABERTURA'] = df_filtrado_data['RESP. ABERTURA'].apply(lambda x: x.title())



if len(df_filtrado_data) != 0:
    # Caixa para Pesquia
    filtro = st.text_input("Busca:")


    # Criando duas novas colunas
    df_filtrado_data = df_filtrado_data.assign(EXECUÇÃO='')
    df_filtrado_data = df_filtrado_data.assign(**{"PÓS EXECUÇÃO": ''})




    # Mecanismo para retorno do filtro
    if filtro.strip():
        df_filtrado_data = df_filtrado_data[df_filtrado_data.apply(
            lambda linha: linha.str.contains(filtro, case=False).any(), axis=1)]
        st.data_editor(df_filtrado_data.style.map(colorize, subset=['SITUAÇÃO']), disabled=["DATA", "TICKET", "CIDADE", "OBJETIVO", "NÍVEL INFRA", "NATUREZA", "RESP. ABERTURA", "AVALIACAO", "ESCOPO TÉCNICO", "SITUAÇÃO"],
                    hide_index=True)
    else:
        df_filtrado_data = st.data_editor(df_filtrado_data.style.map(colorize, subset=['SITUAÇÃO']), disabled=["DATA", "TICKET", "CIDADE", "OBJETIVO", "NÍVEL INFRA", "NATUREZA", "RESP. ABERTURA", "AVALIACAO", "ESCOPO TÉCNICO", "SITUAÇÃO"],
                                        hide_index=True)




    # Quantidade de Manobras
    with st.sidebar:
        quant_manobras = df_filtrado_data['TICKET'].count()
        # st.metric(label="Quantidade Total de Manobras", value=(quant_manobras), delta=-5, delta_color="normal")
        st.metric(label="Quantidade Total de Manobras", value=(quant_manobras))


    @st.cache_data
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name=data_escolhida, index=False)
        writer.close()
        processed_data = output.getvalue()
        return processed_data


    df = to_excel(df_filtrado_data)


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3:
        st.download_button(label="Download ⬇️", type="primary",data=df, file_name=f"diario_de_bordo_{data_escolhida}.xlsx")


else:
    st.error("Não existem manobras para essa data!")

# Informações de atualização no arquivo do mês vigente
mes_hoje = datetime.today().strftime('%Y_%m')
df2 = pd.read_csv(f"{diretorio}/GMUD_{mes_hoje}_REL.XLS.csv", on_bad_lines='skip', encoding="latin-1")
df2 = df2.columns[0]
df2 = str(df2)
st.info(f"Última {df2}", icon="ℹ️")
