portion_down_payment = 0.25
investments_annual_return = 0.04
total_cost = 1000000
semi_annual_raise = 0.07

def savings(annual_salary, portion_saved):
    current_saving = 0
    monthly_saved = ( annual_salary / 12.0 ) * portion_saved
    down_payment = total_cost * portion_down_payment

    for m in range(1,37):
        current_saving += current_saving * investments_annual_return / 12 + monthly_saved
        if not m%6:
            annual_salary += annual_salary * semi_annual_raise
            monthly_saved = ( annual_salary / 12.0 ) * portion_saved

    return current_saving

def best_portion_saved_rate(annual_salary):
    down_payment = total_cost * portion_down_payment
    epsilon = 100
    low= 1
    high = 10000
    mid = (low + high)/2
    step = 0
    while low <= high:
        if abs(savings(annual_salary, mid/10000) - down_payment) <= epsilon:
            break
        if savings(annual_salary, mid/10000) < down_payment:
            low = mid+1
        else:
            high = mid-1
        mid = (low + high)/2
        step += 1
    
    if (low>high):
        return [0, -1]
    else:
        return [mid/10000, step+1]

starting_salary = int(input('Enter your starting salary: '))
best_rate, step = best_portion_saved_rate(starting_salary)
if (step==-1):
	print('It is not possible to pay the down payment in three years.')
else:
	print('Best savings rate: %.4f\nSteps in bisection search: %d'%(best_rate, step))