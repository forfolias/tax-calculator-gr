from tax import _
from tax.calculators.business_calculator_interface import BusinessCalculatorInterface
from tax.calculators.freelancer import FreelancerCalculator
from tax.employment_types.personal_company import PersonalCompanyEmploymentType


class FreelancerEmploymentType(PersonalCompanyEmploymentType):
    title = _("Freelancer")
    key = "freelancer"
    calculator_class = FreelancerCalculator

    def get_calculator_instance(self) -> BusinessCalculatorInterface:
        return self.calculator_class(
            annual_gross_salary=float(self.parameters['annual_gross_salary']),
            monthly_insurance_cost=float(self.parameters['monthly_insurance_cost']),
            expenses=float(self.parameters['expenses']),
            prepaid_tax=float(self.parameters['prepaid_tax']),
            functional_year=int(self.parameters['functional_year']),
        )
