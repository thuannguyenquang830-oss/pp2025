import math
import numpy as np # Import numpy
from operator import attrgetter # To help with sorting


class Student:
    """Represents a single student with an ID, name, and Date of Birth."""
    def __init__(self, student_id, name, dob):
        self._student_id = student_id
        self._name = name
        self._dob = dob
        self._gpa = 0.0 # Thêm thuộc tính để lưu GPA

    def get_id(self):
        """Returns the student's ID."""
        return self._student_id
        
    def get_name(self):
        """Returns the student's name."""
        return self._name

    def get_dob(self):
        """Returns the student's Date of Birth."""
        return self._dob
        
    def set_gpa(self, gpa):
        """Sets the calculated GPA for the student."""
        self._gpa = gpa
        
    def get_gpa(self):
        """Returns the student's GPA."""
        return self._gpa

    def list(self):
        """Displays the student's information (part of polymorphism requirement)."""
        # Thêm hiển thị GPA
        print(f"ID: {self._student_id}, Name: {self._name}, Date of Birth: {self._dob}, GPA: {self._gpa:.2f}")

    @staticmethod
    def input():
        """Static method to prompt for and create a new Student object."""
        student_id = input("    Student ID: ")
        name = input("    Student Name: ")
        dob = input("    Date of Birth (DoB): ")
        return student_id, Student(student_id, name, dob)




class Course:
    """Represents a single course with an ID and name and credit (new requirement)."""
    def __init__(self, course_id, name, credits=1): # Thêm credits mặc định là 1
        self._course_id = course_id
        self._name = name
        self._credits = credits # Thuộc tính mới: số tín chỉ
        
    def get_id(self):
        """Returns the course's ID."""
        return self._course_id
        
    def get_name(self):
        """Returns the course's name."""
        return self._name
        
    def get_credits(self):
        """Returns the course's credit."""
        return self._credits

    def list(self):
        """Displays the course's information (part of polymorphism requirement)."""
        print(f"ID: {self._course_id}, Name: {self._name}, Credits: {self._credits}")

    @staticmethod
    def input():
        """Static method to prompt for and create a new Course object."""
        course_id = input("    Course ID: ")
        name = input("    Course Name: ")
        while True:
            try:
                credits = int(input("    Course Credits: ")) # Nhập tín chỉ
                if credits > 0:
                    break
                else:
                    print("Credits must be a positive integer.")
            except ValueError:
                print("Invalid input. Please enter an integer for credits.")

        return course_id, Course(course_id, name, credits)


# --- Main Management Class (MarkManagementSystem) ---

class MarkManagementSystem:
    """Manages the collection of students, courses, and marks."""
    def __init__(self):
        self._students = {}
        self._courses = {}
        self._marks = {}


    # --- Utility Methods ---

    def _input_integer(self, prompt):
        """A utility method for clean integer input."""
        while True:
            try:
                num = int(input(prompt))
                if num >= 0:
                    return num
                else:
                    print("Please enter a non-negative integer.")
            except ValueError:
                print("Invalid input. Please enter an integer.")


    # --- Input functions ---

    def input_number_of_students(self):
        """Function to input the number of students in a class."""
        return self._input_integer("Enter the number of students in the class: ")


    def input_student_information(self, num_students):
        """Function to input information for each student."""
        print("\n--- Input Student Information ---")
        for i in range(num_students):
            print(f"Enter information for Student {i+1}:")
            student_id, new_student = Student.input()

            if student_id in self._students:
                print(f"ID '{student_id}' already exists. Skipping this input.")
                continue

            self._students[student_id] = new_student
        print("Student information input completed.")


    def input_number_of_courses(self):
        """Function to input the number of courses."""
        return self._input_integer("Enter the number of courses: ")


    def input_course_information(self, num_courses):
        """Function to input information for each course."""
        print("\n--- Input Course Information ---")
        for i in range(num_courses):
            print(f"Enter information for Course {i+1}:")
            course_id, new_course = Course.input()

            if course_id in self._courses:
                print(f"ID '{course_id}' already exists. Skipping this input.")
                continue

            self._courses[course_id] = new_course
            self._marks[course_id] = {}
        print("Course information input completed.")


    def select_course_and_input_marks(self):
        """Function to select a course and input marks for students."""
        if not self._courses or not self._students:
            print("\nNo courses or students available to input marks.")
            return

        print("\n--- Input Marks for Students ---")
        print("Available courses:")
        self.list_courses()

        course_id = input("Select the Course ID to input marks for: ")
        course = self._courses.get(course_id)

        if not course:
            print(f"Error: Course with ID '{course_id}' not found.")
            return

        print(f"\nInput marks for course: **{course.get_name()}**")

        for student_id, student in self._students.items():
            while True:
                try:
                    mark = float(input(f"  Enter mark for student {student_id} - {student.get_name()}: "))
                    # Use math.floor() to round down to 1-digit decimal
                    # math.floor(x * 10) / 10 performs the round-down to 1 decimal place
                    # E.g., 8.79 -> 87 -> 8.7; 8.01 -> 80 -> 8.0
                    rounded_mark = math.floor(mark * 10) / 10

                    # Assuming mark is between 0.0 and 10.0
                    if 0 <= rounded_mark <= 10:
                        self._marks[course_id][student_id] = rounded_mark
                        print(f"  Mark stored (rounded down): {rounded_mark}")
                        break
                    else:
                        print("Mark must be between 0 and 10 after rounding.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        # Recalculate all GPAs after a course's marks are updated
        self.calculate_all_gpas()
        print(f"Mark input completed for course '{course.get_name()}', and all GPAs recalculated.")


    # --- New Function: Calculate GPA for a given student (using numpy) ---

    def calculate_student_gpa(self, student_id):
        """
        Calculates the weighted average GPA for a single student using numpy.
        GPA is calculated as: Sum(Mark * Credits) / Sum(Credits)
        """
        student = self._students.get(student_id)
        if not student:
            return 0.0

        marks_list = []
        credits_list = []

        # Iterate through all courses and find marks for this student
        for course_id, marks_in_course in self._marks.items():
            if student_id in marks_in_course:
                course = self._courses.get(course_id)
                if course:
                    mark = marks_in_course[student_id]
                    credit = course.get_credits()
                    
                    marks_list.append(mark)
                    credits_list.append(credit)

        if not credits_list:
            student.set_gpa(0.0)
            return 0.0
            
        # Use numpy array for weighted sum calculation
        np_marks = np.array(marks_list)
        np_credits = np.array(credits_list)
        
        # Weighted Sum of Credits and Marks: numpy.dot is perfect for this
        weighted_sum_marks = np.dot(np_marks, np_credits)
        sum_of_credits = np.sum(np_credits)
        
        if sum_of_credits == 0:
            gpa = 0.0
        else:
            gpa = weighted_sum_marks / sum_of_credits
            
        student.set_gpa(gpa) # Update the student object's GPA
        return gpa
        
    def calculate_all_gpas(self):
        """Calculates GPA for every student in the system."""
        for student_id in self._students:
            self.calculate_student_gpa(student_id)


    # --- Listing functions ---

    def list_courses(self):
        """Function to list all courses."""
        if not self._courses:
            print("No courses have been entered yet.")
            return
        print("\n--- Course List ---")

        for course in self._courses.values():
            course.list()


    def list_students(self):
        """Function to list all students, sorted by GPA descending (New requirement)."""
        if not self._students:
            print("No students have been entered yet.")
            return

        # Ensure GPAs are up-to-date before sorting
        self.calculate_all_gpas()

        print("\n--- Student List (Sorted by GPA Descending) ---")
        
        # Convert dictionary values to a list for sorting
        student_list = list(self._students.values())
        
        # Sort student list by GPA descending using operator.attrgetter
        # This sorts the list of Student objects based on their _gpa attribute.
        student_list.sort(key=attrgetter('_gpa'), reverse=True)

        # Print the sorted list
        print("--------------------------------------------------------------------------")
        print("{:<10} {:<20} {:<15} {:>5}".format("Student ID", "Student Name", "Date of Birth", "GPA"))
        print("--------------------------------------------------------------------------")

        for student in student_list:
            print("{:<10} {:<20} {:<15} {:>5.2f}".format(
                student.get_id(), 
                student.get_name(), 
                student.get_dob(), 
                student.get_gpa()
            ))
        print("--------------------------------------------------------------------------")


    def show_student_marks_for_given_course(self):
        """Function to display student marks for a selected course."""
        if not self._courses:
            print("\nNo courses available to view marks.")
            return

        print("\n--- View Student Marks by Course ---")
        self.list_courses()

        course_id = input("Select the Course ID to view marks for: ")
        course = self._courses.get(course_id)

        if not course:
            print(f"Error: Course with ID '{course_id}' not found.")
            return

        course_marks = self._marks.get(course_id)
        if not course_marks:
            print(f"No marks have been entered yet for course **{course.get_name()}**.")
            return

        print(f"\nMarks for course: **{course.get_name()}** (Credits: {course.get_credits()})")
        print("---------------------------------------")
        print("{:<10} {:<20} {:>5}".format("Student ID", "Student Name", "Mark"))
        print("---------------------------------------")

        for student_id, mark in course_marks.items():
            student = self._students.get(student_id)
            student_name = student.get_name() if student else 'N/A'
            print("{:<10} {:<20} {:>5.1f}".format(student_id, student_name, mark)) # Hiển thị 1 chữ số thập phân
        print("---------------------------------------")


    # --- Main execution loop (The main function is now a method) ---

    def main(self):
        """The main control function for the program."""
        print("Welcome to the Student Mark Management System (Practical 3: Math, Numpy, Sort).")

        # Initial information input
        num_students = self.input_number_of_students()
        self.input_student_information(num_students)
        
        num_courses = self.input_number_of_courses()
        self.input_course_information(num_courses)

        while True:
            print("\n--- MENU ---")
            print("1. Input marks for a course")
            print("2. List all courses")
            print("3. List all students (Sorted by GPA Descending)")
            print("4. Show student marks for a course")
            print("5. Exit program")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.select_course_and_input_marks()
            elif choice == '2':
                self.list_courses()
            elif choice == '3':
                self.list_students()
            elif choice == '4':
                self.show_student_marks_for_given_course()
            elif choice == '5':
                print("Thank you for using the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


# Run the main function
if __name__ == "__main__":
    manager = MarkManagementSystem()
    manager.main()