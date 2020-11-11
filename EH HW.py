#1
f
#3
l
#5
b
#7
i
#9
s
#11
o
#13
g
#15
n
#17
d
#19
h
#21
r
#23
You must enter a number.
#25
string index out of range
#25
string index out of range
Oops
#27
File Salaries.txt contains an invalid salary.
Thank you for using our program.
#29
while True:
    try:
        n = int(input("Enter a nonzero integer: "))
        reciprocal = 1/n
        print("The reciprocal of {0} is {1:,.3f}".format(n, reciprocal))
        break
    except ValueError:
        print("You did not enter a nonzero integer. Try again.")
    except ZeroDivisionError:
        print("You entered zero. Try Again.")
    
