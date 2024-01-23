# Importing necessary modules and functions
import pandas as pd
import json
import streamlit as st

# Function to calculate the cost before applying the algorithm
def calculate_cost_pre_algorithm(array_demandas_old, array_tecnicos_old):
    # Define the cost of attended and unattended demands
    cost_demand_att= 60
    cost_demand_not_att= 80
    remaining_demands = []
    attended_demands= []
    # Calculate the remaining and attended demands for each technician
    for technicians, demands in zip(array_tecnicos_old, array_demandas_old):
        remaining = demands - (2 * technicians)
        if remaining < 0:
            remaining= 0
        remaining_demands.append(remaining)

        attended= demands - remaining
        if attended < 0:
            attended= 0
        attended_demands.append(attended)
        
    # Calculate the total cost of attended and unattended demands
    value_demand_not_att= sum(remaining_demands) * cost_demand_not_att
    value_demand_att= sum(attended_demands) * cost_demand_att

    # Calculate the total cost before applying the algorithm
    total_cost_pre_algorithm= value_demand_att + value_demand_not_att

    return total_cost_pre_algorithm

# Function to create an array of technicians after applying the algorithm
def create_array_tecnicos_post_algorithm(array_tecnicos_old,  array_setor_origem, array_setor_destino, array_moved_tecnicos):
    array_tecnicos_post_algorithm= array_tecnicos_old.copy()

    # Update the array of technicians based on the technicians transferred
    for i in range(len(array_setor_origem)):
        setor_origin= array_setor_origem[i]
        setor_destino= array_setor_destino[i]
        tecnicos_transferidos= array_moved_tecnicos[i]

        array_tecnicos_post_algorithm[setor_origin - 1] -= tecnicos_transferidos
        array_tecnicos_post_algorithm[setor_destino - 1] += tecnicos_transferidos
    
    return array_tecnicos_post_algorithm

# Function to calculate the cost after applying the algorithm
def calculate_cost_post_algorithm(array_demandas_old, array_tecnicos_post_algorithm):
    cost_demand_att= 60
    attended_demands= []

    # Calculate the attended demands for each technician
    for technicians, demands in zip(array_tecnicos_post_algorithm, array_demandas_old):
        remaining = demands - (2 * technicians)
        if remaining < 0:
            remaining= 0

        attended= demands - remaining
        if attended < 0:
            attended= 0

        attended_demands.append(attended)
    
    # Calculate the total cost of attended demands
    value_demand_att= sum(attended_demands) * cost_demand_att

    # Calculate the total cost after applying the algorithm
    total_cost_post_algorithm = value_demand_att

    return total_cost_post_algorithm
