from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.ika import IkaCalculator
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.ui.components.ui_component_interface import UiComponentInterface
from tax.ui.components.ui_components import InputUiComponent, SelectOption, SelectUiComponent


class IkaEmploymentType(EmploymentTypeBase):
    title = _("IKA")
    key = "ika"
    calculator_class = IkaCalculator

    def get_input_data(self) -> list[UiComponentInterface]:
        input_data = super().get_input_data()

        input_data.append(InputUiComponent(
            name="annual_gross_salary",
            label=_("annual gross salary"),
            placeholder=self.parameters['annual_gross_salary'] if 'annual_gross_salary' in self.parameters and self.parameters['annual_gross_salary'] is not None else "",
            cast=float,
            validator=lambda count: count > 0
        ))

        options = [SelectOption("12", "12"), SelectOption("14", "14"), SelectOption("14.5", "14.5")]
        preselected_index = SelectUiComponent.get_index_of_option_value(
            options,
            str(self.parameters['salaries_count'])
        ) if 'salaries_count' in self.parameters and self.parameters['salaries_count'] is not None else 1
        input_data.append(SelectUiComponent(
            name='salaries_count',
            label=_("number of annual salaries"), cast=float,
            options=options,
            preselected_index=preselected_index
        ))

        input_data.append(InputUiComponent(
            name='kids_number',
            label=_("number of kids"),
            placeholder=str(self.parameters['kids_number']) if 'kids_number' in self.parameters and self.parameters['kids_number'] is not None else "0",
            cast=int,
            validator=lambda count: count >= 0
        ))

        return input_data

    def get_calculator(self) -> CalculatorInterface:
        self.validate_parameters()
        return self.calculator_class(
            annual_gross_salary=float(self.parameters['annual_gross_salary']),
            salaries_count=float(self.parameters['salaries_count']),
            kids_number=int(self.parameters['kids_number']),
        )
