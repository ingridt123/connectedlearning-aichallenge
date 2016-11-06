import re
import string

# read in questions file
# qFile = input("Input questions file name: ")
qFile = "questions.txt"
with open(qFile, "r") as file:
    problems = file.readlines()

# read in answers file
# aFile = input("Input answers file name: ")
aFile = "answers.txt"
with open(aFile, "r") as file:
    answers = file.readlines()

# strip \n from answers
for a in range(len(answers)):
    answers[a] = answers[a].strip()

# statistics for error checking
total = 0       # total number of problems attempted
correct = 0     # total number of problems with correct answers

for problemString in problems:
    # print problem
    print("Question: " + problemString.strip())

    # add to total
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

    # check if units are the same and assign unit
    sameUnit = all(units[0] == item for item in units)
    unit = ""
    if sameUnit:
        possibility[0] += 5     # addition
        possibility[1] += 5     # subtraction
        unit = units[0]
    else:
        possibility[2] += 5     # multiplication
        possibility[3] += 5     # division
        # count number of occurrences of unit in problem and (TODO) units array
        problemUnitCount = []
        for u in units:
            problemUnitCount.append(problemWords.count(u))
        unitLargest = 0
        for c in range(len(problemUnitCount)):
            if problemUnitCount[c] > problemUnitCount[unitLargest]:
                unitLargest = c
        unit = units[unitLargest]

    # check if key words are in problem
    # TODO: differentiate possibilities more
    # TODO: more features -- e.g. structures, ordering of words, minus if key words not in?
    keyWords = [{"how": 1, "much": 1, "many": 1, "in": 4, "total": 4},
                {"how": 1, "much": 1, "many": 1, "away": 4, "left": 4},
                {"how": 1, "many": 1, "much": 1, "each": 3, "in": 4, "total": 4},
                {"how": 1, "many": 1, "much": 1, "each": 3, "distribute": 4, "equal": 4, "equally": 4}]
    for keyList in keyWords:
        currentIndex = keyWords.index(keyList)
        for word in keyList.keys():
            if word in problemWords:
                possibility[currentIndex] += keyList.get(word)

    # find largest possibility
    print("Possibilities: " + str(possibility))
    largest = 0
    for poss in range(len(possibility)):
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
                print("- " + dictOperators[i])
        right = False
    else:
        operator = dictOperators[largest]
        print("Operator: %s" % operator)
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
            answer = str(int(quotient)) + " " + unit

        # print out final answer
        print("MY ANSWER: %s" % answer)

        # check if answer is correct
        problemIndex = problems.index(problemString)
        if answer == str(answers[problemIndex]):
            right = True
        else:
            right = False

    if right:
        print("Correct!")
        correct += 1
    else:
        print("Incorrect.")

    print()

# print out statistics (error rate) after all problems have been attempted
print("--\nSTATISTICS")
print("Total: %i" % total)
print("Correct: %i" % correct)
percentage = correct / total * 100
print("Accuracy: %.2f%%" % percentage)
print("--")

