from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.freelancer import FreelancerCalculator
from tax.employment_types.personal_company import PersonalCompanyEmploymentType


class FreelancerEmploymentType(PersonalCompanyEmploymentType):
    title = _("Freelancer")
    key = "freelancer"
    calculator = FreelancerCalculator

    def get_calculator(self, **kwargs) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=float(kwargs['annual_gross_salary']),
            monthly_insurance_cost=float(kwargs['monthly_insurance_cost']),
            expenses=float(kwargs['expenses']),
            prepaid_tax=float(kwargs['prepaid_tax']),
            functional_year=int(kwargs['functional_year']),
        )
