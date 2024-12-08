from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.freelancer import FreelancerCalculator
from tax.employment_types.personal_company import PersonalCompanyEmploymentType


class FreelancerEmploymentType(PersonalCompanyEmploymentType):
    title = "Freelancer"
    calculator = FreelancerCalculator

    def get_calculator_instance(self) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=float(self.annual_gross_salary),
            monthly_insurance_cost=float(self.monthly_insurance_cost),
            expenses=float(self.expenses),
            prepaid_tax=float(self.prepaid_tax),
            functional_year=int(self.functional_year),
        )
