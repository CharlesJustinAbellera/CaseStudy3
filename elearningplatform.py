from enrollment import Enrollment
from assignment import Assignment
from person import Student, Instructor
from datetime import datetime
from person import PlatformAdmin
import os
from course import Course, Room
from os import system, name
from grade import Grade
from feedback import Feedback
from tabulate import tabulate

def clear(): #* clearing terminals
  if name == 'nt': #* for windows
    _ = system('cls')
  else: # for mac and linux
    _ = system('clear')

class ELearningPlatform:

    Date_established = "12 - 01 - 24"
    Platform_Name = "E-LEARNING PLATFORM"
    Platform_Details = "A system designed to manage students,\ninstructors, and administrators."
    Creator = "Abellera, Lagata, and Martinez"
    
    def __init__(self):
        # Instance Attributes
        self.students = []
        self.instructors = []
        self.admins = []
        self.courses = []
        self.assignments = []

        # Directories/Instance Attributes
        self._assignments_directory = "data/assignments/"
        self._courses_directory = "data/courses/"
        self.grades_dir = os.path.join('data', 'grades')
        self._assignments_directory = "data/assignments/"

        os.makedirs(self._assignments_directory, exist_ok=True)
        os.makedirs(self.grades_dir, exist_ok=True)
        os.makedirs(self._assignments_directory, exist_ok=True)
        os.makedirs(self._courses_directory, exist_ok=True)

    def main_menu(self):
        while True:
            print("\n--- E-LEARNING PLATFORM ---")
            print("1 - Student Login")
            print("2 - Student Register")
            print("3 - Instructor Login")
            print("4 - Instructor Register")
            print("5 - Admin Login")
            print("6 - Admin Register")
            print("7 - About Platform")
            print("8 - Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.student_login()
            elif choice == '2':
                self.student_register()
            elif choice == '3':
                self.instructor_login()
            elif choice == '4':
                self.instructor_register()
            elif choice == '5':
                self.admin_login()
            elif choice == '6':
                self.admin_register()
            elif choice == '7':
                self.get_platform_info()
            elif choice == '8':
                print("Thank you for using this E-Learning Platform! Come Again!")
                break
            else:
                print("Invalid choice. Please try again.")

    @classmethod
    def get_platform_info(cls):
        total_students = PlatformAdmin.get_total_students()
        total_instructors = PlatformAdmin.get_total_instructors()
        total_admins = PlatformAdmin.get_total_admins()
        total_users = total_students + total_instructors + total_admins

        # Data to be displayed in tabulate
        platform_info = [
            ["Platform Name", cls.Platform_Name],
            ["Date Established", cls.Date_established],
            ["About Platform", cls.Platform_Details],
            ["Total Users", total_users],
            ["Total Students", total_students],
            ["Total Instructors", total_instructors],
            ["Total Admins", total_admins],
            ["Created by", cls.Creator]
        ]

        # Display statistics using tabulate
        print("\n                  --- ABOUT PLATFORM ---")
        print(tabulate(platform_info, tablefmt="fancy_grid"))
    
    def student_login(self):
        clear()
        print("--- STUDENT LOGIN ---")
        username = input("Enter username: ")
        password = input("Enter password: ")
        clear()
        
        # Check if the student exists
        if not PlatformAdmin.user_exists(username, 'student'):
            print("No such student found. Please register.")
            return  # Return if student does not exist
        
        # Authenticate student
        student_data = PlatformAdmin.authenticate_user(username, password, 'student')
        
        if student_data:
            # Create Student object from saved data
            student = Student(
                student_data['username'], 
                student_data['password'], 
                student_data['name'], 
                student_data['email'], 
                datetime.strptime(student_data['birthdate'], "%Y-%m-%d"),
                student_data['address'], 
                student_data['gender'], 
                student_data['major'], 
                student_data['year_level'],
                student_data['semester'],
                student_data['academic_year']
            )
            student._user_id = student_data['user_id']
            self.student_menu(student)
        else:
            print("Invalid username or password.")

    def student_menu(self, student):
        while True:
            print(f"User Type: STUDENT")
            print(f"Current User: {student._name} | User ID: {student._user_id}")
            print(f"\n--- STUDENT MENU ---")
            print("1 - View Profile")
            print("2 - Assignments")
            print("3 - Courses")
            print("4 - Feedback")
            print("5 - View Grades")
            print("6 - Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                clear()
                student.display_profile()
            elif choice == '2':
                clear()
                self.student_assignment_menu(student)
            elif choice == '3':
                clear()
                self.student_courses_menu(student)
            elif choice == '4':
                clear()
                self.student_feedback_menu()
            elif choice == '5':
                clear()
                Grade.view_overall_grade(self, student)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def student_assignment_menu(self, student):
        while True:
            print("\n--- ASSIGNMENT MENU ---")
            print("1 - View My Assignments")
            print("2 - Submit Assignment")
            print("3 - View Submitted Assignment Status")
            print("4 - Back to Student Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                # View assigned assignments
                Assignment.student_view_assignment(self, student)
            elif choice == '2':
                # Submit an assignment
                Assignment.student_submit_assignment(self, student)
            elif choice == '3':
                # View assignment status
                Grade.student_view_assignment_status(self, student)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def student_courses_menu(self, student):
        while True:
            print("\n--- COURSES MENU ---")
            print("1 - Request a Course")
            print("2 - View Your Enrolled Courses")
            print("3 - Drop a Course")
            print("4 - Back to Student Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                Enrollment.course_request(student)
            elif choice == '2':
                Course.show_student_courses(self, student)
            elif choice == '3':
                Course.student_drop_course(student)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def student_feedback_menu(self):
        while True:
            print("\n--- FEEDBACK MENU ---")
            print("1 - Send Feedback to Instructor")
            print("2 - Back to Student Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                Feedback.send_feedback(self)
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please try again.")

    def student_register(self):
        # Initialize UserManager directory
        PlatformAdmin.ensure_users_directory()
        clear()
        # Collect registration details
        username = input("Enter username: ")
        password = input("Enter password: ")
        name = input("Enter full name: ")
        email = input("Enter email: ")
        birthdate = input("Enter birthdate (YYYY-MM-DD): ")
        address = input("Enter address: ")
        gender = input("Enter gender(Male or Female): ")
        major = input("Enter major: ")
        yearlevel = input("Enter year level(1st, 2nd, 3rd, 4th):")
        semester = input("Enter Semester(1st or 2nd): ")
        academic_year = input("Enter academic year: ")

        # Create student object and attempt registration
        student = Student(username, password, name, email, 
                          datetime.strptime(birthdate, "%Y-%m-%d"), 
                          address, gender, major, yearlevel, semester,  academic_year)
        
        result = student.register(username, password, name, email, 
                                   datetime.strptime(birthdate, "%Y-%m-%d"), 
                                   address, gender, major, yearlevel, semester, academic_year)
        
        if result:
            self.students.append(student)
            print("Student registered successfully!.")

    def instructor_login(self):
        clear()
        print("--- INSTRUCTOR LOGIN ---")
        username = input("Enter username: ")
        password = input("Enter password: ")
        clear()

        # Check if the instructor exists
        if not PlatformAdmin.user_exists(username, 'instructor'):
            print("No such instructor found. Please register.")
            return  # Return if instructor does not exist
        
        # Authenticate instructor
        instructor_data = PlatformAdmin.authenticate_user(username, password, 'instructor')
        
        if instructor_data:
            # Create Instructor object from saved data
            instructor = Instructor(
                instructor_data['username'], 
                instructor_data['password'], 
                instructor_data['name'], 
                instructor_data['email'], 
                datetime.strptime(instructor_data['birthdate'], "%Y-%m-%d"),
                instructor_data['address'], 
                instructor_data['gender'], 
                instructor_data['department'], 
                instructor_data['specialization']
            )
            instructor._user_id = instructor_data['user_id']
            self.instructor_menu(instructor)
        else:
            print("Invalid username or password.")

    def instructor_menu(self, instructor):
        while True:
            print(f"\nUser Type: INSTRUCTOR")
            print(f"Current User: {instructor._name} | User ID {instructor._user_id}")
            print(f"\n--- INSTRUCTOR MENU ---")
            print("1 - View Profile")
            print("2 - Assignments")
            print("3 - Courses")
            print("4 - View Feedbacks")
            print("5 - Assign Grades")
            print("6 - Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                instructor.display_profile()
            elif choice == '2':
                self.instructor_assignment_menu()
            elif choice == '3':
                Course.instructor_courses_menu(self, instructor)
            elif choice == '4':
                Feedback.view_feedback(self, instructor)
            elif choice == '5':
                Grade.assign_overall_grade(self)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def instructor_assignment_menu(self):
        while True:
            print("\n--- Assignment Menu ---")
            print("1 - Create New Assignment")
            print("2 - View Created Assignments")
            print("3 - Assign Assignment to Students")
            print("4 - View Assignments Passed")
            print("5 - Assign Score for Assignment")
            print("6 - Back to Instructor Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                Assignment.create_assignment(self)
            elif choice == '2':
                Assignment.view_created_assignments(self)
            elif choice == '3':
                Assignment.assign_assignment(self)
            elif choice == '4':
                Assignment.view_assignments_passed(self)
            elif choice == '5':
                Grade.assign_grade_to_student()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def instructor_register(self):
        clear()
        # Initialize UserManager directory
        PlatformAdmin.ensure_users_directory()
        
        # Collect registration details
        username = input("Enter username: ")
        password = input("Enter password: ")
        name = input("Enter full name: ")
        email = input("Enter email: ")
        birthdate = input("Enter birthdate (YYYY-MM-DD): ")
        address = input("Enter address: ")
        gender = input("Enter gender(Male or Female): ")
        department = input("Enter department: ")
        specialization = input("Enter specialization(Field): ")

        # Create instructor object and attempt registration
        instructor = Instructor(username, password, name, email, datetime.strptime(birthdate, "%Y-%m-%d"), address, gender, department, specialization)
        
        result = instructor.register(username, password, name, email, datetime.strptime(birthdate, "%Y-%m-%d"), address, gender, department, specialization)
        
        if result:
            self.instructors.append(instructor)
            print("Instructor registered successfully!")

    def admin_login(self):
        clear()
        print("--- ADMIN LOGIN ---")
        username = input("Enter username: ")
        password = input("Enter password: ")
        clear()

        # Check if the admin exists
        if not PlatformAdmin.user_exists(username, 'admin'):
            print("No such admin found. Please register.")
            return  # Return if admin does not exist
        
        # Authenticate admin
        admin_data = PlatformAdmin.authenticate_user(username, password, 'admin')
        
        if admin_data:
            # Create Admin object from saved data
            admin = PlatformAdmin(
                admin_data['username'], 
                admin_data['password'], 
                admin_data['name'], 
                admin_data['email'], 
                datetime.strptime(admin_data['birthdate'], "%Y-%m-%d"),
                admin_data['address'], 
                admin_data['gender']
            )
            admin._user_id = admin_data['user_id']
            self.admin_menu(admin)
        else:
            print("Invalid username or password.")
    
    def admin_register(self):
        # Initialize UserManager directory
        PlatformAdmin.ensure_users_directory()
        clear()
        # Collect registration details
        username = input("Enter username: ")
        password = input("Enter password: ")
        name = input("Enter full name: ")
        email = input("Enter email: ")
        birthdate = input("Enter birthdate (YYYY-MM-DD): ")
        address = input("Enter address: ")
        gender = input("Enter gender(Male or Female): ")

        # Create student object and attempt registration
        admin = PlatformAdmin(username, password, name, email, 
                          datetime.strptime(birthdate, "%Y-%m-%d"), 
                          address, gender)
        
        result = admin.register(username, password, name, email, 
                                   datetime.strptime(birthdate, "%Y-%m-%d"), 
                                   address, gender)
        
        if result:
            self.admins.append(admin)
            print("Admin registered successfully!.")

    
    def admin_menu(self, admin):
        while True:
            print(f"User Type: ADMIN")
            print(f"Current User: {admin._name} | User ID: {admin._user_id}")
            print("\n--- ADMIN MENU ---")
            print("1 - View Profile")
            print("2 - Courses")
            print("3 - Students")
            print("4 - Instructors")
            print("5 - Rooms")
            print("6 - Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                clear()
                admin.display_profile()
            elif choice == '2':
                clear()
                self.admin_courses_menu()
            elif choice == '3':
                clear()
                self.admin_students_menu()
            elif choice == '4':
                clear()
                self.admin_instructors_menu()
            elif choice == '5':
                clear()
                self.admin_room_menu()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def admin_courses_menu(self):
        while True:
            print("\n--- ADMIN COURSE MENU ---")
            print("1 - Add Course")
            print("2 - Remove Course")
            print("3 - Show Courses")
            print("4 - Assign Course to Instructor")
            print("5 - Back to Admin Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                Course.add_course(self)
            elif choice == '2':
                Course.remove_course(self)
            elif choice == '3':
                Course.show_all_courses(self)
            elif choice == '4':
                Course.assign_course_to_instructor(self)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def admin_students_menu(self):
        while True:
            print("\n--- ADMIN STUDENT MENU ---")
            print("1 - Show Students")
            print("2 - Show Student Course Request")
            print("3 - Add Student to Course")
            print("4 - View Student Courses")
            print("5 - Back to Admin Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                PlatformAdmin.show_students(self)
            elif choice == '2':
                Enrollment.view_course_requests()
            elif choice == '3':
                Enrollment.add_student_to_course(self)
            elif choice == '4':
                PlatformAdmin.view_student_courses()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def admin_instructors_menu(self):
        while True:
            print("\n--- ADMIN INSTRUCTOR MENU ---")
            print("1 - Show Instructors")
            print("2 - Back to Admin Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                PlatformAdmin.show_instructors(self)
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please try again.")

    def admin_room_menu(self):
        while True:
            print("\n--- Room Scheduling System ---")
            print("1 - Add Room")
            print("2 - Show All Added Rooms")
            print("3 - Remove a Room")
            print("4 - Back to Admin Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                Room.create_room()
            elif choice == '2':
                Room.show_all_rooms_with_schedule()
            elif choice == '3':
                Room.remove_room()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")
        
    def run(self):
        self.main_menu()

def main():
    platform = ELearningPlatform()
    platform.run()

if __name__ == "__main__":
    main()