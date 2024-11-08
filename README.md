# Greek tax calculator

A command-line tool designed to calculate net income from an annual gross salary in Greece. By inputting your gross
salary and selecting an employment type, the tool applies Greek tax regulations to provide an estimate of your net
income. This tool is ideal for employees, freelancers, and contractors who need quick insights into their take-home pay.

## Disclaimer

Please note that the calculations provided are estimates based on general tax rules and may not be fully accurate.
This tool is not a substitute for professional accounting advice. Users should consult a certified accountant for
precise tax calculations.
The authors of this tool are not liable for any inaccuracies or financial outcomes resulting from its use.

## Supported employment types

- [x] Employee (IKA)
- [x] Freelancer
- [X] IKE
- [x] OE / EE


## Installation

### Virtual environment

Create and activate a new virtual environment:

```shell
python -m venv venv
source venv/bin/activate
```

### Install dependencies

```shell
pip install -r requirements.txt
```

## Run

### Interactive shell

You can run the tool in interactive mode in order to make it ask for all necessary options for the calculations.

```shell
./bin/tax-calculator --interactive
```

### Command

You can also provide all options through the command line.

```shell
./bin/tax-calculator --employment-type ika --annual-gross-salary 30000 --salaries-count 14 --kids-number 1
```

You can also use multiple employment types calculations

```shell
./bin/tax-calculator -e ika -e freelancer --annual-gross-salary 50000 --salaries-count 14 --kids-number 1 --expenses 3000 --prepaid-tax 0 --functional-year 1 --monthly-insurance-cost 240 
```