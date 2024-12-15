from typing import Callable

from tax import _
from tax.exceptions import InvalidOption
from tax.ui.components.ui_component_interface import UiComponentInterface, InputTypes


class InputUiComponent(UiComponentInterface):
    def __init__(self, name: str = None, label: str = None, placeholder: str = None, cast: Callable = None,
                 validator: Callable = None):
        super().__init__(name, label, cast, validator)
        self.placeholder = placeholder

    def get_default_value(self):
        return self.placeholder

    def to_dict(self) -> dict:
        return {
            "type": InputTypes.Input.value,
            "label": self.label,
            "placeholder": self.placeholder,
        }


class SelectOption:
    def __init__(self, label: str = None, value: str = None):
        self.label = label
        self.value = value

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "value": self.value,
        }


class SelectUiComponent(UiComponentInterface):
    def __init__(self, name: str = None, label: str = None, cast: Callable = str, validator: Callable = None,
                 options: list[SelectOption] = None, preselected_index: int = 0):
        super().__init__(name, label, cast, validator)
        self.options = options
        self.preselected_index = preselected_index

    def get_default_value(self):
        return self.options[self.preselected_index].value

    @staticmethod
    def get_index_of_option_value(options: list[SelectOption], value: str) -> int:
        for index, option in enumerate(options):
            if option.value.lower() == value.lower():
                return index
        raise InvalidOption(
            _("Option '{value}' is not valid. Available options are: {options}").format(value=value, options=", ".join(
                [option.value for option in options]))
        )

    @staticmethod
    def get_index_of_option_label(options: list[SelectOption], label: str) -> int:
        for index, option in enumerate(options):
            if option.label.lower() == label.lower():
                return index
        raise InvalidOption(
            _("Option '{value}' is not valid. Available options are: {options}").format(value=label, options=", ".join(
                [option.value for option in options]))
        )

    def to_dict(self) -> dict:
        return {
            "type": InputTypes.Select.value,
            "label": self.label,
            "options": [option.to_dict() for option in self.options],
            "preselected_index": self.preselected_index,
        }
