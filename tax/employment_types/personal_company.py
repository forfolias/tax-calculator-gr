from typing import Self

from tax.employment_types.employment_type import EmploymentTypeBase
from tax.costs.company_health_insurance import CompanyHealthInsurance


class PersonalCompanyEmploymentType(EmploymentTypeBase):
    title = ""
    calculator = None

    def __init__(self, **kwargs):
        super().__init__()

        self.annual_gross_salary = None
        if 'annual_gross_salary' in kwargs and kwargs['annual_gross_salary'] is not None:
            self.annual_gross_salary = float(kwargs['annual_gross_salary'])

        self.monthly_insurance_cost = None
        if 'monthly_insurance_cost' in kwargs and kwargs['monthly_insurance_cost'] is not None:
            self.monthly_insurance_cost = float(kwargs['monthly_insurance_cost'])

        self.expenses = None
        if 'expenses' in kwargs and kwargs['expenses'] is not None:
            self.expenses = float(kwargs['expenses'])

        self.prepaid_tax = None
        if 'prepaid_tax' in kwargs and kwargs['prepaid_tax'] is not None:
            self.prepaid_tax = float(kwargs['prepaid_tax'])

        self.functional_year = None
        if 'functional_year' in kwargs and kwargs['functional_year'] is not None:
            self.functional_year = int(kwargs['functional_year'])

    def input(self, **kwargs) -> Self:
        super().input(**kwargs)

        from beaupy import prompt, select

        if not self.annual_gross_salary:
            self.annual_gross_salary = prompt(prompt="Please enter your annual gross salary: ", target_type=float,
                                              validator=lambda count: count > 0)

        insurance_classes = CompanyHealthInsurance.costs
        if not self.monthly_insurance_cost:
            print("Please select the insurance class:")
            index = select(
                options=insurance_classes,
                preprocessor=lambda insurance_class: f"{insurance_class.title} ({insurance_class.amount})",
                return_index=True
            )
            self.monthly_insurance_cost = insurance_classes[index].amount
        elif isinstance(self.monthly_insurance_cost, (int,)):
            self.monthly_insurance_cost = insurance_classes[int(self.monthly_insurance_cost)].amount
        elif isinstance(self.monthly_insurance_cost, (str,)):
            self.monthly_insurance_cost = float(self.monthly_insurance_cost)

        if self.prepaid_tax is None:
            self.prepaid_tax = prompt(prompt="Please enter any prepaid tax amount from previous year: ",
                                      target_type=float, initial_value="0", validator=lambda count: count >= 0)

        if self.expenses is None:
            self.expenses = prompt(prompt="Please enter your annual expenses: ", target_type=float, initial_value="0",
                                   validator=lambda count: count >= 0)

        if self.functional_year is None:
            self.functional_year = prompt(prompt="Please enter company's functional number of years: ",
                                          target_type=int, initial_value="0", validator=lambda count: count >= 0)

        return self
