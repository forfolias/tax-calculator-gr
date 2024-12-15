from tax import _
from tax.calculators.business_calculator_interface import BusinessCalculatorInterface
from tax.costs.business_levy import BusinessLevy
from tax.employment_types.personal_company import PersonalCompanyEmploymentType
from tax.ui.components.ui_component_interface import UiComponentInterface
from tax.ui.components.ui_components import SelectOption, SelectUiComponent


class BusinessEntityEmploymentType(PersonalCompanyEmploymentType):
    title = None
    key = None
    calculator_class: type[BusinessCalculatorInterface]

    def get_input_data(self) -> list[UiComponentInterface]:
        input_data = super().get_input_data()

        options = [SelectOption(f"{cost.title} ({cost.amount}€)", str(cost.amount)) for cost in BusinessLevy.costs]
        if 'business_levy_cost' not in self.parameters or self.parameters['business_levy_cost'] is None:
            preselected_index = 1
        else:
            existing_value = str(int(self.parameters['business_levy_cost']))
            preselected_index = SelectUiComponent.get_index_of_option_value(options, existing_value)

        input_data.append(SelectUiComponent(
            name='business_levy_cost',
            label=_("business levy"), cast=float,
            options=options,
            preselected_index=preselected_index
        ))

        return input_data
