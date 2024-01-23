from utils.datatypes import Sector, SolutionType, Solution, Transaction
from utils.exceptions import send_post, error_post
from utils.location import make_matrix
from utils.reduced_cost import calculate_cost_pre_algorithm, create_array_tecnicos_post_algorithm, calculate_cost_post_algorithm


import pandas as pd
import json
import streamlit as st


def evaluate_scores(sectors: list[Sector]) -> SolutionType:
    """This function is used to decide the best course of action when receiving a problem.
    :param sectors: List of sectors.
    :return: The type of the solution that should be returned.
    """
    receiver_sectors: list[Sector] = list(
        filter(lambda setor: setor.score < 0, sectors))

    if len(receiver_sectors) == 0:
        return SolutionType.DONE

    if sum(setor.score for setor in sectors) < 0:
        return SolutionType.UNFEASIBLE

    return SolutionType.SUBOPTIMAL


def algorithm(sectors: list[Sector]) -> tuple[Solution, float]:
    """This function is  used to run the whole greedy algorithm for the allocation problem.
    :param sectors: List of sectors.
    :return: Best solution in the form of a list of transactions and the cost of the solution.
    """
    receiver_sectors: list[Sector] = list(
        filter(lambda setor: setor.score < 0, sectors))
    sender_sectors: list[Sector] = list(
        filter(lambda setor: setor.score > 0, sectors))

    cost: float = 0

    if evaluate_scores(sectors) == SolutionType.SUBOPTIMAL:
        return_solution: Solution = []

        while len(receiver_sectors) > 0:
            receiver_sector: Sector = receiver_sectors[0]
            sender_sectors.sort(
                key=lambda sector: sector.distances[receiver_sector.id_number])
            index: int = 0
            while receiver_sector.score < 0:
                sender_sector: Sector = sender_sectors[index]
                counter: int = sender_sector.transfer(receiver_sector)
                if counter > 0:
                    transaction: Transaction = Transaction.constructor_with_amount(sender_sector,
                                                                                   receiver_sector,
                                                                                   counter
                                                                                   )
                    cost += sender_sector.distances[receiver_sector.id_number] * counter
                    return_solution.append(transaction)
                index += 1
            receiver_sectors.remove(receiver_sector)
        return return_solution, cost
    elif evaluate_scores(sectors) == SolutionType.DONE:
        return "Done", "Done"
    elif evaluate_scores(sectors) == SolutionType.UNFEASIBLE:
        return "Unfeasible", "Unfeasible"
    elif len(sender_sectors) < len(receiver_sectors):
        raise ValueError(
            'There are no feasible solutions available for this problem')
    elif sum(sector.score for sector in sender_sectors) == sum(sector.score for sector in receiver_sectors):
        raise ValueError('This is already a feasible solution.')

def calculate_reduced_cost(array_demandas, tecnicos, setor_origem, setor_destino, tecnicos_transferidos):
    new_array_tecnicos_post_algorithm= []
    calculate_cost_pre_algorithm(array_demandas, tecnicos)
    new_array_tecnicos_post_algorithm= create_array_tecnicos_post_algorithm(tecnicos, setor_origem, setor_destino, tecnicos_transferidos)
    calculate_cost_post_algorithm(array_demandas, new_array_tecnicos_post_algorithm)
            
    reduced_cost_post_algorithm= calculate_cost_pre_algorithm(array_demandas, tecnicos) - calculate_cost_post_algorithm(array_demandas, new_array_tecnicos_post_algorithm)
    return reduced_cost_post_algorithm

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


def otimizar(demanda_por_setor, funcionario_por_setor, cidade):
    """
    Perform optimization.

    Parameters:
    - demanda_por_setor: Demand data by sector.
    - funcionario_por_setor: Technician data by sector.
    """
    try:
        tecnicos = funcionario_por_setor
        demandas = demanda_por_setor
        array_demandas = demanda_por_setor

        greedy_problem = []
        matriz_distancias = make_matrix(
            "./pages/file.csv")
        for idx, (funcionarios, demandas) in enumerate(zip(tecnicos, demandas)):

            distances_column = matriz_distancias.iloc[:, idx].tolist()
            sector = Sector(id_number=idx, demands=demandas,
                            workers=funcionarios, distances=distances_column)

            greedy_problem.append(sector)

        greedy_resultado, _ = algorithm(greedy_problem)

        dados_transacoes = []
        if greedy_resultado != "Done" and greedy_resultado != "Unfeasible":
            for transaction in greedy_resultado:
                # st.write(transaction)
                sender_sector = transaction.sender_sector.id_number
                receiver_sector = transaction.receiver_sector.id_number
                amount = transaction.amount
                # Cria um dicionário com os dados da transação
                dados_transacao = {
                    "Setor origem": sender_sector,
                    "Setor destino": receiver_sector,
                    "Técnicos transferidos": amount,
                }

                # Adiciona o dicionário à lista de dados das transações
                dados_transacoes.append(dados_transacao)

            solution = json.dumps(dados_transacoes)
            
            setor_origem = []
            setor_destino = []
            tecnicos_transferidos = []

            for transacao in dados_transacoes:
                setor_origem.append(transacao['Setor origem'])
                setor_destino.append(transacao['Setor destino'])
                tecnicos_transferidos.append(transacao['Técnicos transferidos'])
            df_transacoes = pd.DataFrame(dados_transacoes)

          


            new_array_tecnicos_post_algorithm= []

            calc_cost_pre_algorithm= calculate_cost_pre_algorithm(array_demandas, tecnicos)
            new_array_tecnicos_post_algorithm= create_array_tecnicos_post_algorithm(tecnicos, setor_origem, setor_destino, tecnicos_transferidos)

            calc_cost_post_algorithm= calculate_cost_post_algorithm(array_demandas, new_array_tecnicos_post_algorithm)
            reduced_cost_post_algorithm= calculate_reduced_cost(array_demandas, tecnicos, setor_origem, setor_destino, tecnicos_transferidos)

            print("A reducao de custo foi de", reduced_cost_post_algorithm)
            post_para_bd = send_post(array_demandas, tecnicos, solution,cidade, reduced_cost_post_algorithm)

            # Exibe a tabela
            st.table(df_transacoes)

            st.write("Custo demandas atendidas antes do algoritmo:", f'${str(calc_cost_pre_algorithm)}')
            st.write("Custo demandas atendidas depois do algoritmo:", f'${str(calc_cost_post_algorithm)}')
            st.write("Custo total reduzido:", f'$${str(reduced_cost_post_algorithm)}')


            st.download_button(
                "Exportar",
                convert_df(df_transacoes),
                "otimizacao.csv",
                "text/csv",
                key='download-csv'
            )
            st.write('Nota: ao exportar a página será recarregada. Mas é possível observar novamente os resultados da otimização na página de históricos.')

        elif greedy_resultado == "Done":
            st.write("A configuração atual já atende a todas as demandas")
            solution_done = "A configuracao atual ja atende a todas as demandas"
            calc_cost_pre_algorithm= calculate_cost_pre_algorithm(array_demandas, tecnicos)
            st.write("Custo demandas atendidas antes do algoritmo:", f'${str(calc_cost_pre_algorithm)}')
            error_post(array_demandas, tecnicos, solution_done, cidade, 0.0)
        elif greedy_resultado == "Unfeasible":
            st.write("Não há técnicos suficientes para atender a todas as demandas")
            solution_unfeasible = "Nao ha tecnicos suficientes para atender a todas as demandas"
            calc_cost_pre_algorithm= calculate_cost_pre_algorithm(array_demandas, tecnicos)
            st.write("Custo demandas atendidas antes do algoritmo:", f'${str(calc_cost_pre_algorithm)}')
            error_post(array_demandas, tecnicos, solution_unfeasible, cidade, 0.0)

    except ValueError as ve:
        if 'no feasible solutions' in str(ve):
            st.write("Não há soluções viáveis disponíveis para este problema.")

        elif 'already a feasible solution' in str(ve):
            st.write("Esta já é uma solução viável.")
        else:
            st.write(
                f"Erro na otimização: {ve}. Tente recarregar a página e rodar a otimização novamente")

    except Exception as e:
        st.write(f"Erro desconhecido: {e}")
