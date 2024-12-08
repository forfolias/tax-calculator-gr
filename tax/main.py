import argparse
import json

from tax.employment_types import available_employment_types
from tax.exceptions import UnknownEmploymentType, UnknownUI
from tax.ui import available_user_interfaces
from . import setup_translations

_ = setup_translations()


def get_employment_type_class(employment_type_key: str):
    for cls in available_employment_types:
        if cls.key == employment_type_key.lower():
            return cls
    raise UnknownEmploymentType(f"Unknown employment type: {employment_type_key}")


def get_ui_class(ui_key: str):
    for cls in available_user_interfaces:
        if cls.key == ui_key.lower():
            return cls
    raise UnknownUI(f"Unknown user interface: {ui_key}")


def get_app_parser():
    parser = argparse.ArgumentParser(
        description=_("Calculate net salary based on annual gross income per employment type.")
    )

    parser.add_argument(
        "--employment-type",
        "-e",
        action="extend",
        nargs="+",
        choices=[employment_type.key for employment_type in available_employment_types],
        default=None,
        help=_("Specify employment type. Can be used multiple times. Defaults to '{default}'").format(
            default=available_employment_types[0].key),
    )
    parser.add_argument(
        "--user-interface",
        "-u",
        choices=[ui.key.lower() for ui in available_user_interfaces],
        default=None,
        help=_("Specify the user interface to use. Defaults to '{default}'").format(
            default=available_user_interfaces[0].key)
    )
    parser.add_argument(
        "--parameters",
        "-p",
        action="store_true",
        help=_("Print available options for specified employment type(s) and exit")
    )

    # Add all employment-types specific options
    options = {}
    for employment_type in available_employment_types:
        properties = [
            k for k, v in employment_type.calculator.__dict__.items()
            if not callable(v) and not k.startswith("__") and not k.startswith("_abc_")
        ]
        for option in properties:
            option = option.replace('_', '-')
            if option not in options:
                options[option] = {'employment_types': []}
            options[option]['employment_types'].append(employment_type.key)

    for option, option_data in options.items():
        applies_to = ", ".join(option_data['employment_types'])
        parser.add_argument(f"--{option}", help=f"Applies to: {applies_to}")

    return parser


def main():
    parser = get_app_parser()
    args = vars(parser.parse_args())

    # Get employment type names and remove from args
    employment_type_names = list(set(args['employment_type'])) if args['employment_type'] else [
        available_employment_types[0].key]
    args.pop('employment_type', None)

    ui_key = args['user_interface'] if args['user_interface'] else available_user_interfaces[0].key
    ui = get_ui_class(ui_key)
    args.pop('user_interface', None)

    # Convert the rest of args to employment type class kwargs
    args = {key.replace('-', '_'): value for key, value in args.items()}

    for employment_type_name in employment_type_names:
        employment_class = get_employment_type_class(employment_type_name)
        employment_type = employment_class(ui(), **args)

        if 'parameters' in args and args['parameters']:
            print(json.dumps({'employment_type': employment_type_name,
                              'parameters': [{"name": index.replace('_', '-'), **component.to_dict()} for
                                             index, component in employment_type.get_input_data().items()]}))
            continue

        employment_type.input(**args)
        employment_type.output()


if __name__ == "__main__":
    main()
