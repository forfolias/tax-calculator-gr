from typing import List

from tax import _
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.ui.apps.ui_interface import UiInterface


class CliUi(UiInterface):
    title = _("Command line arguments")
    key = "cli"

    def run(self, employment_types: List[EmploymentTypeBase] = list) -> None:
        for employment_type in self.employment_types:
            print(f"{employment_type.title}")
            for line in employment_type.get_output_data():
                print(f"{line[0]} {line[1]}")
