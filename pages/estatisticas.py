import pandas as pd
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv



load_dotenv()
diretorio = os.getenv("DIRETORIO")



st.set_page_config(
    page_title="Estatística de Bordo",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)



def hyperlink(val):
    return f'<a href="http://newmonitor/user/gi/gi_view.php?idTicket={val}" target="_blank">{val}</a>'


st.title("Estatísticas de Bordo 📈")
# st.markdown("<h2 style='text-align: center; color: gray;'>Estatísticas de Bordo 📈</h2>", unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: black;'>Em Desenvolvimento 🔨</h3>", unsafe_allow_html=True)



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

df = df[['DATA', 'TICKET', 'CIDADE', 'FECHAMENTO', 'RESP. ABERTURA', 'NATUREZA', 'SITUAÇÃO']]
df_filtrado_data = df.loc[(df['DATA'] == data_escolhida)]

# Mudando o status da coluna SITUAÇÃO em vazio para aguardando status
df_filtrado_data.loc[:, 'SITUAÇÃO'] = df_filtrado_data['SITUAÇÃO'].fillna("Aguardando Ações")


# Ajustando os nomes dos resposáveis
df_filtrado_data.loc[:, 'RESP. ABERTURA'] = df_filtrado_data['RESP. ABERTURA'].apply(lambda x: ' '.join(x.split()[:2]))


# df_filtrado_data['TICKET'] = df_filtrado_data['TICKET'].apply(hyperlink)
df_filtrado_data.loc[:,'TICKET'] = df_filtrado_data['TICKET'].apply(hyperlink)



if len(df_filtrado_data) != 0:

    # Filtros e Soma
    # Por DIA: MANOBRAS
    manobras_total_dia = df_filtrado_data['TICKET'].count()
    filtro_manobras_ok_dia = df_filtrado_data.loc[(df_filtrado_data['FECHAMENTO'] == 'Realizada')]
    manobras_ok_dia = filtro_manobras_ok_dia.shape[0]
    filtro_manobras_NOK_dia = df_filtrado_data.loc[(df_filtrado_data['FECHAMENTO'] != 'Realizada')]
    manobras_NOK_dia = filtro_manobras_NOK_dia.shape[0]



    # Por MES: MANOBRAS
    mes_escolhido = data_escolhida.split("-")[1]
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d-%m-%Y', errors='coerce')
    df_filtrado_mes = df.loc[df['DATA'].dt.strftime('%m') == mes_escolhido]

    manobras_total_mes = df_filtrado_mes['TICKET'].count()
    filtro_manobras_ok_mes = df_filtrado_mes.loc[(df_filtrado_mes['FECHAMENTO'] == 'Realizada')]
    manobras_ok_mes = filtro_manobras_ok_mes.shape[0]
    filtro_manobras_NOK_mes = df_filtrado_mes.loc[(df_filtrado_mes['FECHAMENTO'] != 'Realizada')]
    manobras_NOK_mes = filtro_manobras_NOK_mes.shape[0]


    # Graficos Diario : MANOBRAS
    legendas = 'REALIZADA', 'NÃO REALIZADA'
    valores = [manobras_ok_dia, manobras_NOK_dia]
    explode = (0, 0.1)
    cores = ['#32CD32', '#FF0000']
    fig1, ax1 = plt.subplots()
    # fig1.suptitle('Diário', fontweight='bold')
    ax1.pie(valores, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90, colors=cores)
    ax1.legend(['Realizada', 'Não Realizada'], loc='upper right')



    # Graficos Mensal : MANOBRAS
    # legendas = ["REALIZADA", "NÃO REALIZADA"], loc= "upper right"
    valores = [manobras_ok_mes, manobras_NOK_mes]
    explode = (0, 0.1)
    cores = ['#00CC00', '#FF0000']
    fig2, ax2 = plt.subplots()
    # fig2.suptitle('Mensal', fontweight='bold')
    ax2.pie(valores, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90, colors=cores)
    


    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h3 style='text-align: center; color: gray;'>Visão Geral Diário</h3>", unsafe_allow_html=True)
        st.pyplot(fig1)
        st.info(f"Total: {manobras_total_dia}")
        st.success(f"Sucesso: {manobras_ok_dia}")
        st.error(f"Insucesso: {manobras_NOK_dia}")

    with col2:
        st.markdown("<h3 style='text-align: center; color: gray;'>Visão Geral Mensal</h3>", unsafe_allow_html=True)
        st.pyplot(fig2)
        st.info(f"Total: {manobras_total_mes}")
        st.success(f"Sucesso: {manobras_ok_mes}")
        st.error(f"Insucesso: {manobras_NOK_mes}")

    with col3:
        pass





    # FILTROS E SOMA
    # Programadas -> dia
    # manobras_total_prog_dia = df_filtrado_data['NATUREZA'].count()
    manobras_total_prog_dia = df_filtrado_data[df_filtrado_data['NATUREZA'] == 'Programada']['TICKET'].count()
    manobras_prog_dia = df_filtrado_data.loc[(df_filtrado_data['NATUREZA'] == 'Programada') & (df_filtrado_data['FECHAMENTO'] == 'Realizada')]
    manobras_prog_dia =  manobras_prog_dia.shape[0]
    manobras_NOK_prog_dia = df_filtrado_data.loc[(df_filtrado_data['NATUREZA'] == 'Programada') & (df_filtrado_data['FECHAMENTO'] != 'Realizada')]
    manobras_NOK_prog_dia =  manobras_NOK_prog_dia.shape[0]

    
    

    # Programadas -> mês
    # manobras_total_prog_mes = df_filtrado_mes['NATUREZA'].count()
    manobras_total_prog_mes = df_filtrado_mes[df_filtrado_mes['NATUREZA'] == 'Programada']['TICKET'].count()
    manobras_prog_mes = df_filtrado_mes.loc[(df_filtrado_mes['NATUREZA'] == 'Programada') & (df_filtrado_mes['FECHAMENTO'] == 'Realizada')]
    manobras_prog_mes = manobras_prog_mes.shape[0]
    manobras_NOK_prog_mes = df_filtrado_mes.loc[(df_filtrado_mes['NATUREZA'] == 'Programada') & (df_filtrado_mes['FECHAMENTO'] != 'Realizada')]
    manobras_NOK_prog_mes = manobras_NOK_prog_mes.shape[0]

    # Emergenciais -> dia
    # manobras_total_emerg_dia = (df_filtrado_data['NATUREZA'] == 'Emergencial').count()
    manobras_total_emerg_dia = df_filtrado_data[df_filtrado_data['NATUREZA'] == 'Emergencial']['TICKET'].count()
    manobras_emerg_dia = df_filtrado_data.loc[(df_filtrado_data['NATUREZA'] == 'Emergencial') & (df_filtrado_data['FECHAMENTO'] == 'Realizada')]
    manobras_emerg_dia =  manobras_emerg_dia.shape[0]
    manobras_NOK_emerg_dia = df_filtrado_data.loc[(df_filtrado_data['NATUREZA'] == 'Emergencial') & (df_filtrado_data['FECHAMENTO'] != 'Realizada')]
    manobras_NOK_emerg_dia =  manobras_NOK_emerg_dia.shape[0]
    

    # Emergenciais -> mes
    manobras_total_emerg_mes = df_filtrado_mes[df_filtrado_mes['NATUREZA'] == 'Emergencial']['TICKET'].count()
    manobras_emerg_mes = df_filtrado_mes.loc[(df_filtrado_mes['NATUREZA'] == 'Emergencial') & (df_filtrado_mes['FECHAMENTO'] == 'Realizada')]
    manobras_emerg_mes = manobras_emerg_mes.shape[0]
    manobras_NOK_emerg_mes = df_filtrado_mes.loc[(df_filtrado_mes['NATUREZA'] == 'Emergencial') & (df_filtrado_mes['FECHAMENTO'] != 'Realizada')]
    manobras_NOK_emerg_mes = manobras_NOK_emerg_mes.shape[0]

    st.divider()




    # Graficos PROGAMADA DIARIO
    vals_prog_dia = [manobras_prog_dia, manobras_NOK_prog_dia]

    # Verificação para garantir que ao menos um valor seja positivo
    if all(val == 0 for val in vals_prog_dia):
        vals_prog_dia = [0, 1]  # Substituir zeros por valores mínimos
        leg_graf_prog_dia = 'SEM MANOBRAS',''
        cores_prog_dia = ['#FFFFFF', '#FFFFFF']
        porcentagem = None
    else:
        leg_graf_prog_dia = 'Realizada', 'Não Realizada'
        cores_prog_dia = ['#03bb85', '#FF5733']
        porcentagem = '%1.1f%%'


    fig3, ax3 = plt.subplots()
    ax3.pie(vals_prog_dia, explode=explode, autopct=porcentagem, shadow=True, startangle=120, colors=cores_prog_dia)
    ax3.legend(leg_graf_prog_dia, loc='upper right')


    # Graficos PROGAMADA MENSAL
    leg_graf_prog_mes = 'Realizada', 'Não Realizada'
    vals_prog_mes = [manobras_prog_mes, manobras_NOK_prog_mes]
    # cores_prog_mes = ['#00FF00', '#800080']
    cores_prog_mes  = ['#03bb85', '#FF5733']
    fig4, ax4 = plt.subplots()
    ax4.pie(vals_prog_mes, explode=explode, autopct='%1.1f%%', shadow=True, startangle=60, colors=cores_prog_mes)
    ax4.legend(['Realizada', 'Não Realizada'], loc='upper right')


    # Graficos EMERGENCIAL: DIARIO
    vals_emerg_dia = [manobras_emerg_dia, manobras_NOK_emerg_dia]
    if all (val == 0 for val in vals_emerg_dia):
        vals_emerg_dia = [0, 1]
        leg_graf_emerg_dia = 'SEM MANOBRAS',''
        cores_emerg_dia = ['#FFFFFF', '#FFFFFF']
        porcentagem = None
    else:
        leg_graf_emerg_dia = 'Realizada', 'Não Realizada'
        cores_emerg_dia = ['#00FF00', '#800080']
        porcentagem = '%1.1f%%'

    fig5, ax5 = plt.subplots()
    ax5.pie(vals_emerg_dia, explode=explode, autopct=porcentagem, shadow=True, startangle=120, colors=cores_emerg_dia)
    ax5.legend(leg_graf_emerg_dia, loc='upper right')



    # Graficos EMERGENCIAL: MENSAL
    vals_emerg_mes = [manobras_emerg_mes, manobras_NOK_emerg_mes]

    if all (val == 0 for val in vals_emerg_mes):
        vals_emerg_mes = [0, 1]
        leg_graf_emerg_mes = 'SEM MANOBRAS',''
        cores_emerg_mes = ['#FFFFFF', '#FFFFFF']
        porcentagem = None
    else:
        leg_graf_emerg_mes = 'Realizada', 'Não Realizada'
        cores_emerg_mes = ['#00FF00', '#800080']
        porcentagem = '%1.1f%%'
        

    fig6, ax6 = plt.subplots()
    ax6.pie(vals_emerg_mes, explode=explode, autopct=porcentagem, shadow=True, startangle=60, colors=cores_emerg_mes)
    ax6.legend(leg_graf_emerg_mes, loc='upper right')

   
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<h3 style='text-align: center; color: gray;'>Programadas Diário</h3>", unsafe_allow_html=True)
        st.pyplot(fig3)
        st.info(f"Total: {manobras_total_prog_dia}")
        st.success(f"Sucesso: {manobras_prog_dia}")
        st.error(f"Insucesso: {manobras_NOK_prog_dia}")



    with col2:
        st.markdown("<h3 style='text-align: center; color: gray;'>Emergenciais Diário</h3>", unsafe_allow_html=True)
        st.pyplot(fig5)
        st.info(f"Total: {manobras_total_emerg_dia}")
        st.success(f"Sucesso: {manobras_emerg_dia}")
        st.error(f"Insucesso: {manobras_NOK_emerg_dia}")



    with col3:
        st.markdown("<h3 style='text-align: center; color: gray;'>Programadas Mês</h3>", unsafe_allow_html=True)
        st.pyplot(fig4)
        st.info(f"Total: {manobras_total_prog_mes}")
        st.success(f"Sucesso: {manobras_prog_mes}")
        st.error(f"Insucesso: {manobras_NOK_prog_mes}")


    with col4:
        st.markdown("<h3 style='text-align: center; color: gray;'>Emergenciais Mês</h3>", unsafe_allow_html=True)
        st.pyplot(fig6)
        st.info(f"Total: {manobras_total_emerg_mes}")
        st.success(f"Sucesso: {manobras_emerg_mes}")
        st.error(f"Insucesso: {manobras_NOK_emerg_mes}")

     



    
    st.divider()
    # Mudando o status da coluna FECHAMENTO em vazio para aguardando status
    df_filtrado_data.loc[:, 'FECHAMENTO'] = df_filtrado_data['FECHAMENTO'].fillna("Status em Atualização")

    # Publicação do df
    st.write(df_filtrado_data.to_html(escape=False, index=False), unsafe_allow_html=True)


        


else:
    st.error("Não existem manobras para essa data!")


# Informações de atualização no arquivo do mês vigente
# mes_hoje = datetime.today().strftime('%Y_%m')
# df2 = pd.read_csv(f"/home/wanderson/API/diario_de_bordo/GMUD_{mes_hoje}_REL.XLS.csv", on_bad_lines='skip', encoding="latin-1")
# df2 = df2.columns[0]
# df2 = str(df2)
# st.info(f"Última {df2}", icon="ℹ️")