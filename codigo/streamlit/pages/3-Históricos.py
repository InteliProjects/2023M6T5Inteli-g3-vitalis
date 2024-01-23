# Importa as bibliotecas necessárias
import streamlit as st
import pandas as pd
import time
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
import html


def grafico_barras(funcionario_por_setor, demanda_por_setor):
    """
    Generate a grouped bar chart showing excess/shortage of technicians by sector.

    Parameters:
        - funcionario_por_setor (list): List of technician counts by sector.
        - demanda_por_setor (list): List of demand counts by sector.
    """
    indices_setores = np.arange(len(funcionario_por_setor))

    largura_barra = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    diferenca_por_setor = []
    for i in range(len(funcionario_por_setor)):
        valor_funcionario = int(funcionario_por_setor[i])
        valor_demanda = int(demanda_por_setor[i])
        diferenca_por_setor.append(2 * valor_funcionario - valor_demanda)

    barra_diferenca = ax.bar(indices_setores + largura_barra,
                             diferenca_por_setor, largura_barra, label='Excesso/Falta')

    for bar in barra_diferenca:
        if bar.get_height() < 0:
            bar.set_color('red')

    ax.axhline(0, color='black', linewidth=1)
    ax.set_xlabel('Setor')
    ax.set_ylabel('Excesso/Falta')
    ax.set_title('Excesso/Falta de técnicos por setor')
    ax.set_xticks(indices_setores + largura_barra / 2)
    ax.set_xticklabels([str(i) for i in indices_setores])
    ax.legend()

    st.pyplot(fig)


def convert_date(date_str):
    """
    Convert a date string to a specific format.

    Parameters:
        - date_str (str): Date string to be converted.

    Returns:
        - str: Converted date string.
    """

    date_object = datetime.datetime.strptime(
        date_str, "%a, %d %b %Y %H:%M:%S %Z")
    return date_object.strftime("%Y-%m-%d %H:%M")


def extract_values(row):
    """
    Extract specific values from a DataFrame row.

    Parameters:
        - row (pd.Series): Row of the DataFrame.

    Returns:
        - dict: Extracted values.
    """

    setor_origem = html.unescape(row["Setor origem"].split(":")[1].strip())
    setor_destino = html.unescape(row["Setor destino"].split(":")[1].strip())
    tecnicos_transferidos = html.unescape(
        row["Técnicos transferidos"].split(":")[1].strip())

    return {
        "Setor origem": setor_origem,
        "Setor destino": setor_destino,
        "Técnicos transferidos": tecnicos_transferidos,
    }


def dataFrame_(deslocamento_strings):
    """
    Create a DataFrame from shift data.

    Parameters:
        - deslocamento_strings (list): List of shift data strings.

    Returns:
        - pd.DataFrame: Created DataFrame.
    """
    dados_transacoes = []
    for i in deslocamento_strings:
        dados_transacao = {
            "Setor origem": i[0],
            "Setor destino": i[1],
            "Técnicos transferidos": i[2],
        }
        dados_transacoes.append(dados_transacao)

    df_transacoes = pd.DataFrame(dados_transacoes)

    dados_transacao = df_transacoes.apply(extract_values, axis=1)
    dados_transacao_lista = dados_transacao.tolist()
    df_transacoes = pd.DataFrame(dados_transacao_lista)

    return df_transacoes


def get_history():
    """
    Get historical data from an API.

    Returns:
        - dict: Historical data.
    """

    url_get = "http://127.0.0.1:5000/api/historico"
    historico = requests.get(url_get)
    json_data = historico.json()

    data = {'Date': [],
            'Quantidade de tecnicos': [],
            'Quantidade de demandas': [],
            'array_demandas': [],
            'array_tecnicos': [],
            'Deslocamento': [],
            'Cidade': [],
            'Custo reduzido': []
            }

    for entry in json_data["historico"]:
        index = entry[0] - 1

        while len(data['Date']) <= index:
            data['Date'].append('null')
            data['Quantidade de demandas'].append('null')
            data['Quantidade de tecnicos'].append('null')
            data['array_demandas'].append('null')
            data['array_tecnicos'].append('null')
            data['Deslocamento'].append('null')
            data['Cidade'].append('null')
            data['Custo reduzido'].append('null')

        data['Date'][index] = convert_date(entry[1])
        data['Quantidade de demandas'][index] = entry[2]
        data['Quantidade de tecnicos'][index] = entry[3]
        data['array_demandas'][index] = entry[4]
        data['array_tecnicos'][index] = entry[5]
        data['Deslocamento'][index] = entry[6]
        data['Cidade'][index] = entry[7]
        data['Custo reduzido'][index] = entry[8]

    return data


def tratamento_table(df):
    df = pd.DataFrame(df)
    df = df.replace("null", np.nan)
    df = df.dropna(axis=0, how="any")
    df.sort_index(inplace=True, ascending=False)
    df = df.astype({"Quantidade de demandas": int,
                   "Quantidade de tecnicos": int, "Custo reduzido": int})
    return df


st.set_page_config(
    page_title="Históricos",
    page_icon="📊",
    layout="wide",  # Para estender o fundo dourado à largura da tela
)

st.markdown('''
<style>
    .css-1oe5cao.e1fqkh3o9 {
        /* Adicione aqui suas regras de estilo CSS */
        padding-top: 3rem;
    }
</style>
''', unsafe_allow_html=True)

st.sidebar.image("assets/logo.png", use_column_width=True)

df = tratamento_table(get_history())
print(df.columns)


def delete_rows(selected_rows):
    """
    Delete selected rows.

    Parameters:
        - selected_rows (int): Index of selected rows.
    """
    global df
    linha_bd = selected_rows + 1
    df = df.drop(index=selected_rows).reset_index(drop=True)
    url_get = f"http://127.0.0.1:5000/api/historico/{linha_bd}"
    delete_otimizacao = requests.delete(url_get)
    df = pd.DataFrame(get_history())
    df = df.replace("null", np.nan)
    df = df.dropna(axis=0, how="any")


def main():
    """
    Main function to display the Streamlit app.
    """

    st.title("Página de históricos")
    st.write(
        "Confira todas as otimizações passadas, filtrando por datas e vendo seus resultados.")

    try:
        selected_date = st.selectbox(
            "Selecione um index a partir da tabela", df.index)
        selected_row = df[df.index == selected_date].iloc[0]
        expander = st.expander(f"Detalhes de {selected_row['Date']}")
        with expander:
            deslocamento_df = dataFrame_((selected_row['Deslocamento']))
            st.write(f"Deslocamento: ")
            st.table(deslocamento_df)
            st.write(f"Gráfico: ")
            grafico_barras(
                (selected_row["array_tecnicos"]), (selected_row["array_demandas"]))
    except:
        st.error("Nenhum resultado encontrado!")

    selected_rows = st.selectbox(
        'Deseja deletar alguma otimização? Selecione as linhas para excluir:', df.index)

    if st.button('Excluir otimizações'):
        delete_rows(selected_rows)
        st.success('Otimização excluída com sucesso.')

        time.sleep(1)
        # st.rerun()
    df_visualization = df[["Date", "Quantidade de demandas",
                           "Quantidade de tecnicos", "Cidade", "Custo reduzido"]]
    df_visualization.sort_index(inplace=True, ascending=False)
    st.table(df_visualization)


if __name__ == '__main__':
    main()
