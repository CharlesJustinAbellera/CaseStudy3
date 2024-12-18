import json
from person import Student
from course import Course
from datetime import datetime
import glob
from tabulate import tabulate
import os

class Enrollment:
    # Class attribute
    _total_enrollments = 0
    
    def __init__(self, student, course):
        # Protected instance attributes
        self._student = student
        self._course = course
        
        Enrollment._total_enrollments += 1

    # Returns the total number of enrollments made
    @staticmethod
    def get_total_enrollments():
        return Enrollment._total_enrollments

    #Check if a student is already enrolled in the course
    @staticmethod
    def is_student_enrolled(student_id, course_code):
        try:
            # Load student data
            with open(f'data/users/{student_id}_student_profile.json', 'r') as f:
                student_data = json.load(f)
            
            # Check if the course is in the student's list of enrolled courses
            return any(c['course_code'] == course_code for c in student_data.get('courses', []))
        
        except FileNotFoundError:
            print(f"Error: Student with ID {student_id} was not found.")
            return False
        except json.JSONDecodeError:
            print("Error reading student profile.")
            return False
        
    def enroll_course(self, course):
        # Assuming self._enrolled_courses is a list
        if 'enrolled_courses' not in self.__dict__:
            self._enrolled_courses = []
        
        if course not in self._enrolled_courses:
            self._enrolled_courses.append(course)
            print(f"Enrolled in course: {course.course_name}")
        else:
            print(f"Already enrolled in {course.course_name}")
    

    def add_student_to_course(self):
        print("1 - Add 1 student to course")
        print("2 - Add a whole class to course")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Single student enrollment
            student_id = input("Enter Student ID Number: ")
            course_code = input("Enter Course Code: ")

            if Enrollment.is_student_enrolled(student_id, course_code):
                print(f"Student {student_id} is already enrolled in course {course_code}.")
                return

            # Try to load student from JSON file
            try:
                with open(f'data/users/{student_id}_student_profile.json', 'r') as f:
                    student_data = json.load(f)
            except FileNotFoundError:
                print(f"Error: Student with ID {student_id} was not found.")
                return

            # Try to load course from JSON file
            try:
                with open(f'data/courses/{course_code}_course.json', 'r') as f:
                    course_data = json.load(f)
            except FileNotFoundError:
                print(f"Error: Course with Code {course_code} was not found.")
                return

            # Enroll the student
            Enrollment.enroll_single_student(student_data, course_data, student_id, course_code)

        elif choice == '2':
            # Whole section enrollment
            program = input("Enter Program (e.g., BSCS, BSCE, ABPsych): ")
            year_level = input("Enter Year Level(1st, 2nd, 3rd, 4th): ")
            semester = input("Enter Semester(1st, 2nd): ")
            course_code = input("Enter Course Code: ")

            # Try to load course data
            try:
                with open(f'data/courses/{course_code}_course.json', 'r') as f:
                    course_data = json.load(f)
            except FileNotFoundError:
                print(f"Error: Course with Code {course_code} was not found.")
                return

            # Loop through all student files and find matching students
            student_files = glob.glob('data/users/*_student_profile.json')
            for student_file in student_files:
                with open(student_file, 'r') as f:
                    student_data = json.load(f)

                # Match program, year level, and semester
                if (student_data['major'] == program and 
                    student_data['year_level'] == year_level and 
                    student_data['semester'] == semester):
                    
                    student_id = student_data['user_id']
                    Enrollment.enroll_single_student(student_data, course_data, student_id, course_code)
        else:
            print("Invalid choice. Please Try Again.")

    @staticmethod
    def enroll_single_student(student_data, course_data, student_id, course_code):
        # Create student and course objects
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

        course = Course(
            course_data['course_code'],
            course_data['course_name'],
            course_data['credited_units'],
            course_data['assigned_college_room'],
            course_data['room_number'],
            course_data['day'],
            course_data['start_time'],
            course_data['end_time'],
            course_data['instructor_id']
        )

        # Check if course already exists in student's enrolled courses
        course_exists = any(
            c['course_code'] == course_code
            for c in student_data.get('courses', [])
        )

        # Check if student is already enrolled in the course
        student_already_enrolled = any(
            s['student_id'] == student_id
            for s in course_data.get('enrolled_students', [])
        )

        if not course_exists and not student_already_enrolled:
            # Enroll the student
            enrollment = Enrollment(student, course)
            enrollment.enroll_course(course)

            # Update student profile
            student_data.setdefault('courses', []).append({
                'course_code': course._course_code,
                'course_name': course._course_name,
                'credited_units': course._credited_units,
                'college_room': course._assigned_college_room,
                'room_number': course._room_number,
                'day': course._day,
                'start_time': course._start_time,
                'end_time': course._end_time,
                'instructor_id': course._instructor_id
            })

            # Update course data
            course_data.setdefault('enrolled_students', []).append({
                'student_id': student_id,
                'username': student_data['name'],
                'student_email': student_data['email'],
                'student_major': student_data['major'],
                'student_year_level': student_data['year_level'],
                'student_semester': student_data['semester'],
                'academic_year': student_data['academic_year']
            })

            # Save updated files
            with open(f'data/users/{student_id}_student_profile.json', 'w') as f:
                json.dump(student_data, f, indent=4)
            with open(f'data/courses/{course_code}_course.json', 'w') as f:
                json.dump(course_data, f, indent=4)

            print(f"Student {student_id} successfully enrolled in {course_code}.")
        elif course_exists:
            print(f"Student {student_id} is already enrolled in course {course_code}.")
        else:
            print(f"Student {student_id} is already in course {course_code}.")

    def course_request(student):
        # Directory paths
        courses_dir = "data/courses"
        requests_dir = "data/requests"

        # Get the student's profile file path
        student_id = student._user_id if hasattr(student, '_user_id') else student.get('user_id')
        student_profile_path = f"data/users/{student_id}_student_profile.json"
        
        if not student_id:
            print("Error: Student ID not found.")
            return

        # Ensure the requests directory exists
        os.makedirs(requests_dir, exist_ok=True)

        # Load the student's profile, including major, year level, and semester
        try:
            with open(student_profile_path, 'r') as f:
                student_profile = json.load(f)

            name = student_profile.get("name")
            major = student_profile.get("major")
            year_level = student_profile.get("year_level")
            semester = student_profile.get("semester")
            enrolled_courses = {course["course_code"] for course in student_profile.get("courses", [])}
        except Exception as e:
            print(f"Error reading student profile: {e}")
            return

        # Read available courses from the course directory, excluding already enrolled ones
        available_courses = []
        try:
            for file in os.listdir(courses_dir):
                if file.endswith("_course.json"):
                    with open(os.path.join(courses_dir, file), 'r') as f:
                        course_data = json.load(f)
                        if course_data["course_code"] not in enrolled_courses:
                            available_courses.append({
                                "Course Code": course_data["course_code"],
                                "Course Name": course_data["course_name"],
                                "Credits": course_data["credited_units"]
                            })

            # Check if there are courses available for request
            if not available_courses:
                print("No new courses available for request.")
                return

            # Display available courses using tabulate
            print("Available Courses:")
            print(tabulate(available_courses, headers="keys", tablefmt="grid"))

            # Initialize student's course request data
            request_filename = os.path.join(requests_dir, f"{student_id}_course_requests.json")
            request_data = {
                "student_id": student_id,
                "name": name,
                "major": major,
                "year_level": year_level,
                "semester": semester,
                "course_requests": []
            }

            # Load existing requests if file exists
            if os.path.exists(request_filename):
                with open(request_filename, 'r') as f:
                    request_data = json.load(f)

            # Loop for selecting courses
            while True:
                # Prompt for a course code
                course_code = input("Enter the Course Code of the course you want to request: ").strip().upper()

                # Check if the course exists in available courses
                course_found = next((course for course in available_courses if course["Course Code"] == course_code), None)
                if not course_found:
                    print(f"Course with code '{course_code}' not found in the available courses! Please try again.")
                    continue

                # Check if the course is already requested
                if any(existing["course_code"] == course_code for existing in request_data["course_requests"]):
                    print(f"Course '{course_code}' is already in your requested list.")
                else:
                    # Add the course to the request list
                    request_data["course_requests"].append({
                        "course_code": course_found["Course Code"],
                        "course_name": course_found["Course Name"],
                        "credits": course_found["Credits"]
                    })
                    print(f"Course '{course_code}' added to your requests.")

                # Ask if the student wants to add another course
                add_more = input("Do you want to add another course? (yes/no): ").strip().lower()
                if add_more != "yes":
                    break

            # Save the updated course requests
            with open(request_filename, 'w') as f:
                json.dump(request_data, f, indent=4)

            print("Your course requests have been successfully saved!")

        except Exception as e:
            print(f"Error handling course requests: {e}")


    def view_course_requests():
        # Directory for course request files
        requests_dir = "data/requests"

        # Check if the directory exists
        if not os.path.exists(requests_dir):
            print("No course requests found. The requests directory does not exist.")
            return

        # Prepare a list to hold the tabulated data
        table_data = []

        try:
            # Iterate through all files in the requests directory
            for file in os.listdir(requests_dir):
                if file.endswith("_course_requests.json"):
                    # Read each JSON file
                    with open(os.path.join(requests_dir, file), 'r') as f:
                        request_data = json.load(f)

                        # Extract required fields
                        student_id = request_data.get("student_id", "Unknown")
                        name = request_data.get("name", "Unknown")
                        major = request_data.get("major", "Unknown")
                        year_level = request_data.get("year_level", "Unknown")
                        semester = request_data.get("semester", "Unknown")

                        # Extract course request details
                        course_requests = request_data.get("course_requests", [])
                        course_codes = [course["course_code"] for course in course_requests]

                        # Add data to the table
                        table_data.append({
                            "Student ID": student_id,
                            "Name": name,
                            "Major": major,
                            "Year Level": year_level,
                            "Semester": semester,
                            "Course Requests": ", ".join(course_codes)
                        })

            # Check if there are any requests to display
            if not table_data:
                print("No course requests available to display.")
                return

            # Display all course requests using tabulate
            print("Course Requests:")
            print(tabulate(table_data, headers="keys", tablefmt="grid"))

        except Exception as e:
            print(f"Error reading course requests: {e}")