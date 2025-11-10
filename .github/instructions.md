## Programming Fundamentals COIT 11222

### Assessment 2 - Python Console Programs

### Objectives:

This assessment focuses on applying key Python programming concepts in a more advanced, real-world
scenario. You are required to design, implement, and test a Python application that demonstrates your
understanding of file handling, exception handling, and object-oriented programming (classes and
objects).

### Assignment specification:

#### Assessment Task: Car Inventory Tracker

**Problem Description:** You are tasked with building a car inventory tracker for a car sale company. The system should allow staff to track various types of cars received and sold.

**Dataset:** The dataset is in the form of a csv file. The first line contains the name of fields. Below is the datafile.

#### Sample Input File (carinventory.txt)

```
carbrand,received,sold
BMW,20,
Hyundai,40,4 0
Mercedes,15,
Mazda, 50 , missing data
Audi, nine ,
Skoda,10,
```

**Task Requirements:** Please note that you can make reasonable assumptions (such as for the exact layout of the output) to develop the program. Just make sure to follow guidelines below.

The application should:

1. Read car inventory data from a text file.
2. Create class with appropriate attribute to represent car data.
3. Handle errors such as missing data, bad data formats
4. Print a summary report of the car inventory.
5. Implement a search feature wherein users should be able to search if a car brand is available for sale. Users should be asked to input a car brand name, if the item exists in the supply data, then details such as number of car available for sale displayed. If item is not found in data, ‘Item not found’ message should be displayed.
6. Implement a search feature wherein users should be able to search all cars that are available for
   sale. This function should not take any input and simply print all car brands that have got stock
   available for sale. For example, in the data that has been provided (Hyundai,40,4 0 ), Hyundai is not
   available for sale as store has sold all the 40 items it received. The data provided for BMW is
   (BMW,20,5) and this means BMW is available for sale as store received 20 items of BMW but sold only
   5 so far.
7. You can make reasonable assumptions to create a menu for the user giving option to either print summary report, search car by brand name, search all cars that are available for sale.

**Your program must run without errors and include comments/docstrings.**

### Marking Criteria / Rubric (Total: 12 Marks):

- Correct implementation of class and methods = 3 marks
- Effective exception handling = 3 marks
  Output formatting and logic correctness = 3 marks
- Code readability, comments and structure = 3 marks

Total of 12 marks available.
