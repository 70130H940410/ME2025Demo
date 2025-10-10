
hourlyWage = eval(input("Enter hourly wage:"))
hoursWorked = eval(input("Enter number of hours worked:"))
if hoursWorked<=40:
    salary = hourlyWage*hoursWorked
elif hoursWorked>40:
    salary = (hourlyWage*40) + (1.5*hourlyWage*(hoursWorked-40))

print("Gross pay for week is $" + str(round(salary, 2)))


