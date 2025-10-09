"""
num1 = eval(input("Enter the first number:"))
num2 = eval(input("Enter the second number:"))

if num1 > num2 :
    largerValue = num1
else:
    largerValue = num2

(1) The larger value is"：字串常數，會原封不動地印出。

(2) ,：在 print() 裡，逗號會讓不同項目間自動插入一個空格。

(3) str(largerValue)：將變數 largerValue（可能是數字）轉成字串。

(4) + "."：把句點接在數值後面，讓輸出更像一個完整句子。

print("The larger value is",str(largerValue)+".")

"""




"""

color = input("Enter a color 'BLUE' or 'RED' :")
mode = input("Enter a mode 'STEADY' or 'FLASHING' :")
color = color.upper()
mode = mode.upper()
result = ""

if color == "BLUE":
    if mode == "STEADY":
        result = "Clear view."
    else:
        result = "Cloud Due."

print(result)

"""




"""

gpa = eval(input("Enter your gpa:"))

if gpa >= 3.9:
    honors = "summa cum laude."
elif gpa >= 3.6:
    honors = "magna cum laude."
elif gpa >= 3.3:
    honors = "cum laude."
elif gpa >= 2:
    honors = "."

print("You graduate"+honors)

"""