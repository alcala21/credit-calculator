import math

principal = int(input("Enter the credit principal:\n"))
operation = input("""What do you want to calculate?
type \"m\" - for the number of months,
type \"p\" - for the monthly payment:\n""")

if operation == "m":
    pay = int(input("Enter the monthly payment:\n"))
    months = math.ceil(principal / pay)
    print(f"It takes {months} {'month' if months == 1 else 'months'} to repay the credit.")

elif operation == "p":
    months = int(input("Enter the count of months:\n"))
    pay = math.ceil(principal / months)
    message = f"Your monthly payment = {pay}"
    if principal % months != 0:
        remaining = principal - (months - 1) * pay
        message += f" with last monthly payment = {remaining}."
    print(message)
