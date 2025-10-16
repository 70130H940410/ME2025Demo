total = 0

for i in range(1, 1000001):
    for digit in str(i):
        total += int(digit)

print("The sum of the digits in the numbers \nfrom 1 to one million is {:,}".format(total))