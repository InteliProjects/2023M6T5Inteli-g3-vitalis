from requests import Response
from pandas import DataFrame
from utils.geometry import get_region_centers
from utils.parser import mount_request
import json
import requests
import pandas as pd


def get_distance_matrix(url: str) -> list:
    """ This function is used to get the distance matrix by using a API query URL.
    :param url: Proper OSRM "https://[instance]/table/v1/driving/[semicolon separated coordinates]?annotations=distance".
    :return: The distance matrix using the coordinates provided in the URL.
    """

    res: Response = requests.get(url)
    data: json = res.json()

    matrix: list = data['distances']
    return matrix


def make_matrix(file_dir: str) -> DataFrame:
    """This function is used to query the OSRM API to get a distance matrix from a CSV file in *.txt.
    :param file_dir: String with CSV file directory.
    :return: Distance matrix.
    """

    regions: list[tuple[float, float]] = get_region_centers(file_dir)
    url: str = mount_request(regions)
    return pd.DataFrame(get_distance_matrix(url))
