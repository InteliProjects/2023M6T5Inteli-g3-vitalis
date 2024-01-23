import math
from enum import Enum


class Sector:

    def __init__(self, id_number: int, demands: int, workers: int, distances: list[float]) -> None:
        """This class represents a sector.
        :param id_number: Identification number.
        :param demands: Number of demands / services to be made.
        :param workers: Number of workers.
        :param distances: Distance array to other sectors this -> other.
        """
        self.id_number = id_number
        self.demands = demands
        self.workers = workers
        self.distances = distances
        self.score = self._calc_score()

    @classmethod
    def init_with_score(cls, id_number: int, score: int, distances: list[float]) -> 'Sector':
        sector: Sector = Sector(id_number, 0, 0, distances)
        sector.score = score
        return sector

    def remove_worker(self) -> None:
        """This void method is used to remove a worker from the sector, updating its score.
        """
        self.workers -= 1
        self.score -= 1

    def add_worker(self) -> None:
        """This void method is used to add a worker to the sector, updating its score.
        """
        self.workers += 1
        self.score += 1

    def _calc_score(self) -> int:
        """This method is used to update the sector's score.
        """
        raw_score: int = (2 * self.workers) - self.demands
        return (-math.ceil(abs((2 * self.workers) - self.demands) / 2) if raw_score < 0
                else math.floor(((2 * self.workers) - self.demands) / 2))

    def transfer(self, receiver: any) -> int:
        """This method is used to transfer workers between sectors.
        :return: Number of workers transferred.
        """
        counter: int = 0
        while self.score > 0 > receiver.score and self.score - 1 >= 0:
            receiver.add_worker()
            self.remove_worker()
            counter += 1
        return counter

    def __str__(self) -> str:
        return (f'Sector(id={self.id_number},'
                f'demands={self.demands},'
                f'workers={self.workers},'
                f'score={self.score}, '
                f'distances={self.distances})'
                )


class SolutionType(Enum):
    DONE: 'SolutionType' = 0
    UNFEASIBLE: 'SolutionType' = 1
    SUBOPTIMAL: 'SolutionType' = 2


class Transaction:
    def __init__(self, sender_sector: Sector, receiver_sector: Sector) -> None:
        """This class represents a transaction of workers between sectors.
        :param sender_sector: Sector that is sending the workers.
        :param receiver_sector: Sector that is receiving the workers.
        """
        self.sender_sector: Sector = sender_sector
        self.receiver_sector: Sector = receiver_sector
        self.amount = 1

    @classmethod
    def constructor_with_amount(cls, sender_sector, receiver_sector, amount) -> 'Transaction':
        """This class method is used to construct a transaction of workers between sectors specifying the amount of
        workers moved.
        :param sender_sector: Sector that is sending the workers.
        :param receiver_sector: Sector that is receiving the workers.
        :param amount: Amount of workers moved.
        """
        transaction: Transaction = Transaction(sender_sector, receiver_sector)
        transaction.amount = amount
        return transaction

    def equals(self, other_transaction: 'Transaction') -> bool:
        """This method is used to compare transactions.
        :param other_transaction: Transaction that should be compared with self.
        :return: If transactions are equal are or not (same transfer direction).
        """
        return (self.sender_sector == other_transaction.sender_sector and
                self.receiver_sector == other_transaction.receiver_sector)

    def add(self) -> None:
        """This method is used to increase the amount of transferred workers in a transaction.
        """
        self.amount += 1

    def __str__(self):
        return f'Transaction({self.sender_sector.id_number} -> {self.receiver_sector.id_number} | {self.amount})'


Solution = list[Transaction]


class Region:
    """ This class defines a region where workers and demands are located.
    Attributes:
        id: Region's id.
        coordinates: Where workers live inside the region.
    """

    def __init__(self, region_id, coordinates):
        """
        :param region_id: Region's id.
        :param coordinates: Where workers live inside the region.
        """

        self.id: str = region_id
        self.coordinates: list[tuple] = coordinates
        self.center: tuple = self._calculate_center()

    def __str__(self):
        print(f'Region=(id={self.id}, coordinates={self.coordinates}')

    def _calculate_center(self) -> tuple:
        """This function calculates the center-most point in the region.
        :return: Center-most point of the region.
        """

        sum_x: float = 0
        sum_y: float = 0

        for coordinate in self.coordinates:
            sum_x += coordinate[0]
            sum_y += coordinate[1]

        center: tuple = (sum_x / len(self.coordinates),
                         sum_y / len(self.coordinates))

        tree: cKDTree = cKDTree(self.coordinates)
        distance, index = tree.query(center)
        return self.coordinates[index]
