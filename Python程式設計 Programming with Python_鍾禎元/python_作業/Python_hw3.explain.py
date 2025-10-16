total = 0

for i in range(1, 101):
    ##total += sum(int(digit) for digit in str(i))
    ##for digit in str(i)-->逐一取出字串中的每個字元
    ##int(digit)-->將字元轉為整數

    for digit in str(i):
        total += int(digit)
        print("total+",digit ,"=" ,total)

    print("i=" ,i)

print("The total sum of digits from 1 to 1,000,000 is {:,}".format(total))
print("The total sum"+total+ "of digits from 1 to 1,000,000 is {:,}".format(total))