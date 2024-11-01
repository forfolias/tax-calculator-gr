from beaupy import select

from tax.employment_types.employment_type_interface import EmploymentTypeInterface
from tax.employment_types import available_employment_types


def get_employment_type() -> EmploymentTypeInterface:
    employment_types = available_employment_types
    print("Select employment type:")
    index = select(options=employment_types, preprocessor=lambda employment_type: employment_type[0], return_index=True)
    return employment_types[index][1]()


def main():
    employment_type = get_employment_type()

    # Collect all required data for the employment type
    employment_type.input()
    calculator = employment_type.get_calculator()

    print(f"Annual tax: {calculator.get_annual_tax():.2f}€")
    print(f"Annual health insurance cost: {calculator.get_annual_insurance_cost():.2f}€")
    print(f"Annual net income: {calculator.get_annual_net_salary():.2f}€")
    print(f"Monthly net income: {calculator.get_monthly_net_salary():.2f}€")
