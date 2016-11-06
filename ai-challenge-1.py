import re
import string


"""
Constants
"""

keyWords = [{"in": 4, "total": 4},
            {"away": 4, "left": 4},
            {"each": 3, "in": 4, "total": 4},
            {"each": 3, "distribute": 4, "equal": 4, "equally": 4}]
dictOperators = {0: "addition", 1: "subtraction", 2: "multiplication", 3: "division"}
unitCheck = ["how many", "how much"]
thresholdDifference = 2
thresholdWeight = 2

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

    # possibility for each operation -- addition, subtraction, multiplication, division (highest number is operator)
    possibility = [0, 0, 0, 0]

    # look for numbers
    problemWords = problemString.lower().split(" ")
    for i in range(len(problemWords)):
        problemWords[i] = re.sub(r"["+string.punctuation+"]", "", problemWords[i].strip())

    values = []
    units = []
    for i, word in enumerate(problemWords):
        if re.match(r"[0-9]", word, flags=re.IGNORECASE):
            values.append({
                "value": int(word),
                "unit": problemWords[i+1]
            })
        for case in unitCheck:
            try:
                final = i + len(case.split(" "))
                parts = " ".join([problemWords[w] for w in range(i, final)])
                if parts == case:
                    units.append(problemWords[final])
            except:
                continue

    valueUnits = [item["unit"] for item in values]
    sameUnit = True
    for unit in units:
        if not all([unit == item for item in valueUnits]):
            sameUnit = False
            break

    unit = units[0] or ""
    if sameUnit:
        possibility[0] += 5     # addition
        possibility[1] += 5     # subtraction
    else:
        possibility[2] += 5     # multiplication
        possibility[3] += 5     # division

    # check if key words are in problem
    # TODO: differentiate possibilities more
    # TODO: more features -- e.g. structures, ordering of words, minus if key words not in?
    """
    Weighting
    """
    # keyword weights
    for keyList in keyWords:
        currentIndex = keyWords.index(keyList)
        for word in keyList.keys():
            if word in problemWords:
                possibility[currentIndex] += keyList.get(word)

    largest = 0
    for poss in range(len(possibility)):
        if possibility[poss] > possibility[largest]:
            largest = poss

    withoutMax = possibility[0: largest] + possibility[largest+1:]
    secondLargest = withoutMax.index(max(withoutMax))
    if largest <= secondLargest:
        secondLargest += 1

    if abs(possibility[largest] - possibility[secondLargest]) <= thresholdDifference:
        filteredVals = [item["value"] for item in values]
        if filteredVals.index(max(filteredVals)) == len(filteredVals) - 1:
            if largest == 3 or secondLargest == 3:
                possibility[3] += thresholdWeight
            elif largest == 1 or secondLargest == 1:
                possibility[1] += thresholdWeight
        else:
            if largest == 2 or secondLargest == 2:
                possibility[2] += thresholdWeight
            elif largest == 0 or secondLargest == 0:
                possibility[0] += thresholdWeight

    # find largest possibility
    print("Possibilities: " + str(possibility))

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
        nums = [item["value"] for item in values]
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

# Compare the values of number occurences
# Change assumption for units
# number of items can determine the type of operation

