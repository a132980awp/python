current_saving = 0
portion_down_payment = 0.25
r = 0.04
months = 0

annual_salary = int(input('Enter your annual salary: '))
portion_saved = float(input('Enter the percent of salary to save, as a decimal: '))
total_cost = int(input('Enter the cost of your dream home: '))

monthly_saved = ( annual_salary / 12 ) * portion_saved
down_payment = total_cost * portion_down_payment

while current_saving < down_payment:
    current_saving += current_saving * r / 12 + monthly_saved
    months += 1

print("Number of months:", months)