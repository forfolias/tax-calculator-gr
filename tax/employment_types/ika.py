from typing import Self

from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.ika import IkaCalculator
from tax.employment_types.employment_type import EmploymentTypeBase


class IkaEmploymentType(EmploymentTypeBase):
    title = "IKA"
    calculator = IkaCalculator
    annual_gross_salary = None
    salaries_count = None
    kids_number = 0

    def __init__(self, **kwargs):
        super().__init__()
        self.annual_gross_salary = None
        if 'annual_gross_salary' in kwargs and kwargs['annual_gross_salary'] is not None:
            self.annual_gross_salary = float(kwargs['annual_gross_salary'])

        self.salaries_count = None
        if 'salaries_count' in kwargs and kwargs['salaries_count']:
            self.salaries_count = float(kwargs['salaries_count'])

        self.kids_number = None
        if 'kids_number' in kwargs and kwargs['kids_number'] is not None:
            self.kids_number = int(kwargs['kids_number'])

    def input(self, **kwargs) -> Self:
        super().input(**kwargs)

        from beaupy import prompt, select

        if not self.annual_gross_salary:
            self.annual_gross_salary = prompt(prompt="Please enter your annual gross salary: ", target_type=float,
                                              validator=lambda count: count > 0)

        if not self.salaries_count:
            print("Number of annual salaries:")
            self.salaries_count = float(select(options=["12", "14", "14.5"], cursor_index=1))

        if not self.kids_number:
            self.kids_number = prompt(prompt="Number of kids:", target_type=int, initial_value="0",
                                      validator=lambda count: count >= 0)
        return self

    def get_calculator_instance(self) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=self.annual_gross_salary,
            salaries_count=self.salaries_count,
            kids_number=self.kids_number,
        )
