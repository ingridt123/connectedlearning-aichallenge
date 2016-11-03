import re
import string

# read in questions file
qFile = input("Input questions file name: ")
with open(qFile, "r") as file:
    problems = file.readlines()

# read in answers file
aFile = input("Input answers file name: ")
with open(aFile, "r") as file:
    answers = file.readlines()

# strip \n from answers
for a in range(len(answers)):
    answers[a] = answers[a].strip()

# statistics for error checking
total = 0       # total number of problems attempted
correct = 0     # total number of problems with correct answers

for problemString in problems:
    total += 1

    # dictionary for corresponding operation in list
    dictOperators = {0: "addition", 1: "subtraction", 2: "multiplication", 3: "division"}

    # possibility for each operation -- addition, subtraction, multiplication, division (highest number is operator)
    possibility = [0, 0, 0, 0]

    # look for numbers
    problemWords = problemString.lower().split(" ")
    for i in range(len(problemWords)-1):
        problemWords[i] = re.sub(r"["+string.punctuation+"]", "", problemWords[i].strip())

    nums = []
    indexes = []
    for w in range(len(problemWords)):
        if re.match(r"[0-9]", problemWords[w]):
            nums.append(int(problemWords[w]))
            indexes.append(w)

    # look for units
    units = []
    for index in indexes:
        units.append(problemWords[index+1])

    # check if units are the same
    sameUnit = all(units[0] == item for item in units)
    unit = ""
    if sameUnit:
        possibility[0] += 1     # addition
        possibility[1] += 1     # subtraction
        unit = units[0]
    else:
        possibility[2] += 1     # multiplication
        possibility[3] += 1     # division
        unitCount = []
        for u in units:
            unitCount.append(problemWords.count(u))
        unitLargest = 0
        for c in range(len(unitCount)):
            if unitCount[c] > unitCount[unitLargest]:
                unitLargest = c
        unit = units[unitLargest]

    # TODO: differentiate possibilities more
    # check if key words are in problem -- TODO: weight different words
    # TODO: more features -- e.g. structures, ordering
    keyWords = [["how", "much", "many", "in", "total?"], ["how", "much", "many", "away", "left"], ["each", "how",
                "many", "much", "in", "total"], ["distribute", "equal", "equally"]]
    for keyList in keyWords:
        currentIndex = keyWords.index(keyList)
        for word in keyList:
            if word in problemWords:
                possibility[currentIndex] += 1

    # find largest possibility
    print(possibility)
    largest = 0
    for poss in range(len(possibility)-1):
        if possibility[poss] > possibility[largest]:
            largest = poss

    # test for later on whether answer is correct
    right = False

    # find operator based on largest possibility
    count = possibility.count(possibility[largest])
    if count > 1:
        print("Could not recognize operation. Could be:")
        countIndexes = []
        for i in range(len(possibility)):
            if possibility[i] == possibility[largest]:
                print(dictOperators[i])
        right = False
    else:
        operator = dictOperators[largest]
        answer = ""
        if operator is "addition":                      # addition
            sum = 0
            for num in nums:
                sum += num
            answer = str(sum) + " " + unit
        elif operator is "multiplication":              # multiplication
            product = 1
            for num in nums:
                product *= num
            answer = str(product) + " " + unit
        elif operator is "subtraction":                 # subtraction
            nums.sort(reverse=True)
            difference = nums[0]
            for n in range(1, len(nums)):
                difference -= nums[n]
            answer = str(difference) + " " + unit
        else:                                           # division
            nums.sort(reverse=True)
            quotient = nums[0]
            for n in range(1, len(nums)):
                quotient /= nums[n]
            answer = str(quotient) + " " + unit

        # print out final answer
        print(answer)

        # check if answer is correct
        problemIndex = problems.index(problemString)
        if answer == str(answers[problemIndex]):
            right = True
        else:
            right = False

    if right:
        correct += 1

    print()

# print out statistics (error rate) after all problems have been attempted
print("--\nSTATISTICS")
print("Total: %i" % total)
print("Correct: %i" % correct)
percentage = correct / total * 100
print("Accuracy: %.2f%%" % percentage)
print("--")

