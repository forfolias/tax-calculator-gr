from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.ike import IkeCalculator
from tax.employment_types.business_entity import BusinessEntityEmploymentType


class IkeEmploymentType(BusinessEntityEmploymentType):
    title = "IKE"
    calculator = IkeCalculator

    def get_calculator_instance(self) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=float(self.annual_gross_salary),
            monthly_insurance_cost=self.monthly_insurance_cost,
            expenses=float(self.expenses),
            prepaid_tax=float(self.prepaid_tax),
            functional_year=int(self.functional_year),
            business_levy_cost=self.business_levy_cost,
        )
