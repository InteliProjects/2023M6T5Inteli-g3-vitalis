import os

import pandas as pd
from shapely import Point, Polygon
from components.sidebar import make_setor, extract_tecnicos, extract_demandas
from utils.visualization import grafico_barras
from utils.algorithm import otimizar
from streamlit_folium import folium_static
import streamlit as st
import folium


def main():
    """
    Main function to display the Streamlit app.
    It adds page configuration, css styling and streamlit components, such as tables,
    graphs and maps.
    """
    # Configurando as opções da página
    st.set_page_config(
        page_title="Otimizador",
        page_icon="📊",
        layout="wide",  # Para estender o fundo dourado à largura da tela
    )

    on_off = True
    funcionario_por_setor_definitivo = []
    demanda_por_setor_definitivo = []

    st.markdown('''
    <style>
        .css-1oe5cao.e1fqkh3o9 {
            /* Adicione aqui suas regras de estilo CSS */
            padding-top: 3rem;
        }
        # .css-1ik2ge {
        #     background-color: rgb(0, 84, 163);
        # }
    </style>
    ''', unsafe_allow_html=True)

    st.sidebar.image("assets/logo.png", use_column_width=True)

    st.sidebar.title("Vitalis")

    setor = st.sidebar.file_uploader("Faça upload da localização dos setores")
    colaboradores = None
    demandas = None

    # Display the map accordingly with csv location

    m = folium.Map(location=[-15.7801, -47.9292],
                   zoom_start=11, tiles="Cartodb Positron")

    if setor is not None:
        colaboradores = st.sidebar.file_uploader(
            "Faça upload do ponto de partida colaboradores")
        # Get the current position of the cursor
        current_position = setor.tell()

        # Read the content of the uploaded file
        coordenadas, nSetor, centro = make_setor(setor)

        m = folium.Map(location=centro,
                       zoom_start=11, tiles="Cartodb Positron")

        # Seek back to the original position before writing to the file
        setor.seek(current_position)

        # Specify the output file path relative to the script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file_path = os.path.join(script_dir, "file.csv")

        # Open the output file in write mode and write the content
        with open(output_file_path, "wb") as output_file:
            output_file.write(setor.read())
        for i, index in enumerate(coordenadas, start=0):
            folium.Polygon(locations=index, color='blue', fill=True, smooth_factor=2, fill_color='blue',
                           popup=folium.Popup(f"Área {i}", parse_html=True), tooltip=f"Setor {i}").add_to(m)

        if not coordenadas:
            st.sidebar.warning(
                "Nenhuma coordenada disponível para exibir setores.")

    if colaboradores is not None:
        demandas = st.sidebar.file_uploader("Faça upload das demandas")
        func, cidade = extract_tecnicos(colaboradores)
        latF = func["Latitude"].to_list()
        lonF = func["Longitude"].to_list()
        funcionarios = []
        matrix = coordenadas

        for funcionario in range(len(latF)):
            novo_funcionario = Point(latF[funcionario], lonF[funcionario])
            funcionarios.append(novo_funcionario)

        funcionario_por_setor = [0] * len(matrix)
        for i in range(len(funcionarios)):
            for j in range(len(matrix)):
                if Polygon(matrix[j]).contains(funcionarios[i]):
                    funcionario_por_setor[j] += 1
        funcionario_por_setor_definitivo = funcionario_por_setor

        for i in range(len(latF)):
            folium.Circle(location=[latF[i], lonF[i]], radius=2,
                          color='yellow', fill=True, fill_color='yellow').add_to(m)

        if not colaboradores:
            st.sidebar.warning(
                "Nenhuma colaborador disponível para exibir setores.")

    if demandas is not None:
        df1 = extract_demandas(demandas)
        lon = [df1[i][15] for i in df1.keys()]
        lat = [df1[i][14] for i in df1.keys()]
        demandas = []
        matrix = coordenadas

        for demanda in range(len(lat)):
            nova_demanda = Point(lat[demanda], lon[demanda])
            demandas.append(nova_demanda)

        demanda_por_setor = [0] * len(matrix)
        for i in range(len(demandas)):
            for j in range(len(matrix)):
                if Polygon(matrix[j]).contains(demandas[i]):
                    demanda_por_setor[j] += 1
        demanda_por_setor_definitivo = demanda_por_setor

        for i in range(len(lon)):
            folium.Circle(location=[lat[i], lon[i]], radius=2,
                          color='red', fill=True, fill_color='red').add_to(m)

        if not demandas:
            st.sidebar.warning("Nenhuma demanda disponível para os setores.")
        on_off = False
    col1, col2 = st.columns([2, 0.9])

    st.markdown('''
    <style>
        .css-z5fcl4 {
            padding: 2rem 2rem 2rem;
        }
    </style>
    ''', unsafe_allow_html=True)

    with col1:
        st.header("Mapa Técnicos x Demandas")
        st.write("Adicione os arquivos para observar")
        folium_static(m, width=920, height=600)

    with col2:
        st.header("Resultados")
        st.write("Observe aqui os resultados da otimização")

        if st.sidebar.button("Otimizar", disabled=on_off):
            grafico_barras(funcionario_por_setor_definitivo,
                           demanda_por_setor_definitivo)
            otimizar(demanda_por_setor_definitivo,
                     funcionario_por_setor_definitivo, cidade)


if __name__ == "__main__":
    main()
