import csv

from utils.datatypes import Region

def converter_para_array(dado):
    """
    Convert a data structure to a format suitable for JSON serialization.

    Parameters:
    - dado: Any data structure to be converted.

    Returns:
    - str: The converted string.
    """

    dado = str(dado)
    return dado.replace("[", "{").replace("]", "}").replace(f'"', "")


def mount_request(centers: list[tuple[float, float]]) -> str:
    """This function is used to build the API request URL.
    :param centers: Regions centers to calculate the distances.
    :return: URL to query the API request.
    """

    url: str = "http://router.project-osrm.org/table/v1/driving/"
    for coordinate in centers:
        url += str(coordinate[0]) + ","
        url += str(coordinate[1]) + ";"
    url = url[:-1]
    url += "?annotations=distance"
    return url


def parse_cost_csv(file_dir: str, id_col: int, long_col: int, lat_col: int) -> list[Region]:
    """This function parses a coordinate csv
    :param file_dir: String with CSV file directory.
    :param id_col: Column position that states the region's id.
    :param long_col: Column position that states the point's longitude.
    :param lat_col: Column position that states the point's latitude.
    :return: List of regions
    """

    coordinates: dict[str, list[tuple]] = {}
    with open(file_dir, 'r') as csv_file:
        reader: any = csv.reader(csv_file)

        for r in reader:
            region_id: str = str(r[id_col])
            try:
                long: float = float(r[long_col])
                lat: float = float(r[lat_col])
                coordinate: tuple = (long, lat)
                if region_id not in coordinates:
                    coordinates[region_id] = []
                coordinates[region_id].append(coordinate)
            except ValueError:
                pass

    regions: list[Region] = []

    for key in coordinates.keys():
        region: Region = Region(key, coordinates.get(key))
        regions.append(region)

    return regions
