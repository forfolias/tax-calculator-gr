from tax import _
from tax.calculators.calculator_interface import CalculatorInterface
from tax.calculators.ika import IkaCalculator
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.ui.ui_component_interface import UiComponentInterface
from tax.ui.ui_components import InputUiComponent, SelectOption, SelectUiComponent


class IkaEmploymentType(EmploymentTypeBase):
    title = _("IKA")
    key = "ika"
    calculator = IkaCalculator

    @staticmethod
    def get_input_data(**kwargs) -> list[UiComponentInterface]:
        input_data = EmploymentTypeBase.get_input_data(**kwargs)

        input_data.append(InputUiComponent(
            name="annual_gross_salary",
            label=_("annual gross salary"),
            placeholder=kwargs['annual_gross_salary'] if 'annual_gross_salary' in kwargs and kwargs['annual_gross_salary'] is not None else "",
            cast=float,
            validator=lambda count: count > 0
        ))

        options = [SelectOption("12", "12"), SelectOption("14", "14"), SelectOption("14.5", "14.5")]
        preselected_index = SelectUiComponent.get_index_of_option_value(
            options,
            kwargs['salaries_count']
        ) if 'salaries_count' in kwargs and kwargs['salaries_count'] is not None else 1
        input_data.append(SelectUiComponent(
            name='salaries_count',
            label=_("number of annual salaries"), cast=float,
            options=options,
            preselected_index=preselected_index
        ))

        input_data.append(InputUiComponent(
            name='kids_number',
            label=_("number of kids"),
            placeholder=str(kwargs['kids_number']) if 'kids_number' in kwargs and kwargs['kids_number'] is not None else "0",
            cast=int,
            validator=lambda count: count >= 0
        ))

        return input_data

    def get_calculator(self, **kwargs) -> CalculatorInterface:
        return self.calculator(
            annual_gross_salary=float(kwargs['annual_gross_salary']),
            salaries_count=float(kwargs['salaries_count']),
            kids_number=int(kwargs['kids_number']),
        )
