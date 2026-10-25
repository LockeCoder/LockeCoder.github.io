#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <algorithm>  // for std::sort
#include <limits>     // for numeric_limits
#include <sys/stat.h> // for checking file existence (platform independent)

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

// Function to parse a CSV line into a Course object
Course parseCourseLine(const string& line) {
    Course course;
    stringstream ss(line);
    string temp;

    // Parse the course number
    getline(ss, course.courseNumber, ',');

    // Parse the course title
    getline(ss, course.title, ',');

    // Parse prerequisites (if any)
    while (getline(ss, temp, ',')) {
        if (!temp.empty()) {
            course.prerequisites.push_back(temp);
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