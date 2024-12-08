from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.ike import IkeCalculator
from tax.employment_types.business_entity import BusinessEntityEmploymentType
from tax.ui.interactive_shell_components import SelectOption, SelectUiComponent
from tax.ui.ui_interface import UiInterface


class IkeEmploymentType(BusinessEntityEmploymentType):
    title = _("IKE")
    key = "ike"
    calculator = IkeCalculator

    def __init__(self, ui: UiInterface, **kwargs):
        super().__init__(ui, **kwargs)

        self.has_statutory_reserve = False
        if 'has_statutory_reserve' in kwargs and kwargs['has_statutory_reserve'] is not None:
            self.has_statutory_reserve = kwargs['has_statutory_reserve']

    def get_input_data(self) -> dict:
        input_data = super().get_input_data()
        options = [SelectOption("Yes", "1"), SelectOption("No", "0")]
        preselected_index = SelectUiComponent.get_index_of_option(
            options, str(int(self.has_statutory_reserve))
        ) if self.has_statutory_reserve is not None else 1
        input_data['has_statutory_reserve'] = SelectUiComponent(
            label=_("Statutory reserve requirement:"), cast=str,
            options=options,
            preselected_index=preselected_index,
        )

        return input_data

    def get_calculator_instance(self) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=float(self.annual_gross_salary),
            monthly_insurance_cost=float(self.monthly_insurance_cost),
            expenses=float(self.expenses),
            prepaid_tax=float(self.prepaid_tax),
            functional_year=int(self.functional_year),
            business_levy_cost=float(self.business_levy_cost),
            has_statutory_reserve=bool(int(self.has_statutory_reserve)),
        )
