# CS 300 — ABCU Advising Assistance | Enhanced Capstone Artifact

This project is my enhanced CS 300 advising assistance application, included in my CS 499 Computer Science Capstone portfolio at Southern New Hampshire University. It demonstrates data structure analysis, algorithm selection, C++ development, CSV parsing, prerequisite validation, and maintainable software design.

## Project Overview

The problem I addressed was creating an advising assistance program for ABCU academic advisors. The application loads a course catalog, displays courses in alphanumeric order, and retrieves course information, including prerequisites.

For my CS 499 enhancement, I extended the original application to analyze prerequisite relationships more thoroughly. The enhanced version can display complete prerequisite chains, identify missing references and circular dependencies, and generate a prerequisite-valid course sequence.

## Repository Contents

This `enhanced/` directory contains:

- `ProjectTwo.cpp` — Enhanced C++ advising assistance application.
- `CS 300 ABCU_Advising_Program_Input.csv` — Sample course catalog and prerequisite data.
- `README.md` — Documentation for the enhanced application.

Other capstone materials are maintained separately:

- [Original CS 300 application](../Original/) — Source code before the capstone enhancement.
- [CS 499 enhancement narrative](../4-2%20Milestone%20Three.docx) — Explanation of the changes and relevant course outcomes.
- [ABCU artifact overview](../README.md) — Parent portfolio directory.

Earlier CS 300 assignment documents and screenshots are not part of this enhanced-source directory.

## Data Structures and Algorithms

The application uses an `unordered_map` keyed by course number to support efficient average-case lookup of course records. Each course stores its prerequisites in a `vector<string>`. For alphabetically ordered listings, the program copies course numbers to a vector and sorts them.

The capstone enhancements add graph-based analysis of course dependencies:

- **Prerequisite validation:** Checks whether referenced prerequisite course numbers exist in the loaded catalog.
- **Cycle detection:** Uses depth-first search with visitation states to identify circular prerequisite relationships.
- **Complete prerequisite chains:** Recursively displays dependencies, including indirect prerequisites, and detects cycles while traversing.
- **Prerequisite-valid course order:** Uses Kahn's topological sorting algorithm and a min-priority queue to produce a deterministic order in which available prerequisites precede the courses that require them.

These additions extend the original hash-table approach into a practical dependency-analysis tool for academic advising.

## Program Features

- Loads course records from a CSV file.
- Parses course numbers, titles, and prerequisite fields.
- Trims surrounding whitespace and handles Windows-style line endings in CSV fields.
- Ignores blank prerequisite fields.
- Stores course information in an `unordered_map`.
- Displays all loaded courses or sorts course listings alphanumerically.
- Looks up individual courses and displays their prerequisites.
- Displays full prerequisite chains.
- Reports missing prerequisite references and circular dependencies.
- Generates a prerequisite-valid ordering when the dependency graph is acyclic.
- Validates menu selections and handles missing or empty input files.

## Build and Run

### Requirements

- A compiler supporting C++17 or newer, such as `g++` or Microsoft Visual C++.
- The sample CSV file included in this directory.

### Compile with g++

From the `enhanced/` directory:

```bash
g++ -std=c++17 -Wall -Wextra -pedantic ProjectTwo.cpp -o ProjectTwo
```

### Run on macOS/Linux

```bash
./ProjectTwo
```

### Run on Windows

If compiled to `ProjectTwo.exe` using a suitable Windows C++ toolchain:

```powershell
.\ProjectTwo.exe
```

When prompted for the CSV file path, enter:

```text
CS 300 ABCU_Advising_Program_Input.csv
```

The program expects a valid path to the course data file; running it from the `enhanced/` directory makes the example above work without an absolute path.

## Menu Options

1. Load course data.
2. Display all courses.
3. Display course information.
4. Display a sorted list of courses.
5. Print a course and its prerequisites.
6. Display a complete prerequisite chain.
7. Display a prerequisite-valid course order.
8. Validate prerequisite relationships.
9. Exit.

## Build and Functional Verification

The [GitHub Actions verification workflow](../../../.github/workflows/verify-abcu.yml) compiles both the original and enhanced C++ applications using C++17 and exercises their functional behavior.

**Verification status:** The October 25, 2026 GitHub Actions run #2 completed successfully. The configured checks covered course loading, lookup, sorting, invalid menu input, missing files, and the enhanced application's prerequisite chains, validation, topological sorting, cycle handling, and empty-file behavior.

This is automated build and functional-test evidence, not a claim that every possible input or platform has been tested.

## Skills Demonstrated

- C++17 programming and console application development.
- Hash-table design and average-case efficient lookup.
- Vectors, sorting, and algorithm selection.
- Directed graphs, depth-first search, and cycle detection.
- Topological sorting with Kahn's algorithm.
- CSV parsing, input normalization, and validation.
- Error handling and functional testing.
- Code maintenance, technical documentation, and GitHub Actions verification.

## Portfolio Reflection

### What Was the Problem You Were Solving in the Projects for This Course?

The main problem I addressed was creating an advising assistance program for ABCU academic advisors. The program needed to load course data efficiently, display available courses in alphanumeric order, and allow users to retrieve information about specific courses, including prerequisites. For the capstone enhancement, I extended the program so advisors could also examine dependency chains and determine whether prerequisite relationships were valid.

### How Did You Approach the Problem? Why Are Data Structures Important to Understand?

I approached the problem by focusing on how course data would be organized, searched, and displayed. Based on my analysis from Project One, I chose a hash table because it supports efficient average-case lookup by course number. I also used vectors for prerequisite lists and sorting.

The enhancement required treating prerequisites as a directed graph. Understanding data structures and graph algorithms made it possible to detect circular dependencies and produce a course ordering that respects prerequisites. These decisions affect the application's accuracy, efficiency, and usefulness to an academic advisor.

### How Did You Overcome Any Roadblocks You Encountered?

Input validation and file handling were initial challenges. I added checks for missing files, invalid menu selections, and malformed course records. During capstone verification, automated testing also revealed that blank CSV prerequisite fields and Windows-style line endings caused valid course references to be reported as missing. I corrected the parser to trim whitespace and ignore empty prerequisite entries, then reran the verification workflow successfully.

### How Has Your Work on This Project Expanded Your Approach to Designing Software and Developing Programs?

This project reinforced the importance of planning and analyzing a problem before coding. Comparing data structures helped me choose an appropriate way to store and retrieve courses. Extending the project with prerequisite validation, depth-first search, and topological sorting showed how an existing program can grow to support more demanding requirements without discarding its original design.

### How Has Your Work on This Project Evolved Regarding How You Write Maintainable, Readable, and Adaptable Programs?

Working on this project emphasized clear function boundaries, descriptive names, meaningful comments, and repeatable testing. The enhanced application separates course loading, lookup, dependency validation, chain traversal, and sorting into distinct operations. I also used automated compilation and functional checks to verify changes. This makes it easier to identify defects and extend the application without unintentionally breaking existing functionality.

## Project Value

This artifact demonstrates my ability to evaluate data structures, implement C++ algorithms, process external data, analyze dependencies, and improve an existing application. The contrast between the original and enhanced versions shows the progression from basic course lookup to more sophisticated prerequisite validation and course sequencing.

## Future Improvements

- Add a dedicated unit-testing framework for individual parsing and graph functions.
- Support quoted CSV fields and more detailed malformed-record diagnostics.
- Improve interactive handling of unexpected end-of-file input.
- Add more comprehensive test datasets and cross-platform build coverage.
- Expand documentation for Microsoft Visual Studio users.
- Separate parsing, domain logic, and the menu interface into reusable source files.

## Academic Portfolio Notice

This source code is shared as an academic portfolio artifact to demonstrate my work and learning. Please do not reuse, submit, or redistribute it as your own coursework.
