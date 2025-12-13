import math

class Student:
    """Represents a single student with an ID, name, and Date of Birth."""
    def __init__(self, student_id, name, dob):
        self._student_id = student_id                                      #thuộc tính protected cho id, tên, dob
        self._name = name                                                     
        self._dob = dob                                        
        
    def get_id(self):
        """Returns the student's ID."""
        return self._student_id
        
    def get_name(self):
        """Returns the student's name."""
        return self._name

    def get_dob(self):
        """Returns the student's Date of Birth."""
        return self._dob

    def list(self):
        """Displays the student's information (part of polymorphism requirement)."""        #hiển thị thông tin svien(1 phần yêu cầu tính đa hình)
        print(f"ID: {self._student_id}, Name: {self._name}, Date of Birth: {self._dob}")

    @staticmethod
    def input():
        """Static method to prompt for and create a new Student object."""#phương thức tĩnh để yêu cầu nhập và tạo 1 đối tượng Student mới
        
        student_id = input("    Student ID: ")
        name = input("    Student Name: ")
        dob = input("    Date of Birth (DoB): ")
        return student_id, Student(student_id, name, dob)




class Course:
    """Represents a single course with an ID and name."""
    def __init__(self, course_id, name):
        self._course_id = course_id                                       #thuộc tính protected cho id, name
        self._name = name                                                      
        
    def get_id(self):
        """Returns the course's ID."""
        return self._course_id
        
    def get_name(self):
        """Returns the course's name."""
        return self._name

    def list(self):
        """Displays the course's information (part of polymorphism requirement)."""#hiển thị thông tin svien(1 phần yêu cầu tính đa hình)
        print(f"ID: {self._course_id}, Name: {self._name}")

    @staticmethod
    def input():
        """Static method to prompt for and create a new Course object."""#phương thức tĩnh để yêu cầu nhập và tạo 1 đối tượng Course mới
        
        
        course_id = input("    Course ID: ")
        name = input("    Course Name: ")
        return course_id, Course(course_id, name)





# --- Main Management Class ---

class MarkManagementSystem:
    """Manages the collection of students, courses, and marks."""
    def __init__(self):                                                     # thuộc tính protected để lưu trữ các bộ sưu tập dữ liệu     
        self._students = {}                                                 # {student_id: Student_Object}
        self._courses = {}                                                  # {course_id: Course_Object}       
        self._marks = {}                                                    # {course_id: {student_id: mark}}


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



    # --- Input functions (Matching the original procedural code's logic) ---

    def input_number_of_students(self):
        """Function to input the number of students in a class."""
        return self._input_integer("Enter the number of students in the class: ")


    def input_student_information(self, num_students):
        """Function to input information for each student."""
        print("\n--- Input Student Information ---")
        for i in range(num_students):
            print(f"Enter information for Student {i+1}:")
            student_id, new_student = Student.input()
            
            # Check for duplicate ID                                                #kiểm tra trùng lặp id
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
            
            # Check for duplicate ID                                            #kiểm tra trùng lặp id
            if course_id in self._courses:
                print(f"ID '{course_id}' already exists. Skipping this input.")
                continue
                
            self._courses[course_id] = new_course
            # Initialize marks dictionary for this course
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
        
        # Access students through the attribute
        for student_id, student in self._students.items():
            while True:
                try:
                    mark = float(input(f"  Enter mark for student {student_id} - {student.get_name()}: "))
                    # Assuming mark is between 0.0 and 10.0
                    if 0 <= mark <= 10:
                        # Store mark in the internal _marks structure
                        self._marks[course_id][student_id] = mark
                        break
                    else:
                        print("Mark must be between 0 and 10.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    
        print(f"Mark input completed for course '{course.get_name()}'.")


    # --- Listing functions (Using the list() method for polymorphism) ---     #hàm liệt kê

    def list_courses(self):
        """Function to list all courses."""
        if not self._courses:
            print("No courses have been entered yet.")
            return
        print("\n--- Course List ---")
       
        for course in self._courses.values(): # Demonstrates polymorphism: calling list() on each Course object
            course.list()                     


    def list_students(self):
        """Function to list all students."""
        if not self._students:
            print("No students have been entered yet.")
            return
        print("\n--- Student List ---")
        
        for student in self._students.values():# Demonstrates polymorphism: calling list() on each Student object
            student.list()


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

        print(f"\nMarks for course: **{course.get_name()}**")
        print("---------------------------------------")
        print("{:<10} {:<20} {:>5}".format("Student ID", "Student Name", "Mark"))
        print("---------------------------------------")
        
        for student_id, mark in course_marks.items():
            student = self._students.get(student_id)
            student_name = student.get_name() if student else 'N/A'
            print("{:<10} {:<20} {:>5.2f}".format(student_id, student_name, mark))
        print("---------------------------------------")




    # --- Main execution loop (The main function is now a method) ---

    def main(self):
        """The main control function for the program."""
        print("Welcome to the Student Mark Management System (OOP Version).")

        # Initial information input                                  #nhập thông tin ban đầu
        num_students = self.input_number_of_students()
        self.input_student_information(num_students)
        
        num_courses = self.input_number_of_courses()
        self.input_course_information(num_courses)

        while True:
            print("\n--- MENU ---")
            print("1. Input marks for a course")                     #1.nhập điểm cho 1 khóa học
            print("2. List all courses")                             #2.liệt kê danh sách khóa học
            print("3. List all students")                            #3.liệt kê danh sách svien
            print("4. Show student marks for a course")              #4.hiển thị điểm của svien cho 1 khóa học
            print("5. Exit program")                                 #5.thoát chương trình

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
    manager = MarkManagementSystem()                     # khởi tạo hệ thống quản lý và chạy phương thức main
    manager.main()