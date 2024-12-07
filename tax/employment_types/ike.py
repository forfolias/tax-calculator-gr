from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.ike import IkeCalculator
from tax.employment_types.business_entity import BusinessEntityEmploymentType


class IkeEmploymentType(BusinessEntityEmploymentType):
    title = "IKE"
    calculator = IkeCalculator

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.has_statutory_reserve = False
        if 'has_statutory_reserve' in kwargs and kwargs['has_statutory_reserve'] is not None:
            self.has_statutory_reserve = bool(int(kwargs['has_statutory_reserve']))

    def get_calculator_instance(self) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=float(self.annual_gross_salary),
            monthly_insurance_cost=self.monthly_insurance_cost,
            expenses=float(self.expenses),
            prepaid_tax=float(self.prepaid_tax),
            functional_year=int(self.functional_year),
            business_levy_cost=self.business_levy_cost,
            has_statutory_reserve=self.has_statutory_reserve,
        )
