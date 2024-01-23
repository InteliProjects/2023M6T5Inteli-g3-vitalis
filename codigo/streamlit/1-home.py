# Importando a biblioteca Streamlit
import streamlit as st
from components.sidebar import main as sidebar


def main() -> None:
    # Configurando as opções da página
    st.set_page_config(
        page_title="Vitalis",
        page_icon="📊",
        layout="wide",  # Para estender o fundo dourado à largura da tela
    )

    # Adicionando estilos CSS à página
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

    # Adicionando imagem do logotipo na barra lateral
    st.sidebar.image("assets/logo.png", use_column_width=True)
    # sidebar()

    # Adicionando texto de boas-vindas
    st.title("Bem-vindo(a)")

    # Adicionando texto de boas-vindas
    st.markdown(
        """
        Imagine gerenciar a complexa distribuição de técnicos da V.Tal de forma simplificada e eficiente. 
        Vitalis é a resposta. Um algoritmo inteligente desenvolvido para superar os desafios associados à alocação dinâmica de recursos.

        A tarefa de alocar técnicos é complicada, especialmente quando a dinâmica do cenário muda com frequência.

        O algoritmo da Vitalis busca minimizar deslocamentos entre setores ao considerar o custo operacional associado a cada movimentação de técnico. 
        Procuramos uma configuração que reduza custos, mantendo a eficiência na distribuição.

        Nossa plataforma fornece análises detalhadas da eficiência da distribuição, incluindo visualizações gráficas. 
        Isso permite que os gestores tomem decisões informadas sobre a distribuição de recursos, ajustando conforme necessário.

        A Vitalis é a resposta para simplificar a complexa tarefa de distribuição de técnicos, proporcionando uma gestão mais eficaz e eficiente em ambientes em constante evolução.
        """
    )


if __name__ == "__main__":
    main()
