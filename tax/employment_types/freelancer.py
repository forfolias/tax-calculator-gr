from beaupy import prompt, select

from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.freelancer import FreelancerCalculator
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.insurance_classes.freelancer import Freelancer


class FreelancerEmploymentType(EmploymentTypeBase):
    title = "Freelancer"
    calculator = FreelancerCalculator

    def __init__(self):
        super().__init__()
        self.insurance_class = None
        self.annual_gross_salary = None
        self.expenses = None
        self.prepaid_tax = None
        self.functional_year = None

    def input(self, **kwargs):
        super().input(**kwargs)

        if not self.annual_gross_salary:
            self.annual_gross_salary = prompt(prompt="Please enter your annual gross salary: ", target_type=float,
                                              validator=lambda count: count > 0)

        insurance_classes = Freelancer.insurance_classes
        print("Please select the insurance class:")
        index = select(
            options=insurance_classes,
            preprocessor=lambda insurance_class: f"{insurance_class.title} ({insurance_class.cost})",
            return_index=True
        )
        self.insurance_class = insurance_classes[index]

        if not self.expenses:
            self.expenses = prompt(prompt="Please enter your annual expenses: ", target_type=float, initial_value="0",
                                   validator=lambda count: count >= 0)

        if not self.prepaid_tax:
            self.prepaid_tax = prompt(prompt="Please enter any prepaid tax amount from previous year: ",
                                      target_type=float, initial_value="0", validator=lambda count: count >= 0)

        if not self.functional_year:
            self.functional_year = prompt(prompt="Please enter company's functional number of years: ",
                                          target_type=int, initial_value="0", validator=lambda count: count >= 0)

    def get_calculator(self) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=self.annual_gross_salary,
            insurance_class=self.insurance_class,
            expenses=self.expenses,
            prepaid_tax=self.prepaid_tax,
            functional_year=self.functional_year,
        )
