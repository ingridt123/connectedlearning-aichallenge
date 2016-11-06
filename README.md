# CIS Connected Learning AI Challenge

### Task
Write a computer program that takes a "third-grade real-world math problem" as input, and produces the correct solution as output. See example below:
**Input:** If Rachel ate 276 grams of bacon and 147 grams of sausages, how much food did she eat in total?
**Output:** 423 grams

### Methodology (draft)
- Possibility array checks for probability of each operator based on a number of parameters (e.g. key words), which is used at the end of the program to determine operator for
- Units are determined by loading the word after each number in the problem -- if they are different, it is assumed that the unit that appears most is the correct unit for the answer
-