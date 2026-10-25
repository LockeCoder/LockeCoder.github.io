# CS-300 Data Structures and Algorithms Portfolio

This repository contains my CS-300 portfolio project for the ABCU advising assistance program. The project demonstrates data structure analysis, algorithm selection, C++ implementation, CSV file parsing, input validation, and maintainable software design.

## Project Overview

The main problem I addressed was creating an advising assistance program for ABCU academic advisors.

The program needed to load course data from a CSV file, display available courses in alphanumeric order, and allow users to retrieve information for a specific course, including prerequisites. This required building a data management system that could organize course records, support quick lookups, validate input, and present course information clearly to the user.

## Repository Contents

- `ProjectTwo.cpp` - Final C++ advising assistance program
- `CS 300 ABCU_Advising_Program_Input.csv` - Course input data
- `Project One.docx` - Data structure analysis and pseudocode
- `2-3 Assignment Vector Sorting.docx` - Vector sorting assignment
- `4-2 Assignment Hash Tables.docx` - Hash table assignment
- `5-2 Assignment Binary Search Tree.docx` - Binary search tree assignment
- `Case 1 and 2.png` - Program testing screenshot
- `Case 2 and 3.png` - Program testing screenshot
- `Case 3 and 4.png` - Program testing screenshot
- `Case 4 and 5.png` - Program testing screenshot
- `Input and Output Test with Case 9.png` - Exit and input/output test screenshot
- `README.md` - Repository documentation

## Data Structure Approach

For the final advising program, I used a hash table because it supports efficient course lookup by course number.

This was appropriate for the project because academic advisors need to search for course information quickly and retrieve prerequisite details without scanning the entire dataset manually.

The project also included analysis of other data structures, including vectors and binary search trees. Comparing these structures helped show how data organization affects runtime efficiency, lookup speed, sorting behavior, and maintainability.

## Program Features

- Loads course data from a CSV file
- Parses course number, course title, and prerequisites
- Stores course records in a hash table
- Displays all loaded courses
- Prints courses in alphanumeric order
- Looks up a specific course by course number
- Displays prerequisite information for a selected course
- Validates menu input
- Handles missing files and malformed course data
- Provides a menu-driven console interface

## Build and Run

### Requirements

- C++17 or newer
- Visual Studio, g++, or another C++ compiler

### Input File

The program uses this CSV input file:

```text
CS 300 ABCU_Advising_Program_Input.csv
```

### Compile with g++

```bash
g++ ProjectTwo.cpp -o ProjectTwo
```

### Run on macOS/Linux

```bash
./ProjectTwo
```

### Run on Windows

```bash
ProjectTwo.exe
```

## Menu Options

The program menu allows the user to:

1. Load course data
2. Display all courses
3. Display course information
4. Display a sorted list of courses
5. Print a course and prerequisites
9. Exit

## Skills Demonstrated

- C++ programming
- Data structure analysis
- Hash table implementation
- CSV file parsing
- Input validation
- Error handling
- Alphanumeric sorting
- Menu-driven console application design
- Requirements-based implementation
- Algorithmic thinking
- Technical reflection and documentation

## Portfolio Reflection

### What Was the Problem You Were Solving in the Projects for This Course?

The main problem I addressed was creating an advising assistance program for ABCU academic advisors.

The program needed to load course data efficiently, display all available courses in alphanumeric order, and allow users to retrieve information on specific courses, including prerequisites. This required building a robust data management system to handle course data and support quick lookups.

### How Did You Approach the Problem? Why Are Data Structures Important to Understand?

I approached the problem by focusing on data organization and retrieval efficiency.

Based on my analysis from Project One, I decided to use a hash table for this task because it supports fast data access, which is ideal for applications requiring frequent searches.

Understanding data structures is essential in software development because they directly impact a program's efficiency, speed, and scalability. By selecting a hash table, I could ensure that course lookups and data manipulation operations were optimized for the user's needs.

### How Did You Overcome Any Roadblocks You Encountered?

I encountered roadblocks such as managing user input validation and file errors. To overcome these, I implemented error handling for file operations and designed a user input validation function to support smooth interaction with the menu.

Testing was also important for identifying and fixing unexpected behavior, such as handling empty files or malformed data entries. This improved the reliability of the program.

### How Has Your Work on This Project Expanded Your Approach to Designing Software and Developing Programs?

This project reinforced the importance of planning and analyzing the problem before coding. By developing pseudocode and comparing different data structures, I was able to understand the tradeoffs before choosing the final implementation.

This approach helped me focus on building a scalable and efficient program while keeping the user experience in mind.

### How Has Your Work on This Project Evolved Regarding How You Write Maintainable, Readable, and Adaptable Programs?

Working on this project highlighted the need for clear code structure and documentation. To improve readability, I used inline comments, meaningful variable names, and modular functions.

I also focused on keeping the code adaptable for future requirements, such as adding new features, improving validation, or expanding reporting options. The experience improved my approach to writing maintainable code so others and my future self can understand and expand it.

## Project Value

This project shows my ability to analyze a problem, compare data structure options, select an appropriate implementation strategy, and build a functional C++ console application.

It is strongest for demonstrating foundational software engineering skills, algorithmic thinking, data handling, input validation, and maintainable program design.

## Future Improvements

- Add a `.gitignore` file for C++ and Visual Studio artifacts
- Add clearer Visual Studio build/run instructions
- Organize documents and screenshots into `docs/` and `media/` folders
- Add more defensive validation for malformed CSV rows
- Add more detailed error messages for invalid course data
- Add unit tests for CSV parsing and course lookup logic

## Academic Portfolio Notice

This repository is shared as an academic portfolio artifact. It may include coursework documentation and assignment-specific material created for an educational setting.

Please do not reuse, submit, or redistribute this work as your own.
