from typing import Callable

from tax.ui.ui_component import UiComponent, InputTypes


class InputUiComponent(UiComponent):
    def __init__(self, label: str = None, placeholder: str = None, cast: Callable = None, validator: Callable = None):
        super().__init__(InputTypes.Input, label, cast, validator)
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


class SelectUiComponent(UiComponent):
    def __init__(self, label: str = None, cast: Callable = str, validator: Callable = None,
                 options: list[SelectOption] = None, preselected_index: int = 0):
        super().__init__(InputTypes.Select, label, cast, validator)
        self.options = options
        self.preselected_index = preselected_index

    def get_default_value(self):
        return self.options[self.preselected_index].value

    @staticmethod
    def get_index_of_option(options: list, value: str) -> int:
        for index, option in enumerate(options):
            if option.value == value:
                return index
        return 0

    def to_dict(self) -> dict:
        return {
            "type": InputTypes.Select.value,
            "label": self.label,
            "options": [option.to_dict() for option in self.options],
            "preselected_index": self.preselected_index,
        }
