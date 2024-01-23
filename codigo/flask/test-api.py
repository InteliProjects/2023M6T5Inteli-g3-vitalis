"""
This Python script uses the pytest and requests libraries to perform integration testing on a Flask API. The API is designed to manipulate data in a PostgreSQL database.

The URL of the API being tested is defined at the start of the script.

Each function in the script corresponds to a test case for a specific API endpoint and HTTP method:

- test_create() tests the POST method on the "/api/historico" endpoint.
- test_read() tests the GET method on the "/api/historico" endpoint.
- test_get_by_id() tests the GET method on the "/api/historico/<int:id>" endpoint.
- test_update() tests the PUT method on the "/api/historico/<int:id>" endpoint.
- test_delete() tests the DELETE method on the "/api/historico/<int:id>" endpoint.

Each test case makes a request to the API, checks the status code of the response, and (for POST, PUT, and DELETE methods) checks the message in the response body.
"""

import pytest
import requests

# The URL of the API you are testing
URL = "http://localhost:5000/api/historico"

# this test is break, do not uncomment because it can break our database
# def test_create():
#     """Tests the creation of a new record using the POST method."""
#     # Test data
#     data = {
#         "data": "2023-12-03",
#         "demandas": "{0, 0, 0, 1, 1, 1, 0, 1, 0, 1}",
#         "tecnicos":  "{0, 0, 0, 0, 0, 1, 1, 1, 0, 0}",
#     "otimizacao": [
#         "Setor de origem: Sem origem",
#         "Setor de destino: Sem destino",
#         "Tecnicos transferidos: Nao ha tecnicos suficientes para atender a todas as demandas"
#     ],    }
#     # Making the POST request
#     response = requests.post(URL, json=data)
#     # Checking the status code
#     assert response.status_code == 200
#     # Checking the message
#     assert response.json()["message"] == "Histórico criado"

def test_read():
    """Tests the reading of all records using the GET method."""
    # Making the GET request
    response = requests.get(URL)
    # Checking the status code
    assert response.status_code == 200

def test_get_by_id():
    """Tests the reading of a specific record by its id using the GET method."""
    # Test ID
    id_teste = 23
    # Making the GET request
    response = requests.get(f"{URL}/{id_teste}")
    # Checking the status code
    assert response.status_code == 200

# this test is break, do not uncomment because it can break our database
# def test_update():
#     """Tests the updating of a specific record using the PUT method."""
#     # Test ID
#     id_teste = 31
#     # Test data
#     data = {
#         "data": "2023-12-03",
#         "demandas": "{0, 0, 0, 1, 1, 1, 0, 1, 0, 1}",
#         "tecnicos":  "{0, 0, 0, 0, 0, 1, 1, 1, 2, 5}",
#         "otimizacao": [
#         "Setor de origem: Sem origem",
#         "Setor de destino: Sem destino",
#         "Tecnicos transferidos: Nao ha tecnicos suficientes para atender a todas as demandas"
#     ],    }
#     # Making the PUT request
#     response = requests.put(f"{URL}/{id_teste}", json=data)
#     # Checking the status code
#     assert response.status_code == 200
#     # Checking the message
#     assert response.json()["message"] == f"Histórico with id {id_teste} updated"

def test_delete():
    """Tests the deletion of a specific record using the DELETE method."""
    # Test ID
    id_teste = 33
    # Making the DELETE request
    response = requests.delete(f"{URL}/{id_teste}")
    # Checking the status code
    assert response.status_code == 200
    # Checking the message
    assert response.json()["message"] == f"Histórico with id {id_teste} deleted"