# CIS Connected Learning AI Challenge

### Task
Write a computer program that takes a "third-grade real-world math problem" as input, and produces the correct solution
as output. See example below:

> **Input:** If Rachel ate 276 grams of bacon and 147 grams of sausages, how much food did she eat in total?<br/>
> **Output:** 423 grams

<br/>

### Test Set of Questions
Modified from [http://www.k5learning.com/free-math-worksheets/third-grade-3/word-problems-mixed](http://www.k5learning.com/free-math-worksheets/third-grade-3/word-problems-mixed)

<br/>

### Methodology
- Possibility array checks for probability of each operator based on a number of parameters (e.g key words), which is
used at the end of the program to determine operator
- Key words (or group of words) for word problems of each operation were identified and weights given for the
importance of each
- Units checked (word after numbers) and possibilities added based on whether units are same/different

##### Assumptions
These are assumptions made when creating AI of the program.
- Word problems must be one of the four basic operators: addition, subtraction, multiplication or division
- Units must be the word after "how much" or "how many"
- For subtraction and division, there are no negative answers (no negatives in 3rd grade real-world problems)

##### Steps
1. Input questions and answers (2 separate text files) for list of questions and corresponding answers.
2. Find numbers in the problem and save them for later calculations.
3. Check units for similarity / difference to add to possibilities.
4. Check for key words / group of words in problem and add (if they are present) or subtract (if they aren't present) to
possibilities.
5. Determine operator by identifying highest possibility.
6. Calculate the answer based on the chosen operator and print out the answer with unit.
For each question, the program prints out information to ease readability and troubleshooting. See sample output below:

> Question 1: If Rachel ate 276 grams of bacon and 147 grams of sausages, how many grams of food did she eat in total?<br/>
> Same Unit? True<br/>
> Possibilities: [5, -10, -6, -17]<br/>
> Difference: 11<br/>
> Operator: addition<br/>
> MY ANSWER: 423 grams<br/>
> Correct!<br/>

After answering all the questions, the program prints out a statistical summary. See sample output below: 

> &#45;&#45;<br/>
> STATISTICS<br/>
> Total: 40<br/>
> Correct: 29<br/>
> Accuracy: 72.50%<br/>
> Wrong Questions: [20, 26, 27, 28, 29, 30, 33, 34, 35, 37, 40]<br/>
> &#45;&#45;
