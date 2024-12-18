import json
import os
from tabulate import tabulate

class Feedback:
    # Class attributes
    _total_feedbacks = 0

    # Directories/ Class Attributes
    _DATA_FOLDER = 'data'
    _FEEDBACK_FOLDER = os.path.join(_DATA_FOLDER, 'feedback')
    _INSTRUCTORS_FILE = os.path.join(_DATA_FOLDER, 'instructors.json')
    _STUDENTS_FILE = os.path.join(_DATA_FOLDER, 'students.json')
    

    def __init__(self, user_id=None):
        # Ensure necessary directories and files exist
        self._create_directories()
        
        #Instance attribute
        self.user_id = user_id
    
        Feedback._total_feedbacks += 1

    # Create necessary directories for data storage
    @classmethod
    def _create_directories(cls):
        os.makedirs(cls._DATA_FOLDER, exist_ok=True)
        os.makedirs(cls._FEEDBACK_FOLDER, exist_ok=True)

    @staticmethod
    def _validate_input(input_value, prompt):
        while not input_value or input_value.isspace():
            input_value = input(prompt).strip()
        return input_value

    @classmethod
    def verify_instructor(cls, instructor_id):
        # Define the path to the user profiles folder
        profiles_folder = os.path.join(cls._DATA_FOLDER, 'users')
        
        try:
            # List all files that match the instructor profile naming convention
            instructor_files = [f for f in os.listdir(profiles_folder) if f.endswith('_instructor_profile.json')]
            
            # Loop through each instructor file to find a matching instructor_id
            for instructor_file in instructor_files:
                file_path = os.path.join(profiles_folder, instructor_file)
                with open(file_path, 'r') as file:
                    instructor_data = json.load(file)
                    if instructor_data.get('user_id') == instructor_id:
                        return True  # Match found
            
            # If no match is found
            return False
        
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error accessing instructor files or file is corrupted.")
            return False
    
    def send_feedback(self):
        try:
            # Input validation
            course_code = Feedback._validate_input(
                input("1 - Enter Course Code: ").strip(), 
                "Course Code cannot be empty. Re-enter Course Code: "
            )
            
            instructor_id = Feedback._validate_input(
                input("2 - Enter Instructor ID: ").strip(), 
                "Instructor ID cannot be empty. Re-enter Instructor ID: "
            )
            
            # Verify instructor exists
            if not Feedback.verify_instructor(instructor_id):
                print("Error: Invalid Instructor ID")
                return

            feedback_text = Feedback._validate_input(
                input("3 - Write your Feedback: ").strip(), 
                "Feedback cannot be empty. Re-enter Feedback: "
            )

            # Prepare feedback entry
            feedback_entry = {
                "course_code": course_code,
                "instructor_id": instructor_id,
                "feedback": feedback_text
            }

            # Construct feedback file path
            feedback_file_path = os.path.join(
                Feedback._FEEDBACK_FOLDER, 
                f"{instructor_id}_feedback.json"
            )

            # Ensure the feedback directory exists
            os.makedirs(Feedback._FEEDBACK_FOLDER, exist_ok=True)

            # Check if the feedback file exists; if not, create it with an empty list
            if not os.path.exists(feedback_file_path):
                with open(feedback_file_path, 'w') as file:
                    json.dump([], file)  # Create an empty list in the file if it doesn't exist

            # Read existing feedbacks
            with open(feedback_file_path, 'r') as file:
                feedbacks = json.load(file)

            # Add new feedback
            feedbacks.append(feedback_entry)

            # Write feedback back to file
            with open(feedback_file_path, 'w') as file:
                json.dump(feedbacks, file, indent=4)

            print("Feedback sent successfully!")

        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    def get_total_feedbacks(cls, instructor_id):
        feedback_file_path = os.path.join(Feedback._FEEDBACK_FOLDER, f"{instructor_id}_feedback.json")
        
        try:
            if not os.path.exists(feedback_file_path):
                return 0  # No feedback file means no feedback
            
            with open(feedback_file_path, 'r') as file:
                feedbacks = json.load(file)
            
            return len(feedbacks)  # Return the number of feedbacks

        except json.JSONDecodeError:
            print("Error reading feedback file. The file may be corrupted.")
            return 0
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return 0

    def view_feedback(self, instructor=None):
        if not instructor:
            print("No instructor object provided.")
            return

        instructor_id = instructor._user_id  # Use _user_id as it seems to be the unique ID attribute

        if not instructor_id:
            print("No instructor ID available.")
            return

        feedback_file_path = os.path.join(
            Feedback._FEEDBACK_FOLDER, 
            f"{instructor_id}_feedback.json"
        )

        try:
            with open(feedback_file_path, 'r') as file:
                feedbacks = json.load(file)

            instructor_feedbacks = [
                feedback for feedback in feedbacks 
                if feedback['instructor_id'] == instructor_id
            ]

            if not instructor_feedbacks:
                print("No feedback available.")
                return

            # Prepare data for tabulation
            table_data = [
                [
                    feedback['course_code'],
                    feedback['feedback']
                ] 
                for feedback in instructor_feedbacks
            ]

            # Display feedback using tabulate
            headers = ["Course Code", "Feedback"]
            print("\nList of Feedbacks:")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            # Call the static method to get the total feedback count
            total_feedbacks = Feedback.get_total_feedbacks(instructor_id)
            print(f"Total Feedbacks Received: {total_feedbacks}\n")

        except FileNotFoundError:
            print(f"No feedback file found for Instructor ID: {instructor_id}")
        except json.JSONDecodeError:
            print("Error reading feedback file. The file may be corrupted.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")