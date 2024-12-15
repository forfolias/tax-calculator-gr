from tax import _
from tax.calculators.business_calculator_interface import BusinessCalculatorInterface
from tax.calculators.ike import IkeCalculator
from tax.employment_types.business_entity import BusinessEntityEmploymentType
from tax.ui.components.ui_component_interface import UiComponentInterface
from tax.ui.components.ui_components import SelectOption, SelectUiComponent


class IkeEmploymentType(BusinessEntityEmploymentType):
    title = _("IKE")
    key = "ike"
    calculator_class = IkeCalculator

    def get_input_data(self) -> list[UiComponentInterface]:
        input_data = super().get_input_data()
        options = [SelectOption(_("yes").capitalize(), "1"), SelectOption(_("no").capitalize(), "0")]
        preselected_index = SelectUiComponent.get_index_of_option_value(
            options, str(int(self.parameters['has_statutory_reserve']))
        ) if 'has_statutory_reserve' in self.parameters and self.parameters['has_statutory_reserve'] is not None else 1
        input_data.append(SelectUiComponent(
            name='has_statutory_reserve',
            label=_("statutory reserve requirement"), cast=str,
            options=options,
            preselected_index=preselected_index,
        ))

        return input_data

    def get_calculator_instance(self) -> BusinessCalculatorInterface:
        return self.calculator_class(
            annual_gross_salary=float(self.parameters['annual_gross_salary']),
            monthly_insurance_cost=float(self.parameters['monthly_insurance_cost']),
            expenses=float(self.parameters['expenses']),
            prepaid_tax=float(self.parameters['prepaid_tax']),
            functional_year=int(self.parameters['functional_year']),
            business_levy_cost=float(self.parameters['business_levy_cost']),
            has_statutory_reserve=bool(int(self.parameters['has_statutory_reserve'])),
        )
