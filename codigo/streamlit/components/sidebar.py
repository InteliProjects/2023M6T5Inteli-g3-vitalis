import streamlit as st
import pandas as pd
import json
from shapely.geometry import Point, Polygon


def main():
    # Sidebar para upload de arquivos
    # coordenadas = st.sidebar.file_uploader("Faça upload dos Setores")
    # file_tecnicos = st.sidebar.file_uploader("Faça upload dos colaboradores")
    # file_demandas = st.sidebar.file_uploader("Faça upload das demandas")

    # value_tecnico_att_demanda= st.sidebar.number_input("Insira o custo de uma demanda ser atendida pelo técnico:")
    # value_tecnico_not_demanda= st.sidebar.number_input("Insira o custo de uma demanda não ser atendida pelo técnico:")

    # Chamadas para as funções principais
    make_setor(coordenadas)
    extract_demandas(file_tecnicos)
    extract_tecnicos(file_demandas)


def extract_demandas(file_demandas):
    # Tentativas de leitura com diferentes codificações
    codificacoes = ['utf-8', 'ISO-8859-1', 'cp1252', 'latin1']
    demand_dict = {}
    demand_setor = {}
    df_demandas = None  # Inicializa o DataFrame

    for cod in codificacoes:
        try:
            if file_demandas is not None:
                df_demandas = pd.read_csv(file_demandas, encoding=cod)
                break
        except UnicodeDecodeError:
            continue

    # Verifica se o DataFrame foi criado antes de iterar sobre ele
    if df_demandas is not None:
        for i, row in df_demandas.iterrows():
            demand_dict[f'd{i}'] = row.tolist()
        demand_list = list(demand_dict.keys())
        return demand_dict
    else:
        st.write("Não foi possível ler o arquivo com as codificações fornecidas.")

    # Cria um dicionário que associa demandas aos setores correspondentes
    for demand, valores in demand_dict.items():
        if len(valores) >= 6:
            setor = valores[5]
            if setor not in demand_setor:
                demand_setor[setor] = []
            demand_setor[setor].append(demand)

    json_demandas_por_setor = json.dumps(demand_setor, indent=4)
    parsed_json = json.loads(json_demandas_por_setor)
    formatted_json = json.dumps(parsed_json, indent=4)


def extract_tecnicos(file_tecnicos):
    if file_tecnicos is not None:
        # Leitura do arquivo e seleção das colunas desejadas
        partida = pd.read_csv(file_tecnicos)
        partida = partida[["Cidade", "Latitude", "Longitude"]]
        partida = partida[partida["Cidade"] == "Curitiba"]
        partida["Latitude"] = partida["Latitude"].apply(
            lambda lat: float(lat.replace(",", ".")))
        partida["Longitude"] = partida["Longitude"].apply(
            lambda lat: float(lat.replace(",", ".")))
        cidade = partida["Cidade"].max()
        return partida, cidade
    # else:
    #     st.write("Não foi possível ler o arquivo com as codificações fornecidas.")


def make_setor(coordenadas):
    # Verifica se o argumento coordenadas não é nulo
    if coordenadas is not None:
        # Verifica se o arquivo de coordenadas não está vazio
        if not coordenadas:
            st.sidebar.warning(
                "Nenhuma coordenada disponível para exibir setores.")
        # Chama a função para gerar os polígonos e o número de setores
        coordsT, nSetor, centroid = generate_square_polygon(coordenadas)
        return coordsT, nSetor, centroid
    else:
        # Avisa para fazer o upload do arquivo CSV se coordenadas for nulo
        st.warning("Faça o upload do arquivo CSV para exibir os setores.")


def generate_square_polygon(setor):
    # Lê o arquivo CSV com as coordenadas dos setores
    dataFrame = pd.read_csv(setor)
    linha = 0
    polygons = []

    # Obtém o número total de linhas para iteração
    for i in dataFrame["setor"]:
        linha += 1

    nLinhas = int(dataFrame.iloc[linha-1][3])

    # Itera sobre os setores para criar os polígonos
    for i in range(0, nLinhas + 1):
        subset = dataFrame[dataFrame['setor'] == i]
        polygon_coords = []
        # Obtém as coordenadas para o polígono do setor atual
        for index, row in subset.iterrows():
            polygon_coords.append([row['lon'], row['lat']])

        if polygon_coords:
            polygons.append(polygon_coords)

            centro = [sum(x[0] for x in polygon_coords) / len(polygon_coords),
                      sum(x[1] for x in polygon_coords) / len(polygon_coords)]

    # Obtém o número total de setores
    nSetor = dataFrame["setor"].unique().size

    return polygons, nSetor, centro


def contido(polygons, partida):
    func = partida
    latF = func["Latitude"].to_list()
    lonF = func["Longitude"].to_list()
    coordenadas = Polygon(polygons)

    # Itera sobre os polígonos e as coordenadas de partida para verificar a inclusão
    for i in polygons:
        for j in len(latF):
            point = Point(latF[j], lonF[j])
            is_inside = coordenadas.contains(point)
            print(is_inside)


if __name__ == "__main__":
    main()
