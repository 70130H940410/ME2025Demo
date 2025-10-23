# 輸入三個邊
a = float(input("Enter the first side: "))
b = float(input("Enter the second side: "))
c = float(input("Enter the third side: " ))

# 先找出最長邊（假設是直角邊對面的邊）
sides = [a, b, c]
sides.sort()  # 排序後 sides[2] 為最長邊

# 檢查畢氏定理a^2+b^2-c^2
if abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 1e-6:  #電腦在計算浮點數（小數）時，會有微小的誤差
    print("The triangle is a right triangle.")
else:
    print("The triangle is not a right triangle.")