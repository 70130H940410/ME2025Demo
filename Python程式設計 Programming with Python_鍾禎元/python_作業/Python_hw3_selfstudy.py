"""
While loop 寫法

# 計算 1 到 1,000,000 的所有數字位數總和
i = 1
total = 0

while i <= 1000000:
    # 把 i 轉成字串，再把每個字元轉回整數加總
    for digit in str(i):
        total += int(digit)
    i += 1  # 下一個數字

print(f"The total sum of digits from 1 to 1,000,000 is {total:,}")

"""

# Calculate the total sum of all digits from 1 to 1,000,000
#For loop 寫法
total = 0

for i in range(1, 1000001):   # from 1 to 1,000,000 inclusive
    total += sum(int(digit) for digit in str(i))  # convert number to string, sum its digits

print("The total sum of digits from 1 to 1,000,000 is {:,}".format(total))
##print(f"The total sum of digits from 1 to 1,000,000 is {total:,}")


"""
範例比較

Python
total = 1234567.89
print(f"The total is {total:,}")      # 自動加千分位：1,234,567.89
print(f"The total is {total:,.2f}")   # 千分位 + 兩位小數：1,234,567.89

JavaScript
let total = 1234567.89;
console.log(`The total is ${total.toLocaleString()}`);  // 千分位
console.log(`The total is ${total.toLocaleString('en-US', {minimumFractionDigits: 2})}`); 
JS 沒有像 Python {total:,} 這樣的語法，
要用 Number.toLocaleString() 來達成相同效果。
"""

