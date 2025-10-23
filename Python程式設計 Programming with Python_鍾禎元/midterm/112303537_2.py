# 建立空清單
numbers = []

while True:
    entry = input("Enter a number or press Enter to quit: ")
    if entry == "":   # 若輸入空白代表結束
        break
    else:
        numbers.append(float(entry))  # 轉為數字後加入清單

# 若有輸入資料才計算
if len(numbers) > 0:
    total = sum(numbers)
    average = total / len(numbers)
    print(f"The sum is {total:.1f}")
    print(f"The average is {average:.1f}")
# 若直接輸入enter跳出未輸入數字
else:
    print("No numbers were entered.")