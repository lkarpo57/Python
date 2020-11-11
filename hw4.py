#1
Hw
#3
Enter the population growth as a percent: 2
The population will double in about 36.00 years.
#5
Your income tax is $499.00
#7
Why do clocks run clockwise?
Because they were invented in the northern hemisphere where sundials go clockwise.
#9
168 hours in a week
76 trombones in the big parade
#11
President Bush is a graduate of Yale.
President Obama is a graduate of Columbia.
#13
7
5
#15
Fredrick
#17
Total Cost: $106.00
#19
5
#21
When in the course of human events
#23
Enter grade on midterm exam: 85
Enter grade on final exam: 94
Enter type of student (Pass/Fail) or (Letter Grade): Letter Grade
Semester grade: A

Enter grade on midterm exam: 50
Enter grade on final exam: 62
Enter type of student (Pass/Fail) or (Letter Grade): Pass/Fail
Semester grade: Fail

Enter grade on midterm exam: 56
Enter grade on final exam: 67
Enter type of student (Pass/Fail) or (Letter Grade): Letter Grade
Semester grade: D
#25
def maximum(list1):
    largestNumber = list1[0]
    for number in list1:
        if number > largestNumber:
            largestNumber = number
    return largestNumber
#27
def main():
    word = input("Enter a word:")
    if isQwerty(word):
        print(word, "is a Qwerty word.")
    else:
        print(word, "is not a Qwerty word.")
    def isQwerty(word):
        word = word.upper()
        for ch in word:
            if ch not in "QWERTYUIOP":
                return False
        return True
    main()
#29
def main():
    opt1 = option1()
    opt2 = option2()
    print("Option 1 = ${0:,.2f}.".format(opt1))
    print("Option 2 = ${0:,.2f}.".format(opt2))
    if opt1 > opt2:
        print("Option 1 pays better.")
    elif opt1 == opt2:
        print("Options pay the same.")
    else:
        print("Option 2 is better.")
    def option1():
        sum = 0
        for i in range(10):
            sum += 100
        return sum
def option2():
    sum = 0
    daySalary = 1
    for i in range(10):
        sum += daySalary
        daySalary *= 2
    return sum
main()
#31
#Named constants.
WAGE_BASE = 117000 #There is no social security benefits
#tax on income above this level.
SOCIAL_SECURITY_TAX_RATE = 0.062 #6.2%
MEDICARE_TAX_RATE = 0.0145 #1.45%
ADDITIONAL_MEDICARE_TAX_RATE = .009 #0.9%
def main():
    ##Calculate FICA tax for a single employee.
    ytdEarnings, curEarnings, totalEarnings = obtainEarnings()
    socialSecurityBenTax = calculateBenTax(ytdEarnings, curEarnings, totalEarnings)
    calculateFICAtax(ytdEarnings, curEarnings, totalEarnings, socialSecurityBenTax)
def obtainEarnings():
    str1 = "Enter total earnings for this year prior to current pay period: "
    ytdEarnings = eval(input(str1)) #year-to-date earnings
    curEarnings = eval(input("Enter earnings for the current pay period:"))
    totalEarnings = ytdEarnings + curEarnings
    return(ytdEarnings, curEarnings, totalEarnings)
def calculateBenTax(ytdEarnings, curEarnings, totalEarnings): ##Calculate the Social Security Benefits tax.
    socialSecurityBenTax = 0
    if totalEarnings <= WAGE_BASE:
        socialSecurityBenTax = SOCIAL_SECURITY_TAX_RATE * curEarnings
    elif ytdEarnings < WAGE_BASE:
        socialSecurityBenTax = SOCIAL_SECURITY_TAX_RATE * (WAGE_BASE – ytdEarnings)
    return socialSecurityBenTax
def calculateFICAtax(ytdEarnings, curEarnings, totalEarnings, socialSecurityBenTax): ##Calculate and display the FICA tax.
    medicareTax = MEDICARE_TAX_RATE * curEarnings
    if ytdEarnings >= 200000:
        medicareTax += ADDITIONAL_MEDICARE_TAX_RATE * curEarnings
    elif totalEarnings > 200000:
        medicareTax += ADDITIONAL_MEDICARE_TAX_RATE * (totalEarnings - 200000)
        ficaTax = socialSecurityBenTax + medicareTax
        print("FICA tax for the current pay period: ${0:,.2f}".format(ficaTax))
main()
#1
24 blackbirds baked in a pie.
#3
Cost: $250.00
Shipping cost: $15.00
Total cost: $265.00
#5
Enter first grade: 88
Enter second grade: 99
Enter third grade: 92
[88, 92, 99]
#7
['Banana', 'apple', 'pear']
['apple', 'Banana', 'pear']
#9
nudge nudge
nudge nudge nudge nudge
#11
spam    and     eggs
spam and eggs
#13
George Washington
John Adams
#15
Amadeus
Joseph
Sebastian
Vaughan
#17
['M', 'S', 'a', 'l', 'o', 't']
['a', 'l', 'M', 'o', 'S', 't']
#19
VB Ruby Python PHP Java C++ C
#21
Python Java Ruby C++ PHP VB C
#23
-3 -2 4 5 6
#25
[10, 7, 6, 4, 5, 3]
#27
['BRRR', 'TWO']
#29
['c', 'a']
#31
names = ["George Boole", "Charles Babbage", "Grace Hopper"]
lastNames = [name.split()[-1] for name in names]
#33
A list consisting of the 50 states in uppercase characters.
#35
A list consisting of the 50 states ordered by the lengths of the names in ascending order.
#37
Valid
#39
Valid
#41
Not Valid
#43
Valid
#45
Not valid
#47
almost
#49
def main():
    ##Calculate the original cost of mailing a letter.
    weight = float(input("Enter the number of ounces:"))
    print("Cost: ${0:0,.2f}".format(cost(weight)))
def cost(weight):
    return 0.05 + 0.1 * ceil(weight - 1)
def ceil(x):
        if int(x) != x:
            return int(x + 1)
        else:
            return x main()
def cost(weight):
    return 0.05 + 0.1 * ceil(weight - 1)
def ceil(x):
    if int(x) != x:
        return int(x + 1)
    else:
        return x
main()
#51
def main():
    ##Determine whether two words are anagrams.
    string1 = input("Enter the first word or phrase:")
    string2 = input("Enter the second word or phrase:")
    if areAnagrams(string1, string2):
        print("Are anagrams.")
    else:
        print("Are not anagrams.")
    def areAnagrams(string1, string2):
        firstString = string1.lower()
        secondString = string2.lower()
    #In the next two lines, the if clauses remove all #punctuation and spaces.
        letters1 = [ch for ch in firstString if 'a' <= ch <= 'z']
        letters2 = [ch for ch in secondString if 'a' <= ch <= 'z']
        letters1.sort() letters2.sort()
        return (letters1 == letters2)
main()
#53
def main():
    ##Sort three names.
    pres = [("Lyndon", "Johnson"),("John", "Kennedy"),("Andrew", "Johnson")]
    pres.sort(key=lambda person: person[0]) #sort by first name
    pres.sort(key=lambda person: person[1]) #sort by last name
    for person in pres:
        print(person[1] +',', person[0])
main()
#55
def main():
    ##Sort New England states by land area.
    NE = [("Maine", 30840, 1.329), ("Vermont", 9217, .626), ("New Hampshire", 8953, 1.321), ("Massachusetts", 7800, 6.646), ("Connecticut", 4842, 3.59), ("Rhode Island", 1044, 1.05)]
    NE.sort(key=lambda state: state[1], reverse=True)
    print("Sorted by land area in descending order:")
    for state in NE:
        print(state[0], "", end="")
    print()
main()
#57
def main():
    ##Sort New England states by population density.
    NE = [("Maine", 30840, 1.329), ("Vermont", 9217, .626), ("New Hampshire", 8953, 1.321), ("Massachusetts", 7800, 6.646), ("Connecticut", 4842, 3.59), ("Rhode Island", 1044, 1.05)]
    NE.sort(key=sortByPopulationDensity)
    print("Sorted by population density in ascending order:")
    for state in NE:
        print(state[0], "", end="")
    print()
def sortByPopulationDensity(state):
    return state[2]/ state[1]
main()
#59
def main():
    ##Sort numbers by largest prime factor.
    numbers = [865, 1169, 1208, 1243, 290]
    numbers.sort(key=largestPrimeFactor)
    print("Sorted by largest prime factor:")
    print(numbers)
def largestPrimeFactor(num):
    n = num
    f = 2
    max = 1
    while n > 1:
        if n% f == 0:
            n = int(n/ f)
            if f > max:
                max = f
        else:
            f += 1
        return max
    main()
#61
def main():
    ##Sort numbers by the sum of their odd digits.
    numbers = [865, 1169, 1208, 1243, 290]
    numbers.sort(key=sumOfOddDigits, reverse=True)
    print("Sorted by sum of odd digits:")
    print(numbers)
def sumOfOddDigits(num):
    listNums = list(str(num))
    total = 0
    for i in range(len(listNums)):
        if int(listNums[i])% 2 == 1:
            total += int(listNums[i])
            return total
    main()
#63
def main():
    ##Display presidents ordered by length of first name.
    infile = open("USpres.txt", 'r')
    listPres = [pres.rstrip() for pres in infile]
    infile.close() listPres.sort(key=sortByLengthOfFirstName)
    for i in range(6):
        print(listPres[i])
def sortByLengthOfFirstName(pres):
    return len(pres.split()[0])
main()
#65
def main():
    ##Sort states by number of vowels in descending order.
    infile = open("States.txt", 'r')
    listStates = [state.rstrip() for state in infile]
    infile.close() listStates.sort(key=numberOfVowels, reverse=True)
    for i in range(6):
        print(listStates[i])
def numberOfVowels(word):
    vowels = ('a', 'e', 'i', 'o', 'u')
    total = 0
    for vowel in vowels:
        total += word.lower().count(vowel)
    return total
main()
#67
def main():
    ##Calculate new balance and minimum payment for a credit card.
    (oldBalance, charges, credits) = inputData()
    (newBalance, minimumPayment) = calculateNewValues(oldBalance, charges, credits)
    displayNewData(newBalance, minimumPayment)
def inputData():
    oldBalance = float(input("Enter old balance:"))
    charges = float(input("Enter charges for month:"))
    credits = float(input("Enter credits:"))
    return (oldBalance, charges, credits)
def calculateNewValues(oldBalance, charges, credits):
    newBalance = (1.015) * oldBalance + charges - credits
    if newBalance <= 20:
        minimumPayment = newBalance
    else:
        minimumPayment = 20 + 0.1 * (newBalance - 20)
    return (newBalance, minimumPayment)
def displayNewData(newBalance, minimumPayment):
    print("New balance: ${0:0,.2f}".format(newBalance))
    print("Minimum payment: ${0:0,.2f}".format(minimumPayment))
main()
#69
def main():
    ##Determine a person's earnings for a week.
    (wage, hours) = getWageAndHours()
    payForWeek = pay(wage, hours)
    displayEarnings(payForWeek)
def getWageAndHours():
    hoursworked = eval(input("Enter hours worked:"))
    hourlyWage = eval(input("Enter hourly pay:"))
    return(hourlyWage, hoursworked)
def pay(wage, hours):
    ##Calculate weekly pay with time-and-a-half for overtime.
    if hours <= 40:
        amount = wage * hours
    else:
        amount = (wage * 40) + ((1.5) * wage * (hours - 40))
    return amount
def displayEarnings(payForWeek):
    print("Week’s pay: ${0:,.2f}".format(payForWeek))
main()
#1
def main():
    iheight=int(input("Enter the initial height of the ball: "))
    ivelocity=int(input("Enter the initial velocity of the ball:"))
    height=projectMotion(iheight,ivelocity)
    print("The maximum height of the ball is {0:0.2f} feet".format(height))
    ground=projectGround(iheight,ivelocity)
    print("The ball will hit the ground after approximately {0:0.2f} seconds.".format(ground))
def projectMotion(iheight,ivelocity):
    t=ivelocity/32
    mHeight = (iheight + (ivelocity * t) - (16 * t**2))
    return mHeight
def projectGround(iheight,ivelocity):
    t=0
    gheight = (iheight + (ivelocity * t) - (16 * t**2))
    while(gheight>=0):
        t+=0.1
        gheight = (iheight + (ivelocity * t) - (16 * t**2))
    return t
main()
#2
def main():
    Number=int(input("Enter a  positive integer > 1: ")
    Lpf=largest(Number)
    print("Largest prime factor: ")
def largest(Number):
#3
def main():
    suffix=["septillion","sextillion","quintillion","quadrillion","trillion","billion","million","thousand"," "]
    number=123000004056777888999012345
    index=8
    while (number)>0:
        hundreths=number%1000
        number=number//1000
        if hundreths != 0:
            print(hundreths,suffix[index])
        index-=1
main()    
#4
def main():
    descrName =input("Enter name of item purchased : ")
    descrYear= int(input("Enter year purchased: "))
    descrCost= int(input("Enter cost of item: "))
    descrLife= int(input("Enter estimated life of item: "))
    descrType= input("Enter method of depriciation (SL or DDB): ")
    print("Item Description: ",descrName)
    print("Year Purchased: ",descrYear)
    print("Cost: $",descrCost)
    print("Estimated life: ",descrLife,"years")
    print("Method of depriciation: ",descrType)
    print("","Value at Beg of Yr.","Amount Deprec during Year","Total Deprc to End of Year")
    Tdep=0
    TdescrCost=descrCost
    for descrYear in range (descrYear,descrYear+5):
        if descrType == "DDB":
            descrType = "double-declining balance"
            dep=(descrCost*2)//descrLife
        else:
            descrType = "straight line"
            dep=descrCost//descrLife
        Tdep += dep
        print(descrYear,TdescrCost,dep,Tdep)
        TdescrCost -= dep
main()

#5
aWord=str(input("Enter a word: "))
lletter=None
counter=0
for letter in aWord:
    if lletter==None:
        lletter=letter
    else:
        if abs(ord(letter)-ord(lletter))==1:
            counter += 1
        else:
            counter += 0
        lletter=letter
    if counter >= 2:
        print("This is a thriple letter word")
    print(counter)
