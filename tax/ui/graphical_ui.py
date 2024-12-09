import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Optional, Union, Callable

from tax import _
from tax.ui.ui_component_interface import UiComponentInterface
from tax.ui.ui_components import InputUiComponent, SelectUiComponent
from tax.ui.ui_interface import UiInterface


class GraphicalUi(UiInterface):
    title = "Graphical UI"
    key = "gui"

    window_title = "Tax calculator GR"

    def __init__(self):
        self.root = None
        self.input_entries: list[tuple[Union[tk.Entry, tk.StringVar], UiComponentInterface]] = []
        self.response = {}

    def collect_input(self, title: str = None, input_data: [UiComponentInterface] = list) -> dict:
        # Create the main window
        self.root = tk.Tk()
        self.root.title(self.window_title)
        self.root.geometry("400x522")

        # Create a frame for inputs
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Add label
        if title:
            label = tk.Label(input_frame, text=title, font=("Helvetica", 18), anchor='center')
            label.pack(side=tk.TOP, fill=tk.X)

        # Clear previous state
        self.input_entries.clear()
        self.response.clear()

        # Render input components
        for ui_component in input_data:
            self._create_input_widget(input_frame, ui_component)

        # Submit button
        submit_button = tk.Button(self.root, text=_("Submit"), command=self._validate_and_submit)
        submit_button.pack(pady=10)

        # Start the GUI event loop
        self.root.mainloop()

        return self.response

    def output(self, title: str, data: list[tuple[str, str]]) -> None:
        output_text = "\n".join([f"{line[0].capitalize()}: {line[1]}" for line in data])
        messagebox.showinfo(title=self.window_title, message=title, detail=output_text)

    def _create_input_widget(self, parent_frame: tk.Frame, ui_component: UiComponentInterface):
        # Create a frame for this input
        input_frame = tk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, pady=5)

        # Add label
        if ui_component.label:
            label = tk.Label(input_frame, text=ui_component.label.capitalize() + ":", anchor='w')
            label.pack(side=tk.TOP, fill=tk.X)

        # Render based on input type
        if isinstance(ui_component, InputUiComponent):
            self._create_text_input(input_frame, ui_component)
        elif isinstance(ui_component, SelectUiComponent):
            self._create_select_input(input_frame, ui_component)

    def _create_text_input(self, parent_frame, ui_component: InputUiComponent):
        # Create StringVar to hold the value
        var = tk.StringVar(parent_frame)

        # Set initial value if placeholder exists
        if ui_component.placeholder:
            var.set(str(ui_component.placeholder))

        # Create entry widget
        entry = tk.Entry(parent_frame, textvariable=var)
        entry.pack(fill=tk.X)

        # Store references
        self.input_entries.append((entry, ui_component))

    def _create_select_input(self, parent_frame: tk.Frame, ui_component: SelectUiComponent):
        # Create StringVar to hold the value
        var = tk.StringVar(parent_frame)

        # Populate options
        options = [option.label.capitalize() for option in ui_component.options]

        # Set default selection
        var.set(options[ui_component.preselected_index])

        # Create dropdown
        dropdown = ttk.Combobox(
            parent_frame,
            textvariable=var,
            values=options,
            state="readonly"
        )
        dropdown.pack(fill=tk.X)

        # Store references
        self.input_entries.append((var, ui_component))

    def _validate_and_submit(self):
        try:
            # Validate and convert all inputs
            for input_tuple in self.input_entries:
                # Find the corresponding UI component
                ui_component = input_tuple[1]
                widget = input_tuple[0]

                value = self._get_widget_value(widget, ui_component)
                if value is None:
                    messagebox.showerror(
                        _("Invalid Input"),
                        _("Invalid input for '{field_name}'").format(field_name=ui_component.label)
                    )
                    return

                if not self._validate_value(value, ui_component.validator):
                    messagebox.showerror(
                        _("Validation Error"),
                        _("Validation failed for '{field_name}'").format(field_name=ui_component.label)
                    )
                    return

                # Store the validated value
                self.response[ui_component.name] = value

            # Close the window if all validations pass
            self.root.quit()
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _get_widget_value(self, widget: tk.Entry, ui_component: UiComponentInterface) -> Optional[Any]:
        # Get the raw value
        if isinstance(ui_component, SelectUiComponent):
            selected_index = SelectUiComponent.get_index_of_option_label(ui_component.options, widget.get())
            raw_value = ui_component.options[selected_index].value
        else:
            raw_value = widget.get()

        # Cast the value if needed
        if ui_component.cast:
            try:
                return ui_component.cast(raw_value)
            except (ValueError, TypeError):
                return None

        return raw_value

    def _validate_value(self, value: Any, validator: Callable = None) -> bool:
        # Validate if a validator is provided
        if validator is not None:
            try:
                return validator(value)
            except Exception:
                return False
        return True
