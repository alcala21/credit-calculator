import math

parameters = ['p', 'a', 'n', 'i']
param_dict = {'p': "Enter the credit principal:\n",
              'a': "Enter the monthly payment:\n",
              'n': "Enter the number of periods:\n",
              'i': "Enter the credit interest:\n"}

message_dict = {'p': "Your credit principal",
                'a': "Your annuity payment"}


def factor_value(n, i):
    return (i * (1 + i) ** n) / ((1 + i) ** n - 1)


param_formulas = {'p': lambda a, n, i: int(a / factor_value(n, i)),
                  'a': lambda p, n, i: math.ceil(p * factor_value(n, i)),
                  'n': lambda p, a, i: math.ceil(math.log((a / (a - i * p)), 1 + i))}

parameter = input("""What do you want to calculate?
type \"n\" - for the number of months,
type \"a\" - for the annuity monthly payment,
type \"p\" - for the credit principal:
""")

r_params = [x for x in parameters if x != parameter]
param_values = {x: float(input(param_dict[x])) for x in r_params}
param_values['i'] = param_values['i']/100/12

value = param_formulas[parameter](*param_values.values())

if parameter != 'n':
    print(message_dict[parameter] + f" = {value}!")
else:
    years, months = divmod(value, 12)
    year_str = 'year' if years == 1 else 'years'
    month_str = 'month' if months == 1 else 'months'
    message = ""
    if years == 0:
        message = f"You need {months} {month_str}"
    elif years == 1:
        message = f"You need {years} {year_str}"
    elif value > 12:
        message = f"You need {years} {year_str} and {months} {month_str}"
    print(message + " to repay this credit!")
