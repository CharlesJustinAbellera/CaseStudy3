import uuid
from tabulate import tabulate
from abc import ABC, abstractmethod
import os
import json

class Person(ABC):
    
    def __init__(self, username, password, name, email, birthdate, address, gender):
        # Private attributes
        self.__username = username
        self.__password = password
        
        # Protected attributes
        self._name = name
        self._email = email
        self._birthdate = birthdate
        self._address = address
        self._gender = gender
        
        # Unique identifier
        self._user_id = self.generate_id()

    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password
    
    @abstractmethod
    def generate_id(self):
        pass

    @abstractmethod
    def display_profile(self):
        pass

class Student(Person):   
    # Class attribute
    _total_students = 0
    
    def __init__(self, username, password, name, email, birthdate, address, gender, 
                 major, year_level, semester, academic_year):
        super().__init__(username, password, name, email, birthdate, address, gender)
        
        # Protected instance attributes
        self._major = major
        self._academic_year = academic_year
        self._year_level = year_level
        self._semester = semester
        self._courses = []

    def register(self, username, password, name, email, birthdate, address, gender, major, year_level , semester, academic_year):
        # Check if username already exists
        if PlatformAdmin.username_exists(username):
            print("Account already exists")
            return None
        
        # Generate unique ID
        user_id = self.generate_id()
        
        # Prepare user data
        student_data = {
            'user_id': user_id,
            'username': username,
            'password': password,
            'name': name,
            'email': email,
            'birthdate': birthdate.strftime("%Y-%m-%d"),
            'address': address,
            'gender': gender,
            'major': major,
            'year_level': year_level,
            'semester': semester,
            'academic_year': academic_year,
            
            'courses': []
        }
        
        # Save user profile
        PlatformAdmin.save_user(student_data, 'student')
        
        return student_data
    
    def generate_id(self):
        return f"24-{str(uuid.uuid4())[:5].upper()}"

    def display_profile(self):
        birthdate_str = self._birthdate.strftime("%Y-%m-%d")
        profile_data = [
            ["User ID", self._user_id],
            ["Username", Person.get_username(self)],
            ["Password", Person.get_password(self)],
            ["Name", self._name],
            ["Email", self._email],
            ["Birthdate", birthdate_str],
            ["Address", self._address],
            ["Gender", self._gender],
            ["Major", self._major],
            ["Year Level", self._year_level],
            ["Semester", self._semester],
            ["Year Level", self._academic_year]
        ]
        print(tabulate(profile_data, headers=["Profile", "Data"], tablefmt="grid"))

class Instructor(Person):
    
    # Class attributes
    _total_instructor_courses = 0
    _total_enrolled_students = 0
    
    def __init__(self, username, password, name, email, birthdate, address, gender, 
                 department, specialization):
        super().__init__(username, password, name, email, birthdate, address, gender)
        
        # Protected attributes
        self._department = department
        self._specialization = specialization
        self._assigned_courses = []
        
        # Increment total courses
        Instructor._total_instructor_courses += 1

        # Increment total studdents
        Instructor._total_enrolled_students += 1
    
    def register(self, username, password, name, email, birthdate, address, gender, department, specialization):
        # Check if username already exists
        if PlatformAdmin.username_exists(username):
            print("Account Already Exists")
            return None
        
        # Generate unique ID
        user_id = self.generate_id()
        
        # Prepare user data
        instructor_data = {
            'user_id': user_id,
            'username': username,
            'password': password,
            'name': name,
            'email': email,
            'birthdate': birthdate.strftime("%Y-%m-%d"),
            'address': address,
            'gender': gender,
            'department': department,
            'specialization': specialization,
            'assigned_courses': []
        }
        
        # Save user profile
        PlatformAdmin.save_user(instructor_data, 'instructor')
        
        return instructor_data    
    
    def generate_id(self):
        return f"24-{str(uuid.uuid4())[:5].upper()}"
    
    def display_profile(self):
        birthdate_str = self._birthdate.strftime("%Y-%m-%d")
        profile_data = [
            ["User ID", self._user_id],
            ["Username", Person.get_username(self)],
            ["Password", Person.get_password(self)],
            ["Name", self._name],
            ["Email", self._email],
            ["Birthdate", birthdate_str],
            ["Address", self._address],
            ["Gender", self._gender],
            ["Department", self._department],
            ["Specialization", self._specialization]
        ]
        print(tabulate(profile_data, headers=["Profile", "Value"], tablefmt="grid"))

class PlatformAdmin(Person):
    
    # Class attributes
    _total_students = 0
    _total_instructors = 0

    # Directory / Class attributes
    USERS_DIR = 'data/users/'


    def __init__(self, username, password, name, email, birthdate, address, gender):
        super().__init__(username, password, name, email, birthdate, address, gender)
        
        # Increment total admins
        PlatformAdmin._total_students += 1
        PlatformAdmin._total_instructors += 1

    def register(self, username, password, name, email, birthdate, address, gender):
        # Check if username already exists
        if PlatformAdmin.username_exists(username):
            print("Account Already Exists")
            return None
        
        # Generate unique ID
        user_id = self.generate_id()
        
        # Prepare user data
        admin_data = {
            'user_id': user_id,
            'username': username,
            'password': password,
            'name': name,
            'email': email,
            'birthdate': birthdate.strftime("%Y-%m-%d"),
            'address': address,
            'gender': gender
        }
        
        # Save user profile
        PlatformAdmin.save_user(admin_data, 'admin')
        
        return admin_data   
    
    def generate_id(self):
        return f"24-{str(uuid.uuid4())[:5].upper()}"
    
    def display_profile(self):
        birthdate_str = self._birthdate.strftime("%Y-%m-%d")
        profile_data = [
            ["User ID", self._user_id],
            ["Username", Person.get_username(self)],
            ["Password", Person.get_password(self)],
            ["Name", self._name],
            ["Email", self._email],
            ["Birthdate", birthdate_str],
            ["Address", self._address],
            ["Gender", self._gender]
        ]
        print(tabulate(profile_data, headers=["Profile", "Value"], tablefmt="grid"))

    @staticmethod
    def get_total_students():
        student_files = [f for f in os.listdir(PlatformAdmin.USERS_DIR) if f.endswith('_student_profile.json')]
        return len(student_files)

    @staticmethod
    def get_total_instructors():
        instructor_files = [f for f in os.listdir(PlatformAdmin.USERS_DIR) if f.endswith('_instructor_profile.json')]
        return len(instructor_files)
    
    @staticmethod
    def get_total_admins():
        # Count admin files with the pattern 'admin_id_admin_profile.json'
        admin_files = [f for f in os.listdir(PlatformAdmin.USERS_DIR) if f.endswith('_admin_profile.json')]
        return len(admin_files)

    def show_students(self):
        while True:
            print("\n--- STUDENT FILTERING ---")
            print("1 - Enter Major, Year Level, Semester, and Academic Year")
            print("2 - Show All Students")
            print("3 - Back")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                # Prompt for Major, Year Level , Semester, and Academic Year
                major = input("Enter Major: ").strip()
                year_level = input("Enter Year Level: ").strip()
                semester = input("Enter Semester: ").strip()
                academic_year = input("Enter Academic Year: ").strip()
                
                # Collect students based on filter
                students_data = []
                
                student_files = [f for f in os.listdir('data/users') if f.endswith('_student_profile.json')]
                
                for student_file in student_files:
                    try:
                        with open(os.path.join('data/users', student_file), 'r') as f:
                            student_profile = json.load(f)
                        
                        # Case-insensitive comparison directly from root of student_profile
                        if (student_profile['major'].lower() == major.lower() and
                            student_profile['year_level'].lower() == year_level.lower() and
                            student_profile['semester'].lower() == semester.lower() and
                            student_profile['academic_year'].lower() == academic_year.lower()):
                            
                            
                            students_data.append([
                                student_profile['user_id'],
                                student_profile['username'],
                                student_profile['major'],
                                student_profile['year_level'],
                                student_profile['semester'],
                                student_profile['academic_year']
                            ])
                    
                    except Exception as e:
                        print(f"Error processing {student_file}: {e}")
                        continue
                
                # Display students using tabulate
                if students_data:
                    print("\nStudent Details:")
                    print(tabulate(students_data, 
                                headers=["User ID", "Username", "Major", "Year Level", "Semester", "Academic Year"], 
                                tablefmt="grid"))
                else:
                    print("No students found matching the criteria.")
            
            elif choice == '2':
                # Show all students
                students_data = []
                
                student_files = [f for f in os.listdir('data/users') if f.endswith('_student_profile.json')]
                
                for student_file in student_files:
                    try:
                        with open(os.path.join('data/users', student_file), 'r') as f:
                            student_profile = json.load(f)
                        
                        students_data.append([
                            student_profile['user_id'],
                            student_profile['username'],
                            student_profile['major'],
                            student_profile['year_level'],
                            student_profile['semester'],
                            student_profile['academic_year']
                        ])
                    
                    except Exception as e:
                        print(f"Error processing {student_file}: {e}")
                        continue
                
                # Display students using tabulate
                if students_data:
                    print("\nStudent Details:")
                    print(tabulate(students_data, 
                                headers=["User ID", "Username", "Major", "Year Level", "Semester", "Academic Year"], 
                                tablefmt="grid"))
                    # Count and display the total number of students
                    total_students = PlatformAdmin.get_total_students()
                    print(f"Total Student/s: {total_students}\n")
                else:
                    print("No students found.")
            
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def show_instructors(self):
        while True:
            instructors_data = []
            instructor_files = [f for f in os.listdir('data/users') if f.endswith('_instructor_profile.json')]
            
            for instructor_file in instructor_files:
                try:
                    with open(os.path.join('data/users', instructor_file), 'r') as f:
                        instructor_profile = json.load(f)
                    
                    # Extract assigned courses information
                    assigned_courses = instructor_profile.get('assigned_courses', [])
                    if assigned_courses:
                        # Create a formatted string with course codes and names
                        course_list = ', '.join(f"{course['course_code']} ({course['course_name']})" for course in assigned_courses)
                    else:
                        course_list = 'No assigned courses'

                    # Append instructor data with assigned courses
                    instructors_data.append([
                        instructor_profile['user_id'],
                        instructor_profile['name'],
                        instructor_profile['department'],
                        course_list  # Add assigned courses info here
                    ])
                
                except Exception as e:
                    print(f"Error processing {instructor_file}: {e}")
                    continue
            
            # Display instructors using tabulate
            if instructors_data:
                print("\nList of Instructors:")
                print(tabulate(instructors_data, 
                            headers=["Instructor ID", "Name", "Department", "Assigned Courses"], 
                            tablefmt="grid"))
                # Count and display the total number of instructors
                total_instructors = PlatformAdmin.get_total_instructors()
                print(f"Total Instructor/s: {total_instructors}\n")
                break
            else:
                print("No instructors found.")
            
        
    # Ensure the users directory exists.
    @classmethod
    def ensure_users_directory(cls):
        os.makedirs(cls.USERS_DIR, exist_ok=True)
    
    @classmethod
    def username_exists(cls, username):
        for filename in os.listdir(cls.USERS_DIR):
            if filename.endswith('_profile.json'):
                with open(os.path.join(cls.USERS_DIR, filename), 'r') as f:
                    user_data = json.load(f)
                    if user_data.get('username') == username:
                        return True
        return False
    
    @classmethod
    def authenticate_user(cls, username, password, user_type):
        for filename in os.listdir(cls.USERS_DIR):
            if filename.endswith(f'_{user_type}_profile.json'):
                with open(os.path.join(cls.USERS_DIR, filename), 'r') as f:
                    user_data = json.load(f)
                    if (user_data.get('username') == username and 
                        user_data.get('password') == password):
                        return user_data
        return None
    
    @staticmethod
    def user_exists(username, user_type):
        # List all files in the 'data/users' directory for the given user type
        user_files = [f for f in os.listdir(PlatformAdmin.USERS_DIR) if f.endswith(f'_{user_type}_profile.json')]
        
        # Iterate over the user files
        for user_file in user_files:
            try:
                # Open the user file and load data
                with open(os.path.join(PlatformAdmin.USERS_DIR, user_file), 'r') as f:
                    user_data = json.load(f)
                    # Check if the username matches
                    if user_data.get('username') == username:
                        return True
            except Exception as e:
                print(f"Error processing {user_file}: {e}")
                continue
        return False

    @staticmethod
    def save_user(user_data, user_type):

        # Construct the file name
        file_name = f"{user_data['user_id']}_{user_type}_profile.json"
        file_path = os.path.join(PlatformAdmin.USERS_DIR, file_name)

        # Save the user data into the file
        with open(file_path, "w") as file:
            json.dump(user_data, file, indent=4)

    @staticmethod
    def view_student_courses():
        
        student_id = input("Enter the Student ID: ").strip()
        student_file = os.path.join(PlatformAdmin.USERS_DIR, f"{student_id}_student_profile.json")

        # Check if the student file exists
        if not os.path.exists(student_file):
            print(f"No profile found for Student ID: {student_id}")
            return

        try:
            # Read the student profile JSON file
            with open(student_file, "r") as file:
                student_data = json.load(file)
            
            # Check if the 'courses' field exists in the profile
            courses = student_data.get("courses", [])
            if not courses:
                print(f"Student {student_id} is not enrolled in any courses.")
                return

            # Prepare course data for tabulation
            table_data = []
            for course in courses:
                table_data.append([
                    course.get("course_code", "N/A"),
                    course.get("course_name", "N/A"),
                    course.get("credited_units", "N/A"),
                    course.get("college_room", "N/A"),
                    course.get("room_number", "N/A"),
                    course.get("day", "N/A"),
                    course.get("start_time", "N/A"),
                    course.get("end_time", "N/A"),
                    course.get("instructor_id", "N/A")
                ])

            # Define table headers
            headers = [
                "Course Code", "Course Name", "Units", "College Room",
                "Room No.", "Day", "Start Time", "End Time", "Instructor ID"
            ]

            # Display the table
            print(f"\n--- Courses Enrolled by Student ID: {student_id} ---")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            print()

        except Exception as e:
            print(f"Error reading student profile: {e}")
