from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.ike import IkeCalculator
from tax.employment_types.business_entity import BusinessEntityEmploymentType
from tax.ui.ui_component_interface import UiComponentInterface
from tax.ui.ui_components import SelectOption, SelectUiComponent


class IkeEmploymentType(BusinessEntityEmploymentType):
    title = _("IKE")
    key = "ike"
    calculator = IkeCalculator

    @staticmethod
    def get_input_data(**kwargs) -> list[UiComponentInterface]:
        input_data = BusinessEntityEmploymentType.get_input_data(**kwargs)
        options = [SelectOption(_("yes").capitalize(), "1"), SelectOption(_("no").capitalize(), "0")]
        preselected_index = SelectUiComponent.get_index_of_option_value(
            options, str(int(kwargs['has_statutory_reserve']))
        ) if 'has_statutory_reserve' in kwargs and kwargs['has_statutory_reserve'] is not None else 1
        input_data.append(SelectUiComponent(
            name='has_statutory_reserve',
            label=_("statutory reserve requirement"), cast=str,
            options=options,
            preselected_index=preselected_index,
        ))

        return input_data

    def get_calculator(self, **kwargs) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=float(kwargs['annual_gross_salary']),
            monthly_insurance_cost=float(kwargs['monthly_insurance_cost']),
            expenses=float(kwargs['expenses']),
            prepaid_tax=float(kwargs['prepaid_tax']),
            functional_year=int(kwargs['functional_year']),
            business_levy_cost=float(kwargs['business_levy_cost']),
            has_statutory_reserve=bool(int(kwargs['has_statutory_reserve'])),
        )
