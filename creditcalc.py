import math
import sys


class IncorrectParameters(Exception):
    pass


parameters = ['p', 'a', 'n', 'i']
param_dict = {'p': "Enter the credit principal:\n",
              'a': "Enter the monthly payment:\n",
              'n': "Enter the number of periods:\n",
              'i': "Enter the credit interest:\n"}

message_dict = {'p': "Your credit principal",
                'a': "Your annuity payment"}


def factor_value(n, i):
    return (i * (1 + i) ** n) / ((1 + i) ** n - 1)


formulas = {'p': lambda a, n, i: int(a / factor_value(n, i)),
            'a': lambda p, n, i: math.ceil(p * factor_value(n, i)),
            'n': lambda p, a, i: math.ceil(math.log((a / (a - i * p)), 1 + i)),
            'd': lambda p, n, i, m: math.ceil((p / n) + i * (p - (p * (m - 1)) / n))}
formula_map = {'p': ['a', 'n', 'i'], 'a': ['p', 'n', 'i'],
               'n': ['p', 'a', 'i'], 'd': ['p', 'n', 'i', 'm']}


valid_params = {'diff': ['principal', 'periods', 'interest'],
                'annuity': ['principal', 'payment', 'periods', 'interest']}

symbols = {'principal': 'p', 'payment': 'a',
           'periods': 'n', 'diff': 'd', 'interest': 'i'}
param_names = {y: x for x, y in symbols.items()}


def get_params_values(param_str):
    x, y = param_str.split("=")
    x = x.replace('--', '')
    y = float(y)
    if x == 'interest':
        y = y / (100 * 12)
    return x, y


def print_months(value_):
    years, months = divmod(value_, 12)
    year_str = 'year' if years == 1 else 'years'
    month_str = 'month' if months == 1 else 'months'
    message = ""
    if years == 0:
        message = f"You need {months} {month_str}"
    elif months == 0:
        message = f"You need {years} {year_str}"
    elif value_ > 12:
        message = f"You need {years} {year_str} and {months} {month_str}"
    print(message + " to repay this credit!")


def print_values(calculation, p_dict_):
    if calculation == 'diff':
        total = 0
        periods = int(p_dict_['periods'])
        for m in range(1, periods + 1):
            pay = formulas['d'](p_dict_['principal'],
                                periods, p_dict_['interest'], m)
            print(f"Month {m}: paid out {pay}")
            total += pay
        print()
        print(f"Overpayment = {total - int(p_dict_['principal'])}")
    else:
        param = [x for x in valid_params[calculation] if x not in p_dict_.keys()][0]
        symbol = symbols[param]
        f_params = formula_map[symbol]
        value_ = formulas[symbol](*[p_dict_[param_names[p]] for p in f_params])
        if symbol == 'n':
            print_months(value_)
            print(f"Overpayment = {int(p_dict_['payment'] * value_ - p_dict_['principal'])}")
        else:
            print(f"{message_dict[symbol]} = {value_}!")
            if symbol == 'p':
                print(f"Overpayment = {int(p_dict_['payment'] * p_dict_['periods'] - value_)}")
            else:
                print(f"Overpayment = {int(value_ * p_dict_['periods'] - p_dict_['principal'])}")


command = sys.argv
if len(command) > 1:
    try:
        if len(command) == 5:
            c_type = command[1]
            if c_type == '--type=annuity' or c_type == '--type=diff':
                calc = c_type.replace("--type=", "")
                p_dict = dict()
                for x in command[2:]:
                    p_name, p_value = get_params_values(x)
                    if p_name in valid_params[calc] and p_value > 0:
                        p_dict[p_name] = p_value
                    else:
                        raise IncorrectParameters
                print_values(calc, p_dict)
            else:
                raise IncorrectParameters
        else:
            raise IncorrectParameters
    except IncorrectParameters:
        print('Incorrect parameters')
else:
    parameter = input("""What do you want to calculate?
    type \"n\" - for the number of months,
    type \"a\" - for the annuity monthly payment,
    type \"p\" - for the credit principal:
    """)

    r_params = [x for x in parameters if x != parameter]
    param_values = {x: float(input(param_dict[x])) for x in r_params}
    param_values['i'] = param_values['i']/100/12

    value = formulas[parameter](*param_values.values())

    if parameter != 'n':
        print(message_dict[parameter] + f" = {value}!")
    else:
        print_months(value)
