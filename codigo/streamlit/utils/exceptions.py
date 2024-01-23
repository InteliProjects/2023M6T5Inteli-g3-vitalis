from utils.parser import converter_para_array
import requests, json
import pandas as pd


def send_post(demandas, tecnicos, result,cidade, reduced_cost_post_algorithm):
    """
    Sends error information to a specified API endpoint.

    Parameters:
    - demandas (list): List of demands associated with the error.
    - tecnicos (list): List of technicians associated with the error.
    - result (str): Result or error message to be sent.

    Returns:
    - requests.Response: The response object from the API endpoint.
    """
    url = "http://127.0.0.1:5000/api/historico"
    demandas_setor=converter_para_array(demandas)
    tecnicos_setor=converter_para_array(tecnicos)
    demandas = int(sum(demandas))
    tecnicos = int(sum(tecnicos))
    result = converter_para_array(result)

    obj = {"demandas": demandas,
           "tecnicos": tecnicos,"demandas_setor":f"{demandas_setor}","tecnicos_setor":f"{tecnicos_setor}", "otimizacao": result, "cidade": f"{cidade}", "custo_reduzido": reduced_cost_post_algorithm}
    print(obj)
    post = requests.post(url, json=obj)
    print(post)
    return post


def error_post(demandas, tecnicos, result,cidade, reduced_cost_post_algorithm):
    """ This function is responsible for handling errors in optimization 
    and sending it to the backend"""
    array = []
    url = "http://127.0.0.1:5000/api/historico"
    demandas_setor=converter_para_array(demandas)
    tecnicos_setor=converter_para_array(tecnicos)
    demandas = int(sum(demandas))
    tecnicos = int(sum(tecnicos))


    Json_error = {"Setor de origem": "Sem origem",
                  "Setor de destino": "Sem destino", 'Tecnicos transferidos': f'{result}'}
    array.append(Json_error)

    resultado = json.dumps(array)

    resultado = converter_para_array(resultado)
    obj = {"demandas": demandas,
           "tecnicos": tecnicos,"demandas_setor":f"{demandas_setor}","tecnicos_setor":f"{tecnicos_setor}", "otimizacao": f"{resultado}", "cidade": f"{cidade}", "custo_reduzido": reduced_cost_post_algorithm}
    post = requests.post(url, json=obj)
    print(post)
    return post
