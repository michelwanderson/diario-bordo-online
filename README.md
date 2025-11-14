# Painel de Controle de Manobras - Diário de Bordo

Este projeto consiste em um painel de controle para o acompanhamento de manobras (tickets), com coleta automatizada de dados, organização e visualização estatística.

## Visão Geral

O sistema automatiza a coleta de dados de tickets de manobras de um determinado servidor, organiza esses dados em um formato utilizável e apresenta um painel de controle interativo através do Streamlit.

## Funcionalidades

-   **Coleta Automatizada de Dados:** Extrai informações de tickets de manobras de um site especificado.
-   **Organização de Dados:** Filtra e organiza os dados coletados, preparando-os para análise.
-   **Painel de Controle Interativo:** Apresenta os dados de forma visual e interativa através de um painel Streamlit.
-   **Visualização Estatística:** Exibe gráficos de indicadores chave relacionados às manobras/tickets.

## Arquitetura

O projeto é composto pelos seguintes arquivos:

-   `coletando.py`: Responsável pela coleta de dados do site de manobras, salvando-os inicialmente em um arquivo `GMUD_<ANO>_<MES>_REL.XLS.csv` e, em seguida, filtrando e consolidando os dados em `gmud_rel.csv`.
-   `diario.py`: Arquivo principal que executa o painel de controle interativo utilizando Streamlit.
-   `estatisticas.py`: Implementa a lógica para gerar gráficos e visualizações estatísticas a partir dos dados das manobras.

## Configuração

### Pré-requisitos

-   Python 3.6+
-   Bibliotecas: pandas, Streamlit, requests, beautifulsoup4 (e outras dependências utilizadas nos scripts)

### Instalação

1.  Clone o repositório:

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <DIRETORIO_DO_PROJETO>
    ```
2.  Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

### Configuração do Ambiente

1.  **Agendamento da Coleta de Dados:**

    Configure um cron job para executar o script `coletando.py` a cada hora. Isso garante que o relatório de manobras seja atualizado regularmente.

    ```bash
    0 * * * * python3 /caminho/para/coletando.py
    ```

2.  **Arquivo `.env`:**

    Crie um arquivo `.env` na raiz do projeto e configure as seguintes variáveis:

    ```
    URL_SERVIDOR="<URL_DO_SERVIDOR_DE_MANOBRAS>"
    DIRETORIO_PROJETO="<DIRETORIO_LOCAL_DOS_ARQUIVOS_DO_PROJETO>"
    ```

    Substitua `<URL_DO_SERVIDOR_DE_MANOBRAS>` pela URL do servidor onde os tickets de manobras são registrados e `<DIRETORIO_LOCAL_DOS_ARQUIVOS_DO_PROJETO>` pelo caminho absoluto para a pasta do projeto no seu sistema.

### Execução

Para iniciar o painel de controle, execute o seguinte comando:

```bash
streamlit run /caminho/para/diario.py --server.port=6510
```


Abra o navegador e acesse `http://localhost:6510` para visualizar o painel.

### Detalhes Importantes
Dicionário de Cidades: Verifique o dicionário de nomes de cidades no arquivo coletando.py para garantir que todos os nomes de cidades estejam no mesmo padrão utilizado no site de manobras/tickets.


### Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias, correções de bugs e novas funcionalidades.