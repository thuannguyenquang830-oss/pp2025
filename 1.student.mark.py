# e1.student.mark.py

# Using dictionaries for data storage: dùng dictionaries để lưu dữ liệu
# courses: {id: name}
# students: {id: (name, DoB)} - Using a tuple for (name, DoB)
# marks: {course_id: {student_id: mark}}

courses = {}
students = {}
marks = {}

# --- Input functions ---

def input_number_of_students():
    """Function to input the number of students in a class."""                  #hàm nhập số lượng sinh viên trong 1 lớp
    while True:
        try:
            num = int(input("Enter the number of students in the class: "))
            return num
        except ValueError:
            print("Invalid input. Please enter an integer.")                    #---nếu đầu vào không phải số nguyên, in ra 



def input_student_information(num_students):
    """Function to input information for each student."""                       #hàm nhập thông tin của từng sinh viên
    print("\n--- Input Student Information ---")
    for i in range(num_students):
        print(f"Enter information for Student {i+1}:")
        student_id = input("  Student ID: ")
        # Check for duplicate ID                                                #kiểm tra trùng lặp ID sinh viên
        if student_id in students:
            print(f"ID '{student_id}' already exists. Skipping this input.")    #---nếu id svien đã tồn tại, bỏ qua 
            continue
            
        name = input("  Student Name: ")
        dob = input("  Date of Birth (DoB): ")
        students[student_id] = (name, dob)
    print("Student information input completed.")



def input_number_of_courses():
    """Function to input the number of courses."""                              #hàm nhập số lượng khóa học
    while True:
        try:
            num = int(input("Enter the number of courses: "))
            return num
        except ValueError:
            print("Invalid input. Please enter an integer.")                    #---nếu đầu vào không phải số nguyên, không hợp lệ, in ra



def input_course_information(num_courses):
    """Function to input information for each course."""                        #hàm nhập thông tin khóa học
    print("\n--- Input Course Information ---")                                 
    for i in range(num_courses):
        print(f"Enter information for Course {i+1}:")
        course_id = input("  Course ID: ")
        # Check for duplicate ID                                                #kiểm tra trùng lặp ID khóa học
        if course_id in courses:
            print(f"ID '{course_id}' already exists. Skipping this input.")
            continue
            
        name = input("  Course Name: ")
        courses[course_id] = name
        # Initialize marks dictionary for this course                           #khởi tạo điểm cho khóa học này
        marks[course_id] = {}
    print("Course information input completed.")



def select_course_and_input_marks():
    """Function to select a course and input marks for students."""             #hàm chọn khóa học và nhập điểm cho sinh viên
    if not courses or not students:
        print("\nNo courses or students available to input marks.")             #---nếu chưa có khóa học or svien, in ra
        return

    print("\n--- Input Marks for Students ---")
    print("Available courses:")
    list_courses()

    course_id = input("Select the Course ID to input marks for: ")              
    if course_id not in courses:
        print(f"Error: Course with ID '{course_id}' not found.")                #---nếu ko tìm thấy id của khóa học đã nhập, in ra
        return

    print(f"\nInput marks for course: **{courses[course_id]}**")
    for student_id, (name, dob) in students.items():
        while True:
            try:
                mark = float(input(f"  Enter mark for student {student_id} - {name}: "))
                # Assuming mark is between 0.0 and 10.0
                if 0 <= mark <= 10:
                    marks[course_id][student_id] = mark
                    break
                else:
                    print("Mark must be between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    print(f"Mark input completed for course '{courses[course_id]}'.")




# --- Listing functions ---

def list_courses():
    """Function to list all courses."""                                         #hàm liệt kê danh sách khóa học
    if not courses:
        print("No courses have been entered yet.")
        return
    print("\n--- Course List ---")
    for id, name in courses.items():
        print(f"ID: {id}, Name: {name}")



def list_students():
    """Function to list all students."""                                        #hàm liệt kê danh sách sinh viên
    if not students:
        print("No students have been entered yet.")                             #---nếu ko có svien, in ra
        return
    print("\n--- Student List ---")
    for id, (name, dob) in students.items():
        print(f"ID: {id}, Name: {name}, Date of Birth: {dob}")



def show_student_marks_for_given_course():
    """Function to display student marks for a selected course."""              #hàm hiển thị điểm của sinh viên cho khóa học đã chọn
    if not courses:
        print("\nNo courses available to view marks.")                          #---chưa có khóa học để xem điểm 
        return

    print("\n--- View Student Marks by Course ---")
    list_courses()

    course_id = input("Select the Course ID to view marks for: ")
    if course_id not in courses:
        print(f"Error: Course with ID '{course_id}' not found.")                #ko tìm thấy khóa học của id đã nhập
        return

    course_marks = marks.get(course_id)
    if not course_marks:
        print(f"No marks have been entered yet for course **{courses[course_id]}**.")
        return

    print(f"\nMarks for course: **{courses[course_id]}**")
    print("---------------------------------------")
    print("{:<10} {:<20} {:>5}".format("Student ID", "Student Name", "Mark"))
    print("---------------------------------------")
    for student_id, mark in course_marks.items():
        # Retrieve student name from the students dictionary                        #lấy tên sinh viên từ dictionary students
        student_name = students.get(student_id, ('N/A', 'N/A'))[0] 
        print("{:<10} {:<20} {:>5.2f}".format(student_id, student_name, mark))
    print("---------------------------------------")


# --- Main execution loop ---

def main():
    """The main control function for the program."""                                #hàm điều khiến chính của chương trình
    print("Welcome to the Student Mark Management System.")

    # 1. Initial information input                                                  #nhập thông tin cơ bản
    num_students = input_number_of_students()
    input_student_information(num_students)
    
    num_courses = input_number_of_courses()
    input_course_information(num_courses)

    while True:
        print("\n--- MENU ---")
        print("1. Input marks for a course")                                        #1.nhập điểm cho 1 khóa học
        print("2. List all courses")                                                #2.liệt kê danh sách khóa học
        print("3. List all students")                                               #3.liệt kê danh sách svien
        print("4. Show student marks for a course")                                 #4.hiển thị điểm của svien cho 1 khóa học
        print("5. Exit program")                                                    #5.thoát chương trình

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            select_course_and_input_marks()
        elif choice == '2':
            list_courses()
        elif choice == '3':
            list_students()
        elif choice == '4':
            show_student_marks_for_given_course()
        elif choice == '5':
            print("Thank you for using the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the main function
if __name__ == "__main__":
    main()