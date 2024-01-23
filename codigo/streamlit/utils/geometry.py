from pandas import DataFrame, Series
from shapely.geometry import Polygon, Point
import pandas as pd


def get_region_centers(file_dir: str) -> list[tuple[float, float]]:
    """This function is used to get centers from regions inside a csv file.
    :param file_dir: String with CSV file directory.
    :return: List with center of regions.
    """
    df: DataFrame = pd.read_csv(file_dir)
    regions: Series = df['setor']
    long: Series = df['lon']
    lat: Series = df['lat']
    centers: list[tuple[float, float]] = []

    row: int = 1
    region_index: int = 1

    while row < regions.size:
        polygon_coordinates: list[tuple[float, float]] = []
        while row < regions.size and regions.iloc[row] == region_index:
            polygon_coordinates.append((lat.iloc[row], long.iloc[row]))
            row += 1
        polygon_center: Point = Polygon(polygon_coordinates).centroid
        centers.append((polygon_center.x, polygon_center.y))
        region_index += 1

    return centers
