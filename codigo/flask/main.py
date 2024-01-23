"""
This Python script is a Flask application that provides an API for manipulating data in a PostgreSQL database. 
It uses the psycopg2 library to interact with PostgreSQL and the dotenv library to load environment variables.

Database operations are performed using SQL queries that are defined as constants at the start of the script.

The Flask application defines several routes that correspond to different database operations:

- The "/" route returns a welcome message.
- The "/api/historico" route supports POST methods to create a new record and GET to read all records.
- The "/api/historico/<int:id>" route supports GET, PUT, and DELETE methods to read, update, and delete a specific record, respectively.

Each route calls a function that performs the appropriate database operation.

The script also includes a commented '/test_db' route that can be used to test the database connection.
"""

import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
import datetime
from zoneinfo import ZoneInfo
import pytz

# Defining SQL queries
INSERT_VALUES_HISTORICO= (
    "INSERT INTO historico(data, demandas, tecnicos, demandas_setor, tecnicos_setor, otimizacao, cidade, custo_reduzido) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_historico;"
)
GET_VALUES_HISTORICO = (
    "SELECT * FROM historico"
)
GET_VALUES_HISTORICO_BY_ID = (
    "SELECT * FROM historico WHERE id_historico = %s"
)
UPDATE_VALUES_HISTORICO = (
    "UPDATE historico SET data = %s, demandas = %s, tecnicos = %s, demandas_setor = %s, tecnicos_setor = %s, otimizacao = %s, cidade = %s, custo_reduzido= %s WHERE id_historico = %s"
)
DELETE_VALUES_HISTORICO = (
    "DELETE FROM historico WHERE id_historico = %s"
)

# Loading environment variables
load_dotenv()

# Initializing the Flask application
app = Flask(__name__)
url= os.getenv("DATABASE_URL")
connection= psycopg2.connect(url)

@app.get("/")
def home():
    """Returns a welcome message."""
    return "Hello World" 

@app.post("/api/historico")
def create():
    """Creates a new record in the database with the data received in the request body."""
    req= request.get_json()
    date= datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
    demand= req["demandas"]
    tecnic= req["tecnicos"]
    demand_setor= req["demandas_setor"]
    tecnic_setor= req["tecnicos_setor"]
    otimizacao= req["otimizacao"]
    cidade= req["cidade"]
    custo_reduzido= req["custo_reduzido"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VALUES_HISTORICO, (date, demand, tecnic, demand_setor, tecnic_setor, otimizacao, cidade, custo_reduzido))
            id_historico= cursor.fetchone()[0]
    return {"id": id_historico, "message": f"Histórico criado"}, 200

@app.get("/api/historico")
def read():
   """Reads all records from the database."""
   with connection:
       with connection.cursor() as cursor:
           cursor.execute(GET_VALUES_HISTORICO)
           historico = cursor.fetchall()
   return {"historico": historico}, 200

@app.get("/api/historico/<int:id>")
def get_by_id(id):
   """Reads a specific record from the database by its id."""
   with connection:
       with connection.cursor() as cursor:
           cursor.execute(GET_VALUES_HISTORICO_BY_ID, (id,))
           historico = cursor.fetchone()
   if historico is None:
       return {"message": f"Histórico with id {id} not found"}, 404
   else:
       return {"historico": historico}, 200

@app.put("/api/historico/<int:id>")
def update(id):
   """Updates a specific record in the database with the data received in the request body."""
   req = request.get_json()
   date= datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
   demand = req["demandas"]
   tecnic = req["tecnicos"]
   demand_setor = req["demandas_setor"]
   tecnic_setor = req["tecnicos_setor"]
   otimizacao = req["otimizacao"]
   cidade= req["cidade"]
   custo_reduzido= req["custo_reduzido"]

   with connection:
       with connection.cursor() as cursor:
           cursor.execute(UPDATE_VALUES_HISTORICO, (date, demand, tecnic, demand_setor, tecnic_setor, otimizacao, cidade, custo_reduzido, id))
   return {"message": f"Histórico with id {id} updated"}, 200

@app.delete("/api/historico/<int:id>")
def delete(id):
   """Deletes a specific record from the database by its id."""
   with connection:
       with connection.cursor() as cursor:
           cursor.execute(DELETE_VALUES_HISTORICO, (id,))
   return {"message": f"Histórico with id {id} deleted"}, 200