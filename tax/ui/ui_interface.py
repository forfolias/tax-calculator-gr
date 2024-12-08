from abc import abstractmethod

from tax.ui.ui_component import UiComponent


class UiInterface:
    title = None
    key = None

    @abstractmethod
    def collect_input(self, input_data: dict[str, UiComponent]) -> dict:
        pass

    @abstractmethod
    def output(self, title: str, data: list[tuple[str, str]]) -> None:
        pass
