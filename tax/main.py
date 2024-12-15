import argparse
from inspect import signature

from tax.employment_types import available_employment_types
from tax.exceptions import UnknownEmploymentType, UnknownUI
from tax.ui.apps import available_user_interfaces
from . import setup_translations

_ = setup_translations()


def get_employment_type_class(employment_type_key: str):
    for cls in available_employment_types:
        if cls.key == employment_type_key.lower():
            return cls
    raise UnknownEmploymentType(_("Unknown employment type: '{name}'").format(name=employment_type_key))


def get_ui_class(ui_key: str):
    for cls in available_user_interfaces:
        if cls.key == ui_key.lower():
            return cls
    raise UnknownUI(_("Unknown user interface: '{name}'").format(name=ui_key))


def get_app_parser():
    parser = argparse.ArgumentParser(
        description=_("Calculate net salary based on annual gross income per employment type.")
    )

    parser.add_argument(
        "--employment-type",
        "-e",
        action="extend",
        nargs="*",
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

    # Add all employment-types specific parameters
    parameters = {}
    for employment_type in available_employment_types:
        params = signature(employment_type.calculator_class.__init__).parameters
        for param_name, param in params.items():
            if param_name == "self":
                continue
            if param_name not in parameters:
                parameters[param_name] = [employment_type.title]
            else:
                parameters[param_name].append(employment_type.key)

    for name, employment_types in parameters.items():
        parser.add_argument(
            f"--{name.replace('_', '-')}",
            help=_("Applies to: {list}").format(list=", ".join(employment_types)),
        )

    return parser


def main():
    parser = get_app_parser()
    args = vars(parser.parse_args())

    # Get employment type names and remove from args
    employment_type_keys = list(set(args['employment_type'])) if args['employment_type'] else []
    args.pop('employment_type', None)

    ui_key = args['user_interface'] if args['user_interface'] else available_user_interfaces[0].key
    ui = get_ui_class(ui_key)
    args.pop('user_interface', None)

    # Convert the rest of args to employment type class kwargs
    args = {key.replace('-', '_'): value for key, value in args.items()}

    employment_type_classes = [et(**args) for et in available_employment_types if et.key in employment_type_keys]
    ui(employment_type_classes).run()


if __name__ == "__main__":
    main()
