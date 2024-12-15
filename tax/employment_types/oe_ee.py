from tax import _
from tax.calculators.business_calculator_interface import BusinessCalculatorInterface
from tax.calculators.oe_ee import OeEeCalculator
from tax.employment_types.business_entity import BusinessEntityEmploymentType


class OeEeEmploymentType(BusinessEntityEmploymentType):
    title = _("OE-EE")
    key = 'oe-ee'
    calculator_class = OeEeCalculator

    def get_calculator_instance(self) -> BusinessCalculatorInterface:
        return self.calculator_class(
            annual_gross_salary=float(self.parameters['annual_gross_salary']),
            monthly_insurance_cost=float(self.parameters['monthly_insurance_cost']),
            expenses=float(self.parameters['expenses']),
            prepaid_tax=float(self.parameters['prepaid_tax']),
            functional_year=int(self.parameters['functional_year']),
            business_levy_cost=float(self.parameters['business_levy_cost']),
        )
