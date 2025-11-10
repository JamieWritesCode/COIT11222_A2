# Assessment Context: COIT11222 Car Inventory Tracker

## 1. Assignment Overview

Your task is to assess a Python console application designed to track a car inventory. The student's requirements (which were provided to them) are detailed in `.github/instructions.md`.

**Core Functional Requirements (from student instructions):**

- The program must read data from a text file named `carinventory.txt`.
- The program must use a **Python class** to represent the car data.
- The program must **gracefully handle errors** in the data file (like missing or bad data) _without crashing_.
- The program must provide a text-based menu with three options:
  1.  Print a summary report.
  2.  Search for a car by brand name.
  3.  List all cars that are available for sale (`received` > `sold`).

## 2. Test Harness & Data

To ensure a fair and consistent assessment, you **must create the `carinventory.txt` file** in the project's root directory _before_ running the student's script.

**File Content for `carinventory.txt`:**
You must use this _exact_ content. The "Mazda" and "Audi" lines are intentionally malformed to test error handling.

carbrand, received, sold BMW,20,5 Hyundai, 40,40 Mercedes, 15,5 Mazda, 50, missing data Audi, nine,5 Skoda, 10,2

## 3. Setup & Execution Instructions

1.  **Check for Dependencies:** Look for a `requirements.txt` file. If it exists, install it using `pip install -r requirements.txt`. If not, assume the project uses only the Python standard library.
2.  **Create Test File:** Create the `carinventory.txt` file (from Section 2) in the same directory as the main Python script.
3.  **Identify Main Script:** Locate the main runnable Python file (e.g., `main.py`, `app.py`, `assignment2.py`).
4.  **Execute:** Run the main script (e.g., `python main.py`).

## 4. Functional Test Plan

You must follow these test steps _exactly_ to check the program's functionality.

- **Test 1: Startup & Error Handling**

  - **Action:** Run the main Python script.
  - **Expected:** The program **must not crash**. It should load successfully, likely printing a warning or error message for the "Mazda" and "Audi" lines, and then display the main menu.

- **Test 2: Summary Report**

  - **Action:** At the menu, select the option for "Summary Report".
  - **Expected:** A formatted report is printed showing all _validly loaded_ cars (BMW, Hyundai, Mercedes, Skoda).

- **Test 3: Search by Brand (Found)**

  - **Action:** At the menu, select "Search by Brand". When prompted, enter `BMW`.
  - **Expected:** The program displays the correct details for BMW (e.g., "Received: 20, Sold: 5, Available: 15").

- **Test 4: Search by Brand (Not Found)**

  - **Action:** At the menu, select "Search by Brand". When prompted, enter `Ford`.
  - **Expected:** The program prints an "Item not found" message.

- **Test 5: List Available Cars (Logic Check)**
  - **Action:** At the menu, select "List all available cars".
  - **Expected:** The program prints a list that **includes** BMW, Mercedes, and Skoda. The list **must exclude** Hyundai (as `received` 40 - `sold` 40 = 0).

## 5. Marking Rubric (Total 12 Marks)

You must assign a score for each criterion based on your observations from the code and the test plan.

| Criteria                                           | Max Marks | What to Look For (Expectations)                                                                                                                                                                                                                                                                                                                  |
| :------------------------------------------------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Correct implementation of class and methods** | 3         | **3 (High):** A `class` is correctly defined for car data. The program uses this class (e.g., stores data as a list of `Car` objects). <br> **1-2 (Mid):** A class is defined but not used effectively (e.g., data is kept in parallel lists/dictionaries). <br> **0 (Low):** No `class` is used.                                                |
| **2. Effective exception handling**                | 3         | **3 (High):** **Test 1 Passed.** The program _did not crash_ on startup. It correctly handled both the `ValueError` ("nine") and the `IndexError` ("missing data"). <br> **1-2 (Mid):** The program handled _one_ error but crashed on the other. <A\*0 (Low):\*\* **Test 1 Failed.** The program crashed on startup.                            |
| **3. Output formatting and logic correctness**     | 3         | **3 (High):** **Tests 2, 3, 4, and 5 all passed.** The logic for "available cars" (Test 5) and the search function (Tests 3, 4) was correct. Output is clean. <br> **1-2 (Mid):** One or more tests (2-5) failed, or the logic/formatting was incorrect. <br> **0 (Low):** Multiple tests failed, or the features were not implemented.          |
| **4. Code readability, comments and structure**    | 3         | **3 (High):** Student name/ID is present in comments. Code is well-structured (e.g., uses functions for menu items). Clear comments/docstrings are used. <br> **1-2 (Mid):** Code is messy (e.g., all in one global script), comments are sparse, or student ID is missing. <br> **0 (Low):** Code is unreadable, uncommented, and unstructured. |

## 6. Required Output Format

You must provide your assessment in the following markdown format. Do not add any conversational text.

---

### **Assessment: [Student ID]**

**Overall Feedback:** [Provide 1-2 sentences summarizing the student's work, highlighting strengths and key areas for improvement.]

| Criteria                     |      Mark      | Justification                                                        |
| :--------------------------- | :------------: | :------------------------------------------------------------------- |
| 1. Class and Methods         |     [0-3]      | [Brief justification for the score]                                  |
| 2. Exception Handling        |     [0-3]      | [Brief justification. **State clearly if Test 1 passed or failed.**] |
| 3. Output and Logic          |     [0-3]      | [Brief justification, noting results of Tests 2-5.]                  |
| 4. Readability and Structure |     [0-3]      | [Brief justification for the score]                                  |
| **Total**                    | **[Sum] / 12** |                                                                      |
