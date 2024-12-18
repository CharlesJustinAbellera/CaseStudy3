import json
import os
from tabulate import tabulate

class Grade: 
    # Directories
    _grade_directory = 'data/grades/'
    _assignments_directory = 'data/assignments/'
    
    def __init__(self, student, assignment):
        # Instance Attrubutes
        self._student = student
        self._assignment = assignment

    # Determine the grade rate based on the score
    @staticmethod
    def determine_grade_rate(score):
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Average"
        elif score >= 60:
            return "Below Average"
        else:
            return "Failed"

    # Assign a grade to a student for a specific assignment.  
    @classmethod
    def assign_grade_to_student(cls):
        os.makedirs(cls._assignments_directory, exist_ok=True)
        try:
            # 1. Prompt for Assignment Code
            assignment_code = input("1 - Enter Assignment Code: ").strip()
            if not assignment_code:
                print("Error: Assignment code cannot be empty.")
                return

            # 2. Prompt for Student ID
            student_id = input("2 - Enter Student ID: ").strip()
            if not student_id:
                print("Error: Student ID cannot be empty.")
                return

            # Find the corresponding student's submission file
            submission_filename = f"{student_id}_assignment_submission.json"
            submission_path = os.path.join(cls._assignments_directory, submission_filename)

            if not os.path.exists(submission_path):
                print(f"Error: No submission found for student ID {student_id} for assignment {assignment_code}.")
                return

            # Load existing submission data
            with open(submission_path, 'r') as f:
                submission_data = json.load(f)

            # 3. Check if a grade has already been assigned
            if "score" in submission_data and "grade_rate" in submission_data:
                print(f"Error: A grade has already been assigned to student {student_id} for assignment '{assignment_code}'.")
                print(f"Assigned Score: {submission_data['score']}, Grade: {submission_data['grade_rate']}")
                return

            # 4. Prompt for Score
            try:
                score = float(input("3 - Enter Score (out of 100): ").strip())
                if not (0 <= score <= 100):
                    print("Error: Score must be between 0 and 100.")
                    return
            except ValueError:
                print("Error: Invalid score input.")
                return

            # 5. Determine the grade rate based on the score
            grade_rate = Grade.determine_grade_rate(score)

            # 6. Append grade and grade rate to the submission data
            submission_data['score'] = score
            submission_data['grade_rate'] = grade_rate

            # Save the updated submission data back to the file
            with open(submission_path, 'w') as f:
                json.dump(submission_data, f, indent=4)

            print(f"Grade assigned to student {student_id} for assignment '{assignment_code}' with score: {score} ({grade_rate})")

        except Exception as e:
            print(f"An error occurred: {e}")
    
    # Allow student to view the status of their assignments
    @staticmethod
    def student_view_assignment_status(self, student):
        os.makedirs(self._assignments_directory, exist_ok=True)
        passed_assignments = []
        
        # Ensure student has a 'student_id' attribute
        student_id = student._user_id if hasattr(student, '_user_id') else student.get('user_id')
        if not student_id:
            print("Error: Student ID not found.")
            return
        
        # Iterate through all submission files to find the relevant data for the student
        for filename in os.listdir(self._assignments_directory):
            if filename.endswith(f"{student_id}_assignment_submission.json"):
                try:
                    # Load the student's submission data from the JSON file
                    with open(os.path.join(self._assignments_directory, filename), 'r') as f:
                        submission_data = json.load(f)
                        
                        # Check if the student_id in the file matches the logged-in student_id
                        if submission_data.get('student_id') == student_id:
                            # Extract relevant details for the student
                            course_code = submission_data.get('course_code')
                            assignment_code = submission_data.get('assignment_code')
                            assignment_name = submission_data.get('assignment_name')
                            score = submission_data.get('score', 'Not yet graded')  # Default to 'N/A' if no score is present
                            grade_rate = submission_data.get('grade_rate', 'Not yet assigned')  # Default to 'N/A' if no grade rate is present
                            status = submission_data.get('status', 'N/A')  # Default to 'N/A' if no status is present
                            
                            # Append the data to the passed_assignments list
                            passed_assignments.append([
                                course_code,
                                assignment_code,
                                assignment_name,
                                score,
                                grade_rate,
                                status
                            ])
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    continue
        
        # Display the assignment details
        if passed_assignments:
            print("Assignment Status:")
            headers = ["Course Code", "Assignment Code", "Assignment Name", "Score", "Score Rate", "Status(Late or On Time)"]
            print(tabulate(passed_assignments, headers=headers, tablefmt="grid"))
        else:
            print(f"No submitted assignments found for student ID: {student_id}")

        # Ensure grades directory exists
        self.grades_dir = os.path.join('data', 'grades')
        os.makedirs(self.grades_dir, exist_ok=True)

    def assign_overall_grade(self):
            # Get input from instructor
            course_code = input("Enter Course Code: ").strip()
            student_id = input("Enter Student ID: ").strip()

            # Path for the course file
            course_file_path = f"data/courses/{course_code}_course.json"
            if not os.path.exists(course_file_path):
                print(f"Error: Course file for '{course_code}' not found.")
                return
            
            # Check if student is enrolled in the course
            try:
                with open(course_file_path, 'r') as file:
                    course_data = json.load(file)

                # Get list of enrolled students
                enrolled_students = course_data.get("enrolled_students", [])
                is_enrolled = any(student["student_id"] == student_id for student in enrolled_students)

                if not is_enrolled:
                    print(f"Error: Student ID '{student_id}' is not enrolled in course '{course_code}'.")
                    return
            except Exception as e:
                print(f"Error reading course file: {e}")
                return

            # Prepare filename for saving grades
            filename = f"{student_id}_grade.json"
            filepath = os.path.join(self.grades_dir, filename)

            # Check if the grade has already been assigned
            if os.path.exists(filepath):
                print(f"Error: Grade has already been assigned to Student ID {student_id} for Course {course_code}.")
                return

            # Input grade validation
            while True:
                try:
                    grade = float(input("Enter the Grade (0-100): "))
                    if 0 <= grade <= 100:
                        break
                    else:
                        print("Grade must be between 0 and 100.")
                except ValueError:
                    print("Invalid grade. Please enter a numeric value.")
            
            # Prepare the grades data
            grades_data = [{
                "course_code": course_code,
                "grade": grade
            }]
            
            # Save the grade to the JSON file
            os.makedirs(self.grades_dir, exist_ok=True)
            with open(filepath, 'w') as file:
                json.dump(grades_data, file, indent=4)
            
            print(f"Grade saved successfully for Student ID '{student_id}' in Course '{course_code}'.")

    # Allows student to view their grades
    def view_overall_grade(self, student):

        student_id = student._user_id if hasattr(student, '_user_id') else student.get('user_id')
        if not student_id:
            print("Error: Student ID not found.")
            return
        
        # Find all grade files for this student
        student_grade_files = [
            f for f in os.listdir(self.grades_dir) 
            if f.startswith(f"{student_id}_") and f.endswith("_grade.json")
        ]
        
        if not student_grade_files:
            print(f"No grades found for Student ID {student_id}")
            return
        
        # Collect all grades
        all_grades = []
        for filename in student_grade_files:
            filepath = os.path.join(self.grades_dir, filename)
            with open(filepath, 'r') as file:
                course_grades = json.load(file)
                all_grades.extend(course_grades)
        
        # Calculate average
        average = Grade.Calculate_Average(self, student)
        
        # Prepare table for display
        table_data = [
            [grade['course_code'], grade['grade']] for grade in all_grades
        ]
        table_data.append(["Average", f"{average:.2f}"])
        
        # Display grades using tabulate
        print(tabulate(table_data, 
                       headers=["Course Code", "Grade"], 
                       tablefmt="grid"))

    # Calculates average of all grades assigned to student
    def Calculate_Average(self, student):

        student_id = student._user_id if hasattr(student, '_user_id') else student.get('user_id')
        if not student_id:
            print("Error: Student ID not found.")
            return
        
        # Find all grade files for this student
        student_grade_files = [
            f for f in os.listdir(self.grades_dir) 
            if f.startswith(f"{student_id}_") and f.endswith("_grade.json")
        ]
        
        if not student_grade_files:
            return 0
        
        # Collect all grades
        all_grades = []
        for filename in student_grade_files:
            filepath = os.path.join(self.grades_dir, filename)
            with open(filepath, 'r') as file:
                course_grades = json.load(file)
                all_grades.extend([grade['grade'] for grade in course_grades])
        
        # Calculate and return average
        return sum(all_grades) / len(all_grades) if all_grades else 0