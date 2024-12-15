import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Optional, Callable, List

from tax import _
from tax.employment_types import available_employment_types
from tax.employment_types.employment_type import EmploymentTypeBase
from tax.ui.apps.interactive_ui import InteractiveUI
from tax.ui.components.ui_component_interface import UiComponentInterface
from tax.ui.components.ui_components import InputUiComponent, SelectUiComponent


class MultiSelectDialog:
    def __init__(self, parent, title, options):
        """
        Create a multiselect dialog with a list of options.

        :param parent: Parent window
        :param title: Dialog title
        :param options: List of options to select from
        """
        # Create the dialog window
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("260x220")
        self.window.resizable(False, False)

        tk.Label(self.window, text=_("Select employment type") + ":").pack(pady=10)
        self.listbox = tk.Listbox(self.window, selectmode=tk.MULTIPLE, width=40, height=5)
        for option in options:
            self.listbox.insert(tk.END, option)
        self.listbox.pack(padx=20, pady=10)

        # Variables to store the result
        self.selected_indexes = None

        # Confirm and Cancel buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        confirm_btn = tk.Button(button_frame, text=_("OK"), command=self.on_confirm)
        confirm_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(button_frame, text=_("Cancel"), command=self.window.destroy)
        cancel_btn.pack(side=tk.LEFT)

        # Make the dialog modal
        self.window.grab_set()

    def on_confirm(self):
        """
        Handle confirm button click by storing selected indexes.
        """
        # Get selected indexes
        self.selected_indexes = self.listbox.curselection()

        # Close the dialog
        self.window.destroy()

    def show(self):
        """
        Show the dialog and wait for it to close.

        :return: Tuple of selected indexes or None if canceled
        """
        # Wait for the window to be closed
        self.window.wait_window()

        # Return the selected indexes
        return self.selected_indexes

class GraphicalUi(InteractiveUI):
    title = "Graphical UI"
    key = "gui"
    window_title = "Tax calculator GR"

    def __init__(self, employment_types: List[EmploymentTypeBase] = None):
        self.main_window_width = 360
        self.main_window_height = 574
        self.main_window = tk.Tk()
        self.main_window.withdraw()
        self.main_window.title(self.window_title)
        self.main_window.geometry(f"{self.main_window_width}x{self.main_window_height}")
        self.notebook = ttk.Notebook(self.main_window)

        super().__init__(employment_types)

        self.tabs_data = {}


    def get_employment_types(self, **kwargs) -> List[EmploymentTypeBase]:
        indexes = MultiSelectDialog(
            self.main_window,
            self.window_title,
            [employment_type.title for employment_type in available_employment_types]
        ).show()
        employment_types = []
        if indexes:
            for index in indexes:
                employment_types.append(available_employment_types[index](**kwargs))

        return employment_types


    def run(self) -> None:
        if not self.employment_types:
            return

        self.main_window.deiconify()

        label = tk.Label(self.main_window, text=_("Calculate net salary based on annual gross income per employment type."), wraplength=self.main_window_width-20)
        label.pack(padx=10, pady=5, fill=tk.X)

        for employment_type in self.employment_types:
            self.do_run(employment_type)

        self.notebook.pack(expand=True, fill="both")

        # Resize main window based on contents
        self.main_window.update_idletasks()
        self.main_window.geometry(f"{self.main_window_width}x{self.main_window.winfo_reqheight()}+{self.main_window.winfo_x()}+{self.main_window.winfo_y()}")
        self.main_window.resizable(False, False)

        # Start the GUI event loop
        self.main_window.mainloop()

    def do_run(self, employment_type: EmploymentTypeBase) -> None:
        title = employment_type.title
        input_data = employment_type.get_input_data()
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)

        input_frame = tk.Frame(tab)
        input_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        inputs = []
        for ui_component in input_data:
            inputs.append((self._create_input_widget(input_frame, ui_component), ui_component))
        self.tabs_data[employment_type.key] = inputs

        submit_button = tk.Button(tab, text=_("Calculate"), command=lambda: self._validate_and_submit(employment_type))
        submit_button.pack(pady=10)

    def output(self, title: str, data: list[tuple[str, str]]) -> None:
        output_text = "\n".join([f"{line[0].capitalize()}: {line[1]}" for line in data])
        messagebox.showinfo(title=self.window_title, message=title, detail=output_text)

    def _create_input_widget(self, parent_frame: tk.Frame, ui_component: UiComponentInterface):
        input_frame = tk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, pady=5)

        # Add label
        if ui_component.label:
            label = tk.Label(input_frame, text=ui_component.label.capitalize() + ":", anchor='w')
            label.pack(side=tk.TOP, fill=tk.X)

        # Render based on input type
        if isinstance(ui_component, InputUiComponent):
            return self._create_text_input(input_frame, ui_component)
        elif isinstance(ui_component, SelectUiComponent):
            return self._create_select_input(input_frame, ui_component)

    def _create_text_input(self, parent_frame, ui_component: InputUiComponent):
        # Create StringVar to hold the value
        var = tk.StringVar(parent_frame)

        # Set initial value if placeholder exists
        if ui_component.placeholder is not None:
            var.set(str(ui_component.placeholder))

        # Create entry widget
        entry = tk.Entry(parent_frame, textvariable=var)
        entry.pack(fill=tk.X)

        return entry

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

        return var

    def _validate_and_submit(self, employment_type: EmploymentTypeBase):
        try:
            # Validate and convert all inputs
            for input_tuple in self.tabs_data[employment_type.key]:
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
                employment_type.parameters[ui_component.name] = value

        except Exception as e:
            messagebox.showerror(_("Error"), str(e))

        self.output(employment_type.title, employment_type.get_output_data())

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
