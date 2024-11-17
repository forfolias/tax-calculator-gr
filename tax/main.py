import argparse
from typing import List


from tax.employment_types import available_employment_types


def get_employment_type_class(employment_type_name):
    for cls in available_employment_types:
        if cls.title.lower() == employment_type_name.lower():
            return cls
    raise Exception(f"Unknown employment type: {employment_type_name}")


def select_employment_types() -> List[str]:
    from beaupy import select_multiple

    employment_types = available_employment_types
    print("Select employment type:")
    return select_multiple(
        options=[employment_type.title for employment_type in employment_types],
        minimal_count=1,
        ticked_indices=[0]
    )


def main():
    parser = argparse.ArgumentParser(
        description="Calculate net salary based on annual gross income per employment type."
    )

    # Adding --employment-type argument
    parser.add_argument(
        "--employment-type",
        "-e",
        action="append",
        choices=[employment_type.title.lower() for employment_type in available_employment_types],
        help="Specify employment type. Can be used multiple times"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive ask for any required missing values"
    )

    # Add all employment-types options
    options = {}
    for employment_type in available_employment_types:
        for k, v in employment_type.calculator.__dict__.items():
            is_callable = callable(v)
            if not callable(v) and not k.startswith("__") and not k.startswith("_abc_"):
                foo = k
        properties = [
            k for k, v in employment_type.calculator.__dict__.items()
            if not callable(v) and not k.startswith("__") and not k.startswith("_abc_")
        ]
        for option in properties:
            option = option.replace('_', '-')
            if option not in options:
                options[option] = {'employment_types': []}
            options[option]['employment_types'].append(employment_type.title)

    for option, option_data in options.items():
        applies_to = ", ".join(option_data['employment_types'])
        parser.add_argument(f"--{option}", help=f"Applies to: {applies_to}")

    args = vars(parser.parse_args())
    args = {key.replace('-', '_'): value for key, value in args.items()}

    # Process employment types
    if not args['employment_type']:
        employment_type_names = select_employment_types()
    else:
        employment_type_names = args['employment_type']
        args.pop('employment_type', None)

    interactive = args.pop('interactive', False)
    for employment_type_name in employment_type_names:
        employment_class = get_employment_type_class(employment_type_name)
        employment_type = employment_class(**args)

        if interactive:
            employment_type.input(**args)

        calculator = employment_type.get_calculator()

        print(f"Employment type: {employment_class.title}")
        print(f"Annual net income: {calculator.get_annual_net_salary():.2f}€")
        print(f"Monthly net income: {calculator.get_monthly_net_salary():.2f}€")


if __name__ == "__main__":
    main()
