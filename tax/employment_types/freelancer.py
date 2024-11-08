from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.freelancer import FreelancerCalculator
from tax.employment_types.personal_company import PersonalCompanyEmploymentType


class FreelancerEmploymentType(PersonalCompanyEmploymentType):
    title = "Freelancer"
    calculator = FreelancerCalculator

    def get_calculator_instance(self) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=self.annual_gross_salary,
            monthly_insurance_cost=self.monthly_insurance_cost,
            expenses=self.expenses,
            prepaid_tax=self.prepaid_tax,
            functional_year=self.functional_year,
        )
