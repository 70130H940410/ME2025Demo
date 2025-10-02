#2.1-Numbers
""""
#Example1
print(3+2,3-2,3*2)
print(8/2,8**2,2*(3+4))

#Example2
speed=50
timeElapsed=14
distance=speed*timeElapsed
print(distance)

#Example3
a=2
b=3
print(abs(1-(4*b)))
print(int((a*b)+.8))
print(round(a/b,3))


#Example4
num1=6
num1+=1
num2=7
num2-=5
num3=8
num3/=2
print(num1,num2,round(num3))
num1=1
num1*=3
num2=2
num2**=3
print(num1,num2)



#Example5
totalInches=41
feet=totalInches//12
inches=totalInches%12
print(feet,inches)

"""

#2.2-Strings

"""
#Example1
print("python")
print("python"[1],"python"[5],"python"[2:4])
strl="hello world!"
print(strl.find('w'))
print(strl.find('x'))
print(strl.rfind('l'))


#Example2
print("python")
print("python"[-1],"python"[-4],"python"[-5:-2])
strl="spam & eggs"
print(strl[-2])
print(strl[-8:-3])
print(strl[0:-1])


#Example3
print("python"[2:],"python"[:4],"python"[:])
print("python"[-3:],"python"[:-3])


#Example4
fullName=input("enter a full name: ")
n= fullName.rfind(" ")
print("last name:",fullName[n+1:])
print("fist name:",fullName[:n])


#Example5
print(int("23"))
print(float("23"))
print(eval("23"))
print(eval("23.5"))
x=5
print(eval("23+(2*x)"))



#Example6(same as Example4)
fullName = input("enter a full name: ")
n= fullName.rfind(" ")
print("last name:",fullName[n+1:])
print("fist name:",fullName[:n])

"""

#2.3-Output

#Example1
print("01234567890123456")
print("a\tb\tc")
print("a\tb\tc".expandtabs(5))
print("nudge, \tnudge, \nwink, \twink.".expandtabs(11))

#Example2








