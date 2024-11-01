from beaupy import prompt, select

from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.ika import IkaCalculator
from tax.employment_types.employment_type import EmploymentTypeBase


class IkaEmploymentType(EmploymentTypeBase):
    title = "Ika"
    calculator = IkaCalculator
    available_annual_salaries = ["12", "14", "14.5"]

    def __init__(self):
        super().__init__()
        self.annual_gross_salary = None
        self.salaries_count = None
        self.kids_number = None

    def input(self, **kwargs):
        super().input(**kwargs)

        if not self.annual_gross_salary:
            self.annual_gross_salary = prompt(prompt="Please enter your annual gross salary: ", target_type=float,
                                              validator=lambda count: count > 0)

        if not self.salaries_count:
            print("Number of annual salaries:")
            self.salaries_count = float(select(options=self.available_annual_salaries, cursor_index=1))

        if not self.kids_number:
            self.kids_number = prompt(prompt="Number of kids:", target_type=int, initial_value="0",
                                      validator=lambda count: count >= 0)
        return self

    def get_calculator(self) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=self.annual_gross_salary,
            salaries_count=self.salaries_count,
            kids_number=self.kids_number,
        )
