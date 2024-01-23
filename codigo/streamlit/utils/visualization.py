import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def grafico_barras(funcionario_por_setor, demanda_por_setor):
    """
    Create a grouped bar chart showing the excess/shortage of technicians per sector.

    Parameters:
    - funcionario_por_setor (list[int]): List of technicians per sector.
    - demanda_por_setor (list[int]): List of demands per sector.
    """
    st.write("Funcionários: " + str(sum(funcionario_por_setor)) +
             "; Demandas: " + str(sum(demanda_por_setor)))
    indices_setores = np.arange(len(funcionario_por_setor))

    largura_barra = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    diferenca_por_setor = []
    for i in range(len(funcionario_por_setor)):
        diferenca_por_setor.append(
            2*funcionario_por_setor[i] - demanda_por_setor[i])

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
