from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.oe_ee import OeEeCalculator
from tax.employment_types.business_entity import BusinessEntityEmploymentType


class OeEeEmploymentType(BusinessEntityEmploymentType):
    title = _("OE-EE")
    key = 'oe-ee'
    calculator = OeEeCalculator

    def get_calculator(self, **kwargs) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=float(kwargs['annual_gross_salary']),
            monthly_insurance_cost=float(kwargs['monthly_insurance_cost']),
            expenses=float(kwargs['expenses']),
            prepaid_tax=float(kwargs['prepaid_tax']),
            functional_year=int(kwargs['functional_year']),
            business_levy_cost=float(kwargs['business_levy_cost']),
        )
