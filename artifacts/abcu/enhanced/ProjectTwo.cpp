#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <algorithm>  // for std::sort
#include <limits>     // for numeric_limits
#include <sys/stat.h> // for checking file existence (platform independent)
#include <queue>
#include <unordered_set>
#include <functional>

using namespace std;

// Define a structure to hold course information
struct Course {
    string courseNumber;
    string title;
    vector<string> prerequisites;
};

// Function to check if a file exists
bool fileExists(const string& filePath) {
    struct stat buffer;
    return (stat(filePath.c_str(), &buffer) == 0);
}

// Trim surrounding whitespace, including CRLF line endings, from CSV fields.
string trimCsvField(const string& value) {
    const size_t first = value.find_first_not_of(" \t\r\n");
    if (first == string::npos) {
        return "";
    }

    const size_t last = value.find_last_not_of(" \t\r\n");
    return value.substr(first, last - first + 1);
}

// Function to parse a CSV line into a Course object
Course parseCourseLine(const string& line) {
    Course course;
    stringstream ss(line);
    string field;

    // Read and normalize the course number.
    if (getline(ss, field, ',')) {
        course.courseNumber = trimCsvField(field);
    }

    // Read and normalize the course title.
    if (getline(ss, field, ',')) {
        course.title = trimCsvField(field);
    }

    // Trim prerequisite codes and ignore empty CSV fields.
    while (getline(ss, field, ',')) {
        string prerequisite = trimCsvField(field);
        if (!prerequisite.empty()) {
            course.prerequisites.push_back(prerequisite);
        }
    }

    return course;
}

// Function to load courses from the CSV file into the hash table
unordered_map<string, Course> loadCoursesFromFile(const string& filePath) {
    unordered_map<string, Course> courses;
    ifstream file(filePath);

    // Check if the file is open
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << filePath << endl;
        return courses;  // Return empty map if file cannot be opened
    }

    string line;
    while (getline(file, line)) {
        // Ignore empty lines
        if (line.empty()) {
            continue;
        }

        // Parse the line into a Course object
        Course course = parseCourseLine(line);

        // Ensure the course has a course number and title (basic validation)
        if (course.courseNumber.empty() || course.title.empty()) {
            cerr << "Error: Invalid course data. Skipping line: " << line << endl;
            continue;  // Skip malformed lines
        }

        // Insert the course into the hash table
        courses[course.courseNumber] = course;
    }

    file.close();  // Close the file after reading
    return courses;
}


// Validate that every prerequisite references a course that exists.
bool validatePrerequisites(const unordered_map<string, Course>& courses) {
    bool valid = true;

    for (const auto& pair : courses) {
        const Course& course = pair.second;

        for (const string& prerequisite : course.prerequisites) {
            if (courses.find(prerequisite) == courses.end()) {
                cerr << "Warning: " << course.courseNumber
                     << " references missing prerequisite "
                     << prerequisite << "." << endl;
                valid = false;
            }
        }
    }

    return valid;
}

// Depth-first search helper used for cycle detection.
bool detectCycleDFS(
    const string& courseNumber,
    const unordered_map<string, Course>& courses,
    unordered_map<string, int>& state
) {
    // 0 = unvisited, 1 = currently visiting, 2 = finished
    state[courseNumber] = 1;

    auto courseIt = courses.find(courseNumber);
    if (courseIt == courses.end()) {
        return false;
    }

    for (const string& prerequisite : courseIt->second.prerequisites) {
        // Missing prerequisites are handled separately by validation.
        if (courses.find(prerequisite) == courses.end()) {
            continue;
        }

        if (state[prerequisite] == 1) {
            return true;
        }

        if (state[prerequisite] == 0 &&
            detectCycleDFS(prerequisite, courses, state)) {
            return true;
        }
    }

    state[courseNumber] = 2;
    return false;
}

// Detect circular prerequisite relationships.
bool hasPrerequisiteCycle(const unordered_map<string, Course>& courses) {
    unordered_map<string, int> state;

    for (const auto& pair : courses) {
        state[pair.first] = 0;
    }

    for (const auto& pair : courses) {
        if (state[pair.first] == 0 &&
            detectCycleDFS(pair.first, courses, state)) {
            return true;
        }
    }

    return false;
}

// Recursively print every prerequisite in a course's prerequisite chain.
void printPrerequisiteChainRecursive(
    const string& courseNumber,
    const unordered_map<string, Course>& courses,
    unordered_set<string>& currentPath,
    int depth
) {
    auto courseIt = courses.find(courseNumber);

    if (courseIt == courses.end()) {
        cout << string(depth * 4, ' ')
             << courseNumber << " [course not found]" << endl;
        return;
    }

    for (const string& prerequisite : courseIt->second.prerequisites) {
        cout << string(depth * 4, ' ') << "-> " << prerequisite;

        auto prereqIt = courses.find(prerequisite);

        if (prereqIt == courses.end()) {
            cout << " [course not found]" << endl;
            continue;
        }

        cout << " - " << prereqIt->second.title;

        if (currentPath.find(prerequisite) != currentPath.end()) {
            cout << " [cycle detected]" << endl;
            continue;
        }

        cout << endl;

        currentPath.insert(prerequisite);
        printPrerequisiteChainRecursive(
            prerequisite,
            courses,
            currentPath,
            depth + 1
        );
        currentPath.erase(prerequisite);
    }
}

// Display the complete prerequisite chain for one course.
void displayPrerequisiteChain(
    const unordered_map<string, Course>& courses,
    const string& courseNumber
) {
    auto courseIt = courses.find(courseNumber);

    if (courseIt == courses.end()) {
        cout << "Course not found." << endl;
        return;
    }

    cout << "\nPrerequisite chain for "
         << courseIt->second.courseNumber << " - "
         << courseIt->second.title << ":" << endl;

    if (courseIt->second.prerequisites.empty()) {
        cout << "No prerequisites." << endl;
        return;
    }

    unordered_set<string> currentPath;
    currentPath.insert(courseNumber);

    printPrerequisiteChainRecursive(
        courseNumber,
        courses,
        currentPath,
        1
    );
}

// Generate a prerequisite-valid course ordering using Kahn's algorithm.
vector<string> topologicalSort(
    const unordered_map<string, Course>& courses
) {
    unordered_map<string, int> indegree;
    unordered_map<string, vector<string>> dependents;

    for (const auto& pair : courses) {
        indegree[pair.first] = 0;
    }

    // Convert course -> prerequisite relationships into
    // prerequisite -> dependent relationships.
    for (const auto& pair : courses) {
        const Course& course = pair.second;

        for (const string& prerequisite : course.prerequisites) {
            if (courses.find(prerequisite) != courses.end()) {
                dependents[prerequisite].push_back(course.courseNumber);
                indegree[course.courseNumber]++;
            }
        }
    }

    // A min-priority queue keeps the output deterministic when multiple
    // courses are available at the same time.
    priority_queue<string, vector<string>, greater<string>> ready;

    for (const auto& pair : indegree) {
        if (pair.second == 0) {
            ready.push(pair.first);
        }
    }

    vector<string> ordering;

    while (!ready.empty()) {
        string current = ready.top();
        ready.pop();

        ordering.push_back(current);

        vector<string>& nextCourses = dependents[current];
        sort(nextCourses.begin(), nextCourses.end());

        for (const string& dependent : nextCourses) {
            indegree[dependent]--;

            if (indegree[dependent] == 0) {
                ready.push(dependent);
            }
        }
    }

    // If every course was not processed, a cycle exists.
    if (ordering.size() != courses.size()) {
        ordering.clear();
    }

    return ordering;
}

// Display a valid ordering in which prerequisites appear before courses
// that depend on them.
void displayValidCourseOrder(
    const unordered_map<string, Course>& courses
) {
    vector<string> ordering = topologicalSort(courses);

    if (ordering.empty() && !courses.empty()) {
        cout << "\nUnable to generate a valid course order." << endl;
        cout << "A circular prerequisite dependency exists." << endl;
        return;
    }

    cout << "\nPrerequisite-Valid Course Order:" << endl;

    for (const string& courseNumber : ordering) {
        const Course& course = courses.at(courseNumber);
        cout << course.courseNumber << " - " << course.title << endl;
    }
}

// Run structural validation on prerequisite relationships.
void displayPrerequisiteValidation(
    const unordered_map<string, Course>& courses
) {
    cout << "\nPrerequisite Validation:" << endl;

    bool referencesValid = validatePrerequisites(courses);
    bool cycleFound = hasPrerequisiteCycle(courses);

    if (referencesValid) {
        cout << "All prerequisite references match loaded courses." << endl;
    }

    if (cycleFound) {
        cout << "Cycle detected in prerequisite relationships." << endl;
    }
    else {
        cout << "No prerequisite cycles detected." << endl;
    }

    if (referencesValid && !cycleFound) {
        cout << "Course prerequisite structure is valid." << endl;
    }
}

// Function to display all courses
void displayCourses(const unordered_map<string, Course>& courses) {
    for (const auto& pair : courses) {
        const Course& course = pair.second;
        cout << "Course Number: " << course.courseNumber << ", Title: " << course.title << endl;

        if (!course.prerequisites.empty()) {
            cout << "Prerequisites: ";
            for (const string& prereq : course.prerequisites) {
                cout << prereq << " ";
            }
            cout << endl;
        }
        else {
            cout << "No prerequisites" << endl;
        }
    }
}

// Function to display information for a specific course
void displayCourseInfo(const unordered_map<string, Course>& courses, const string& courseNumber) {
    if (courses.find(courseNumber) != courses.end()) {
        const Course& course = courses.at(courseNumber);
        cout << "Course Number: " << course.courseNumber << ", Title: " << course.title << endl;

        if (!course.prerequisites.empty()) {
            cout << "Prerequisites: ";
            for (const string& prereq : course.prerequisites) {
                cout << prereq << " ";
            }
            cout << endl;
        }
        else {
            cout << "No prerequisites" << endl;
        }
    }
    else {
        cout << "Course not found." << endl;
    }
}

// Function to print a sorted list of courses
void PrintCourseList(const unordered_map<string, Course>& courses) {
    if (courses.empty()) {
        cout << "No courses available." << endl;
        return;
    }

    // Extract the course numbers and store them in a vector
    vector<string> courseNumbers;
    for (const auto& pair : courses) {
        courseNumbers.push_back(pair.first);  // Add the course number to the vector
    }

    // Sort the course numbers alphanumerically
    sort(courseNumbers.begin(), courseNumbers.end());

    // Display the sorted list of courses
    cout << "\nSorted List of Courses:" << endl;
    for (const string& courseNumber : courseNumbers) {
        const Course& course = courses.at(courseNumber);
        cout << "Course Number: " << course.courseNumber << ", Title: " << course.title << endl;
    }
}

// Function to print course information and prerequisites
void PrintCourse(const unordered_map<string, Course>& courses, const string& courseNumber) {
    // Check if the course exists in the hash table
    auto it = courses.find(courseNumber);
    if (it != courses.end()) {
        const Course& course = it->second;
        cout << "Course Number: " << course.courseNumber << ", Title: " << course.title << endl;

        if (!course.prerequisites.empty()) {
            cout << "Prerequisites: ";
            for (const string& prereq : course.prerequisites) {
                cout << prereq << " ";
            }
            cout << endl;
        }
        else {
            cout << "No prerequisites." << endl;
        }
    }
    else {
        cout << "Error: Course with number " << courseNumber << " not found." << endl;
    }
}

// Function to display the menu
void displayMenu() {
    cout << "\nMenu:" << endl;
    cout << "1. Load Course Data" << endl;
    cout << "2. Display All Courses" << endl;
    cout << "3. Display Course Information" << endl;
    cout << "4. Display Sorted List of Courses" << endl;
    cout << "5. Print Course and Prerequisites" << endl;  // New option for printing specific course info
    cout << "6. Display Complete Prerequisite Chain" << endl;
    cout << "7. Display Prerequisite-Valid Course Order" << endl;
    cout << "8. Validate Prerequisite Relationships" << endl;
    cout << "9. Exit" << endl;
    cout << "Enter your choice: ";
}

// Function to get validated user choice for menu
int getValidatedChoice() {
    int choice;
    while (true) {
        if (cin >> choice) {
            if (choice >= 1 && choice <= 9) {
                return choice;
            }
            else {
                cout << "Invalid choice. Please enter a number between 1 and 9: ";
            }
        }
        else {
            cout << "Invalid input. Please enter a valid number: ";
            cin.clear(); // Clear error state
            cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Ignore rest of the invalid input
        }
    }
}

int main() {
    unordered_map<string, Course> courses; // Hash table to hold courses
    string filePath;

    // Prompt the user for the file path before displaying the menu
    cout << "Enter the CSV file path (e.g., CS 300 ABCU_Advising_Program_Input.csv): ";
    getline(cin, filePath);  // Use getline to capture file path with spaces

    // Ensure file exists before proceeding
    if (!fileExists(filePath)) {
        cerr << "Error: File does not exist. Please check the file path." << endl;
        return 1;
    }

    // Load the courses from the file
    courses = loadCoursesFromFile(filePath);

    // Check if any courses were loaded
    if (courses.empty()) {
        cout << "No courses were loaded. Exiting program." << endl;
        return 1;
    }
    else {
        cout << "Courses loaded successfully!" << endl;
        displayPrerequisiteValidation(courses);
    }

    int choice = 0;
    // Loop to keep showing the menu until the user exits
    do {
        displayMenu();  // Show the menu
        choice = getValidatedChoice();  // Get validated user choice

        switch (choice) {
        case 1:
            // Re-load courses from the file (optional if you want to allow reloading)
            courses = loadCoursesFromFile(filePath);
            if (courses.empty()) {
                cout << "No courses were loaded." << endl;
            }
            else {
                cout << "Courses loaded successfully!" << endl;
                displayPrerequisiteValidation(courses);
            }
            break;

        case 2:
            // Display all loaded courses
            displayCourses(courses);
            break;

        case 3: {
            // Ask for a specific course number and display its information
            string courseNumber;
            cout << "Enter the course number: ";
            cin >> courseNumber;
            displayCourseInfo(courses, courseNumber);
            break;
        }

        case 4:
            // Display the sorted list of courses
            PrintCourseList(courses);
            break;

        case 5: {
            // Ask for a specific course number and print its prerequisites
            string courseNumber;
            cout << "Enter the course number: ";
            cin >> courseNumber;
            PrintCourse(courses, courseNumber);
            break;
        }

        case 6: {
            // Display the full prerequisite chain for a selected course.
            string courseNumber;
            cout << "Enter the course number: ";
            cin >> courseNumber;
            displayPrerequisiteChain(courses, courseNumber);
            break;
        }

        case 7:
            // Display a prerequisite-valid ordering using topological sorting.
            displayValidCourseOrder(courses);
            break;

        case 8:
            // Validate prerequisite references and check for cycles.
            displayPrerequisiteValidation(courses);
            break;

        case 9:
            cout << "Exiting program. Goodbye!" << endl;
            break;

        default:
            cout << "Invalid choice. Please enter a valid option." << endl;
            break;
        }

    } while (choice != 9);  // Repeat until the user selects "Exit"

    return 0;
}
