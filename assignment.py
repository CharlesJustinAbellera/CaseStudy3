import json
import os
from datetime import datetime
from tabulate import tabulate

class Assignment:
    
    # Directories / Class Attributes
    _assignments_directory = 'data/assignments/'
    _courses_directory = "data/courses/"
    
    def __init__(self, assignment_code, assignment_name, details, points, deadline_date, deadline_time):
        
        # Instance attributes
        self._assignment_code = assignment_code
        self._assignment_name = assignment_name
        self._details = details
        self._points = points
        self._deadline_date = deadline_date
        self._deadline_time = deadline_time
    
    #Check if an assignment with the given code exists
    @staticmethod
    def assignment_exists(assignment_code):
        assignment_path = os.path.join(Assignment._assignments_directory, f"{assignment_code}_assignment.json")
        return os.path.exists(assignment_path)
    
    def create_assignment(self):
        # Ensure the 'assignments' directory inside 'data' exists
        os.makedirs(self._assignments_directory, exist_ok=True)
        
        # Collect assignment details step by step
        assignment_details = {}
        
        # 1. Assignment Code
        while True:
            assignment_code = input("1 - Enter Assignment Code: ")
            if Assignment.assignment_exists(assignment_code):
                print(f"Assignment with code {assignment_code} already exists. Please enter a unique code.")
            else:
                assignment_details['assignment_code'] = assignment_code
                break
        
        # 2. Assignment Name
        assignment_details['assignment_name'] = input("2 - Enter Assignment Name: ")
        
        # 3. Assignment Details
        assignment_details['details'] = input("3 - Enter Assignment Details: ")
        
        # 4. Assignment Points
        while True:
            try:
                assignment_details['points'] = int(input("4 - Enter Assignment Points: "))
                break
            except ValueError:
                print("Please enter a valid number of points.")
        
        # 5. Deadline Date
        while True:
            deadline_date = input("5 - Enter Assignment Deadline Date (YYYY-MM-DD): ")
            try:
                # Validate date format
                datetime.strptime(deadline_date, "%Y-%m-%d")
                assignment_details['deadline_date'] = deadline_date
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
        
        # 6. Deadline Time
        while True:
            deadline_time = input("6 - Enter Assignment Deadline Time (HH:MM): ")
            try:
                # Validate time format
                datetime.strptime(deadline_time, "%H:%M")
                assignment_details['deadline_time'] = deadline_time
                break
            except ValueError:
                print("Invalid time format. Use HH:MM.")
        
        # Save assignment to a JSON file inside the 'assignments' folder
        filename = os.path.join(self._assignments_directory, f"{assignment_details['assignment_code']}_assignment.json")
        
        # Write the assignment details to the JSON file
        with open(filename, 'w') as f:
            json.dump(assignment_details, f, indent=4)
        
        print("Assignment created successfully!")
    
    def view_created_assignments(self):
        assignments = []
        
        # Iterate through assignment files
        for filename in os.listdir(self._assignments_directory):
            if filename.endswith('_assignment.json'):
                with open(os.path.join(self._assignments_directory, filename), 'r') as f:
                    assignment_data = json.load(f)
                    assignments.append([
                        assignment_data['assignment_code'],
                        assignment_data['assignment_name'],
                        assignment_data['details'],
                        assignment_data['points'],
                        assignment_data['deadline_date'],
                        assignment_data['deadline_time']
                    ])
        
        # Display using tabulate
        headers = ["Assignment Code", "Assignment Name", "Details", "Points", "Deadline Date", "Deadline Time"]
        print(tabulate(assignments, headers=headers, tablefmt="grid"))

    def assign_assignment(self):
        os.makedirs(self._courses_directory, exist_ok=True)
        
        # 1. Enter Assignment Code
        assignment_code = input("1 - Enter Assignment Code: ") 
        
        # Construct full path to the assignment file
        full_assignment_path = os.path.join(self._assignments_directory, f"{assignment_code}_assignment.json")
        
        # Check if the file exists
        if not os.path.exists(full_assignment_path):
            print(f"Assignment file does not exist: {full_assignment_path}")
            return
        
        # Load assignment details
        try: 
            with open(full_assignment_path, 'r') as f: 
                assignment_data = json.load(f) 
        except Exception as e:
            print(f"Error reading assignment file: {e}")
            return 
        
        # 2. Enter Course Code
        course_code = input("2 - Enter Course Code: ") 
        
        # Load course details to get enrolled students
        try:
            full_course_path = os.path.join(self._courses_directory, f"{course_code}_course.json")
            with open(full_course_path, 'r') as f:
                course_data = json.load(f)
        except FileNotFoundError:
            print(f"Course {course_code} not found!") 
            return
        
        # Extract enrolled students from course JSON
        enrolled_students = course_data.get('enrolled_students', [])
        
        # Check if there are any enrolled students
        if not enrolled_students:
            print(f"No students enrolled in course {course_code}")
            return
        
        # Create an assignments tracking file
        assignments_tracking_file = os.path.join(self._assignments_directory, f"{assignment_code}_assigned.json")
        
        # Prepare assignment tracking data
        assignment_tracking = { 
            'assignment_code': assignment_code, 
            'course_code': course_code, 
            'assignment_details': assignment_data,  # Include full assignment details
            'assigned_students': [] 
        }
        
        # Add student details to tracking
        for student in enrolled_students:
            assignment_tracking['assigned_students'].append({
                'student_id': student['student_id'], 
                'username': student['username']
            })
        
        # Save assignment tracking
        with open(assignments_tracking_file, 'w') as f: 
            json.dump(assignment_tracking, f, indent=4)
        
        print(f"Assignment {assignment_code} assigned to {len(enrolled_students)} student/s in course {course_code}!")
    
    def view_assignments_passed(self):
        passed_assignments = []
        
        # Iterate through the directory where student submission files are stored
        for filename in os.listdir(self._assignments_directory):
            if filename.endswith('_submission.json'):  # Look for submission files, not assigned ones
                with open(os.path.join(self._assignments_directory, filename), 'r') as f:
                    submission_data = json.load(f)

                # Extract relevant data from the submission
                student_id = submission_data.get('student_id')
                username = submission_data.get('username')
                assignment_code = submission_data.get('assignment_code')
                assignment_name = submission_data.get('assignment_name')
                submission_details = submission_data.get('submission_details', 'N/A')
                status = submission_data.get('status')
                score = submission_data.get('score', 'Not yet Scored')
                grade_rate = submission_data.get('grade_rate', 'Pending')

                # Check if the submission is passed on time or late
                submission_status = Assignment._check_late_submission(submission_data, {'submission_time': submission_data['submission_timestamp']})

                # Add to passed assignments list if submitted
                if submission_status == "On Time" or submission_status == "Late":
                    passed_assignments.append([
                        username,
                        student_id,
                        assignment_code,
                        assignment_name,
                        submission_details,
                        submission_status,
                        score,
                        grade_rate
                    ])
        
        # Display using tabulate
        print("\nAssignments Passed:")
        headers = ["Student Name", "Student ID", "Assignment Code", "Assignment Name", "Passed Assignment Details", "Status(Late or On Time)", "Score", "Grade Rate"]
        print(tabulate(passed_assignments, headers=headers, tablefmt="grid"))
        
    @staticmethod
    def _check_late_submission(assignment_details, student):
        if not student.get('submission_time'):
            return "Not Submitted"
        
        # Combine deadline date and time
        deadline = datetime.strptime(
            f"{assignment_details['deadline_date']} {assignment_details['deadline_time']}",
            "%Y-%m-%d %H:%M"
        )
        
        # Parse the full submission timestamp with microseconds
        submission_time = datetime.strptime(student['submission_time'], "%Y-%m-%d %H:%M")
        
        return "Late" if submission_time > deadline else "On Time"
    
    # Count total assignments for the student
    @staticmethod
    def count_assignments_for_student(self, student):
        assignment_count = 0  # Initialize assignment count
        
        if isinstance(student, str):
            student_id = student  
        elif hasattr(student, '_user_id'):
            student_id = student._user_id
        else:
            print("Error: Invalid student object or missing 'user_id'.")
            return
        
        try:
            # Find all assigned assignment tracking files
            assigned_files = [f for f in os.listdir(self._assignments_directory) 
                            if f.endswith('_assigned.json')]
            
            for file in assigned_files:
                # Read each assigned assignment file
                with open(os.path.join(self._assignments_directory, file), 'r') as f:
                    assigned_data = json.load(f)
                
                # Check if student is in the assigned students list
                student_assigned = any(
                    assigned_student['student_id'] == student_id
                    for assigned_student in assigned_data.get('assigned_students', [])
                )
                
                if student_assigned:
                    # Increment assignment count if student is assigned this assignment
                    assignment_count += 1
            
            return assignment_count
        
        except Exception as e:
            print(f"Error counting assignments: {e}")
            return 0  # Return 0 if there's an error

    def student_view_assignment(self, student):
        os.makedirs(self._assignments_directory, exist_ok=True)
        
        # Determine if student is a string (student_id) or an object
        if isinstance(student, str):
            student_id = student  # If it's a string, it's already the student ID
        elif hasattr(student, '_user_id'):
            student_id = student._user_id  # If it's an object, use _user_id
        else:
            print("Error: Invalid student object or missing 'user_id'.")
            return
        
        try:
            # Find all assigned assignment tracking files
            assigned_files = [f for f in os.listdir(self._assignments_directory) 
                            if f.endswith('_assigned.json')]
            
            assignment_data = []
            
            for file in assigned_files:
                # Read each assigned assignment file
                with open(os.path.join(self._assignments_directory, file), 'r') as f:
                    assigned_data = json.load(f)
                
                # Check if student is in the assigned students list
                student_assigned = any(
                    assigned_student['student_id'] == student_id  # Use student_id determined above
                    for assigned_student in assigned_data.get('assigned_students', [])
                )
                
                if student_assigned:
                    # Extract assignment details from the main assignment file
                    assignment_code = assigned_data.get('assignment_code')
                    assignment_file_path = os.path.join(self._assignments_directory, f"{assignment_code}_assignment.json")
                    
                    with open(assignment_file_path, 'r') as af:
                        assignment_details = json.load(af)
                    
                    assignment_data.append([
                        assigned_data.get('course_code', 'N/A'),
                        assignment_code,
                        assignment_details.get('assignment_name', 'N/A'),
                        assignment_details.get('details', 'N/A'),
                        assignment_details.get('points', 'N/A'),
                        assignment_details.get('deadline_date', 'N/A'),
                        assignment_details.get('deadline_time', 'N/A')
                    ])
            
            # Display assignments using tabulate
            if assignment_data:
                headers = ["Course Code", "Assignment Code", "Assignment Name", "Details", 
                        "Points", "Deadline Date", "Deadline Time"]
                print(tabulate(assignment_data, headers=headers, tablefmt="grid"))
                
                # Print the total number of assignments
                total_assignments = Assignment.count_assignments_for_student(self, student)
                print(f"Total Assignments: {total_assignments}\n")
            else:
                print("No assignments found for you.")
        
        except Exception as e:
            print(f"Error viewing assignments: {e}")

    # Submit an assignment if the student is assigned to it
    def student_submit_assignment(self, student):
        os.makedirs(self._assignments_directory, exist_ok=True)

        student_id = getattr(student, '_user_id', None)

        try:
            # 1. Enter Assignment Code
            assignment_code = input("1 - Enter Assignment Code: ").strip()
            if not assignment_code:
                print("Error: Assignment code cannot be empty.")
                return
            
            # Find the correct assignment file
            assignment_file_path = os.path.join(self._assignments_directory, f"{assignment_code}_assigned.json")
            if not os.path.exists(assignment_file_path):
                print(f"Error: Assignment '{assignment_code}' not found.")
                return
            
            # Load assignment data
            with open(assignment_file_path, 'r') as f:
                assigned_data = json.load(f)
            
            # Check if student is assigned to this assignment
            student_assigned = next(
                (s for s in assigned_data.get('assigned_students', []) if s['student_id'] == student_id),
                None
            )
            
            if not student_assigned:
                print("Error: You are not assigned to this assignment.")
                return
            
            # Check if the student has already submitted
            if student_assigned.get('submission_status') == 'Submitted':
                print("Error: You have already submitted this assignment.")
                return
            
            # Extract assignment details
            assignment_details = assigned_data.get('assignment_details', {})
            deadline_str = f"{assignment_details['deadline_date']} {assignment_details['deadline_time']}"
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

            # Get the current submission time and check if it's late
            submission_time = datetime.now()  # Get current time
            submission_status = Assignment._check_late_submission(assignment_details, {'submission_time': submission_time.strftime("%Y-%m-%d %H:%M")})

            # Warn the student if the submission is late
            if submission_status == "Late":
                print("Warning: The submission deadline has passed. Your submission will be marked as late.")

            # 2. Enter Submission Details
            submission_details = input("2 - Enter Details of Your Assignment: ").strip()
            if not submission_details:
                print("Error: Submission details cannot be empty.")
                return

            # Prepare submission data with the new status
            submission_data = {
                'course_code': assigned_data['course_code'],
                'assignment_name': assignment_details['assignment_name'],
                'assignment_code': assignment_code,
                'student_id': student_assigned['student_id'],
                'username': student_assigned['username'],
                'submission_details': submission_details,
                'submission_timestamp': submission_time.strftime("%Y-%m-%d %H:%M"),
                'deadline_date': assignment_details['deadline_date'],
                'deadline_time': assignment_details['deadline_time'],
                'status': submission_status  # Add status field based on deadline comparison
            }
            
            # Save the submission
            submission_filename = f"{student_assigned['student_id']}_assignment_submission.json"
            submission_path = os.path.join(self._assignments_directory, submission_filename)
            
            with open(submission_path, 'w') as f:
                json.dump(submission_data, f, indent=4)
            
            print(f"Assignment '{assignment_code}' submitted successfully!")
            return submission_path
        
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON file format.")
        except KeyError as e:
            print(f"Error: Missing key {e}. Please check the assignment data.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")