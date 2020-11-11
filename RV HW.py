#1
A free throw by a basketball player who makes 75% of his or her free throws.
#3
The result of an at-bat by a baseball player with a .275 average.
#5
The random selection of two people to be co-chairs of a club.
#7
Randomly assigning starting positions in a one-mile race.
#9
import random
list1 = [chr(n) for n in range(ord('A'), ord('Z')+1)]
list2 = random.sample(list1, 3)
print(",".join(list2))
#11
import random
list1 = [n for n in range(2, 101, 2)]
list2 = random.sample(list1, 2)
print(list2[0], list2[1])
#13
import random
numberOfHeads = 0
for i in range(100):
    if(random.choice(["Head","Tail"]) == "Head"):
        numberOfHeads += 1
print("In 100 tosses, heads occured {0} times.".format(numberOfHeads))
#15
import random
allNumbers = [ n for n in range(1, 51)]
threeNumbers = random.sample(allNumbers, 3)
infile = open("StatesAlpha.txt", 'r')
line Number = 1
for line in infile:
    if lineNumber in threeNumbers:
        print(line.rstrip())
    lineNumber += 1
infile.close()
#17
import random
import pickle
NUMBER_OF_TRIALS = 10000

def main():
    totalNumberOfMatches = 0
    for i in range(NUMBER_OF_TRIALS):
        totalNumberOfMatches += matchTwoDecks()
    averageNumberOfMatches = totalNumberOfMatches / NUMBER_OF_TRIALS
    print("The average number of cards that")
    print("matched was {0:.3f}.".format(averageNumberOfMatches))
def matchTwoDecks():
    infile = open("DeckOfCardsList.dat", 'rb')
    deck1 = pickle.load(infile)
    infile.close()
    infile = open("DeckOfCardsList.dat", 'rb')
    deck2 = pickle.load(infile)
    infile.close()
    random.shuffle(deck1)
    random.shuffle(deck2)
    numberOfMatches = 0
    for i in range(52):
        if(deck1[i] == deck2[i]):
            numberOfMatches += 1
    return numberOfMatches
main()
#19
import random
whiteBalls = [num for num in range(1,60)]
whiteBallSelection = random.sample(whiteBalls, 5)
for i in range(5):
    whiteBallSelection[i] = str(whiteBallSelection[i])
print("White Balls: ".join(whiteBallSelection))
powerBall = random.randint(1,35)
print("Powerball:", powerBall)
#21
import random
coin = ['T', 'H']
result = ""
for i in range(32):
    result += random.choice(coin)
print(result)
if("TTTTT" in result) or ("HHHHH" in result):
    print("There was a run of five consecutive")
    print("same outcomes.")
else:
    print("There was not a run of five consecutive ")
    print("same outcomes.")
#23
import random
import pickle
def main():
    bridgeHand = getHand()
    print(" , ".join(bridgeHand))
    HCP = calculateHighCardPointCount(bridgeHand)
    print("HPC =", HCP)
def getHand():
    infile = open("DeckOfCardsList.dat", 'rb')
    deckOfCards = pickle.load(infile)
    infile.close()
    bridgeHand = random.sample(deckOfCards, 13)
    return bridgeHand
def calculateHighCardPointCount(bridgeHand):
    countDict{'A':4, 'K':3, 'Q':2, 'J':1}
    HPA = 0
    for card in bridgeHand:
        rank = card[0]
        if rank in "AKQJ":
            HPC += countDict[rank]
    return HPC
main()
