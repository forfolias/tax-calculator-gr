from abc import abstractmethod

from tax.ui.ui_component_interface import UiComponentInterface


class UiInterface:
    title = None
    key = None

    @abstractmethod
    def collect_input(self, title: str = None, input_data: list[UiComponentInterface] = list) -> dict:
        pass

    @abstractmethod
    def output(self, title: str, data: list[tuple[str, str]]) -> None:
        pass
