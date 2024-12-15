from abc import abstractmethod
from typing import List

from tax.employment_types.employment_type import EmploymentTypeBase


class UiInterface:
    title = None
    key = None
    employment_types: List[EmploymentTypeBase] = []

    def __init__(self, employment_types: List[EmploymentTypeBase] = None):
        self.employment_types = employment_types if employment_types else []

    @abstractmethod
    def run(self) -> None:
        pass
