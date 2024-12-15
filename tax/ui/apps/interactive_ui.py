from abc import abstractmethod
from typing import List

from tax.employment_types.employment_type import EmploymentTypeBase
from tax.ui.apps.ui_interface import UiInterface


class InteractiveUI(UiInterface):

    def __init__(self, employment_types: List[EmploymentTypeBase] = None):
        super().__init__(employment_types)
        self.employment_types = employment_types if employment_types else self.get_employment_types()

    @abstractmethod
    def get_employment_types(self, **kwargs) -> List[EmploymentTypeBase]:
        pass
