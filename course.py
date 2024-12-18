import json
from tabulate import tabulate
import os
from datetime import datetime

class Room():
    def __init__(self, assigned_college_room, room_number):
        #Instance Attributes
        self._assigned_college_room = assigned_college_room
        self._room_number = room_number
        self._scheduled_times = []

    # Check if a room is already created or exists in the system
    @staticmethod
    def is_room_already_created(assigned_college_room, room_number):
        filename = f'data/rooms/{assigned_college_room}_{room_number}_room.json'
        return os.path.exists(filename)
    
    @staticmethod
    def create_room():
        # Collect room information
        assigned_college_room = input("Enter Assigned College Room: ").strip().upper()
        room_number = input("Enter Room Number: ").strip()
        
        # Validate inputs
        if not assigned_college_room or not room_number:
            print("Invalid input. Both college room and room number are required.")
            return None
        
        # Check if room already exists using the static method
        if Room.is_room_already_created(assigned_college_room, room_number):
            print(f"Room {assigned_college_room} {room_number} already exists!")
            return None
        
        # Prepare room data
        room_data = {
            "assigned_college_room": assigned_college_room,
            "room_number": room_number,
            "scheduled_times": []
        }
        
        # Ensure data directory exists
        os.makedirs('data/rooms', exist_ok=True)
        
        # Save room information
        filename = f'data/rooms/{assigned_college_room}_{room_number}_room.json'
        try:
            with open(filename, 'w') as f:
                json.dump(room_data, f, indent=4)
            
            print(f"Room {assigned_college_room} {room_number} created successfully!")
            return room_data
        except Exception as e:
            print(f"Error creating room: {e}")
            return None
    
    @classmethod
    def show_all_rooms_with_schedule(cls):
        rooms_data = []
        
        # Find all room JSON files
        try:
            room_files = [f for f in os.listdir('data/rooms') if f.endswith('_room.json')]
            
            for room_file in room_files:
                try:
                    with open(os.path.join('data/rooms', room_file), 'r') as f:
                        room_details = json.load(f)
                    
                    # Prepare room data for display
                    rooms_data.append([
                        room_details['assigned_college_room'],
                        room_details['room_number'],
                        len(room_details.get('scheduled_times', [])),
                        ', '.join([f"{schedule.get('day', 'N/A')}: {schedule.get('start_time', 'N/A')}-{schedule.get('end_time', 'N/A')}" 
                                   for schedule in room_details.get('scheduled_times', [])])
                    ])
                
                except Exception as e:
                    print(f"Error processing {room_file}: {e}")
                    continue
            
            # Display rooms using tabulate
            if rooms_data:
                print("\nRoom Schedules:")
                print(tabulate(rooms_data, headers=["College Room", "Room Number", "Scheduled Times", "Time Slots"], 
                            tablefmt="grid"))
            else:
                print("No rooms found.")
        
        except FileNotFoundError:
            print("No rooms directory found.")
    
    @classmethod
    def remove_room(cls):
        assigned_college_room = input("Enter Assigned College Room: ").strip().upper()
        room_number = input("Enter Room Number: ").strip()
        
        # Construct the filename
        filename = f'data/rooms/{assigned_college_room}_{room_number}_room.json'
        
        # Check if room exists and remove
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Room {assigned_college_room} {room_number} removed successfully!")
            else:
                print(f"Room {assigned_college_room} {room_number} not found.")
        except Exception as e:
            print(f"Error removing room: {e}")
    
    # Check if a room is registered in the system
    @classmethod
    def is_room_registered(cls, assigned_college_room, room_number):
        filename = f'data/rooms/{assigned_college_room}_{room_number}_room.json'
        return os.path.exists(filename)
    

class Schedule(Room):

    # Directories/ Class Attributes
    data_path = "data/"
    rooms_dir = "rooms/"
    courses_dir = "courses/"

    def __init__(self, assigned_college_room, room_number, day, start_time, end_time ):
        super().__init__(assigned_college_room, room_number)
        # Protected Instance attributes
        self._day = day
        self._start_time = start_time
        self._end_time = end_time
    
    # Schedule a course with conflict checking
    @classmethod
    def schedule_course(cls):
        # Collect course details
        course_name = input("Enter Course Name: ").strip()
        assigned_college_room = input("Enter Assigned College Room: ").strip().upper()
        room_number = input("Enter Room Number: ").strip()
        day = input("Enter Day (e.g., Monday): ").strip().capitalize()
        start_time = input("Enter Start Time (HH:MM): ").strip()
        end_time = input("Enter End Time (HH:MM): ").strip()
        
        # Prepare course details
        course_details = {
            'course_name': course_name,
            'assigned_college_room': assigned_college_room,
            'room_number': room_number,
            'day': day,
            'start_time': start_time,
            'end_time': end_time
        }
        
        # Check room schedule conflict
        if cls.check_room_schedule_conflict(course_details):
            # Ensure courses directory exists
            os.makedirs('data/courses', exist_ok=True)
            
            # Create course filename
            course_filename = f'data/courses/{course_name}_course.json'
            
            # Save course schedule
            try:
                with open(course_filename, 'w') as f:
                    json.dump(course_details, f, indent=4)
                
                print(f"Course {course_name} scheduled successfully!")
                return course_details
            except Exception as e:
                print(f"Error scheduling course: {e}")
                return None
        
        return None
    
    # Check for room schedule conflicts.
    @staticmethod
    def check_room_schedule_conflict(course_details):
        assigned_college_room = course_details.get('assigned_college_room')
        room_number = course_details.get('room_number')
        proposed_day = course_details.get('day')
        proposed_start_time = course_details.get('start_time')
        proposed_end_time = course_details.get('end_time')
        
        # Construct room filename
        room_filename = f'data/rooms/{assigned_college_room}_{room_number}_room.json'
        
        # Check if room exists
        if not os.path.exists(room_filename):
            print(f"Room {assigned_college_room} {room_number} is not registered!")
            return False
        
        # Read existing room schedules
        try:
            with open(room_filename, 'r') as f:
                room_data = json.load(f)
            
            # Get existing scheduled times
            scheduled_times = room_data.get('scheduled_times', [])
            
            # Convert times to minutes for comparison
            def time_to_minutes(time_str):
                hours, minutes = map(int, time_str.split(':'))
                return hours * 60 + minutes
            
            proposed_start = time_to_minutes(proposed_start_time)
            proposed_end = time_to_minutes(proposed_end_time)
            
            # Check for conflicts on the same day
            for schedule in scheduled_times:
                if schedule.get('day') == proposed_day:
                    sched_start = time_to_minutes(schedule.get('start_time'))
                    sched_end = time_to_minutes(schedule.get('end_time'))
                    
                    # Check for time overlap
                    if not (proposed_end <= sched_start or proposed_start >= sched_end):
                        print(f"Time conflict in room {assigned_college_room} {room_number} on {proposed_day}!")
                        print(f"Conflicting Schedule: {schedule.get('start_time')} - {schedule.get('end_time')}")
                        return False
            
            # No conflicts found, add new schedule
            scheduled_times.append({
                'day': proposed_day,
                'start_time': proposed_start_time,
                'end_time': proposed_end_time
            })
            
            # Update room JSON with new schedule
            room_data['scheduled_times'] = scheduled_times
            with open(room_filename, 'w') as f:
                json.dump(room_data, f, indent=4)
            
            return True
        
        except Exception as e:
            print(f"Error checking room schedule: {e}")
            return False

class Course(Schedule, Room):   
    # Class attributes
    _total_courses = 0
    _min_credits = 2
    _max_credits = 6
    
    def __init__(self, course_code, course_name, credited_units, assigned_college_room, room_number, day, start_time, end_time, instructor_id):
        super().__init__(assigned_college_room, room_number, day, start_time, end_time,)
        # Protected Instance attributes
        self._course_code = course_code
        self._course_name = course_name
        self._credited_units = credited_units
        self._enrolled_students = []
        self._assigned_instructor = None
        self._instructor_id = instructor_id
        
        # Increment total courses
        Course._total_courses += 1
    
    # Getter for course code
    @property
    def course_code(self):
        return self._course_code
    
    # Getter for course name.
    @property
    def course_name(self):
        return self._course_name
    
    def save_course_details(self, instructor_id):
        
        # Construct the filename for the instructor's profile
        filename = f'data/users/{instructor_id}_instructor_profile.json'
        
        # Prepare the course details dictionary
        course_data = {
            'course_code': self._course_code,
            'course_name': self._course_name,
            'credited_units': self._credited_units,
            'college_room': self._assigned_college_room,
            'room_number': self._room_number,
            'day': self._day,
            'start_time': self._start_time,
            'end_time': self._end_time   
        }
        
        try:
            # Read the existing instructor profile
            with open(filename, 'r') as f:
                instructor_profile = json.load(f)
            
            # Check if 'assigned_courses' exists, if not create it
            if 'assigned_courses' not in instructor_profile:
                instructor_profile['assigned_courses'] = []
            
            # Add the new course to the assigned courses
            instructor_profile['assigned_courses'].append(course_data)
            
            # Write the updated profile back to the file
            with open(filename, 'w') as f:
                json.dump(instructor_profile, f, indent=4)
            
            print(f"Course details saved successfully to {filename}")
        
        except FileNotFoundError:
            print(f"Instructor profile file not found: {filename}")
        except Exception as e:
            print(f"Error saving course details: {e}")

    def add_course(self):
        # Collect course information
        course_code = input("Enter Course Code: ").strip()
        course_name = input("Enter Course Name: ").strip()

        # Validate credited units
        try:
            credited_units = int(input(f"Enter Accredited Units (between {Course._min_credits} and {Course._max_credits}): ").strip())
            if credited_units < Course._min_credits or credited_units > Course._max_credits:
                print(f"Invalid credited units! Please enter a value between {Course._min_credits} and {Course._max_credits}.")
                return
        except ValueError:
            print("Invalid input! Please enter a valid integer for credited units.")
            return

        assigned_college_room = input("Enter College Room: ").strip().upper()
        room_number = input("Enter Room Number: ").strip()

        # Schedule details
        day = input("Enter Day of Week (Monday-Friday): ").strip().capitalize()
        start_time = input("Enter Start Time (HH:MM)(24-hour format): ").strip()
        end_time = input("Enter End Time (HH:MM)(24-hour format): ").strip()

        # Prepare course details dictionary with placeholders for instructor
        course_details = {
            'course_code': course_code,
            'course_name': course_name,
            'credited_units': credited_units,
            'assigned_college_room': assigned_college_room,
            'room_number': room_number,
            'day': day,
            'start_time': start_time,
            'end_time': end_time,
            'instructor_id': None,  # Placeholder
            'name': None,  # Placeholder
            'enrolled_students': []
        }

        # Step 1: Validate Room Existence
        room_filename = f'data/rooms/{assigned_college_room}_{room_number}_room.json'
        if not os.path.exists(room_filename):
            print(f"Room {assigned_college_room} {room_number} is not registered in the system!")
            return

        # Step 2: Check Room Schedule Conflicts
        if not Schedule.check_room_schedule_conflict(course_details):
            print("Cannot create course due to scheduling conflict.")
            return

        # Step 3: Save Course Details
        try:
            os.makedirs('data/courses', exist_ok=True)
            with open(f'data/courses/{course_code}_course.json', 'w') as f:
                json.dump(course_details, f, indent=4)

            print("Course added successfully! Instructor can be assigned later.")
        except Exception as e:
            print(f"Error saving course details: {e}")

    def assign_course_to_instructor(self):
        course_code = input("Enter Course Code to Assign: ").strip()
        instructor_id = input("Enter Instructor ID: ").strip()

        # Check if course exists
        course_path = f'data/courses/{course_code}_course.json'
        if not os.path.exists(course_path):
            print(f"Course {course_code} does not exist.")
            return

        # Check if instructor profile exists
        instructor_profile_path = f'data/users/{instructor_id}_instructor_profile.json'
        if not os.path.exists(instructor_profile_path):
            print(f"No profile found for instructor {instructor_id}.")
            return

        try:
            # Load course details
            with open(course_path, 'r') as f:
                course_details = json.load(f)

            # Load instructor profile
            with open(instructor_profile_path, 'r') as f:
                instructor_profile = json.load(f)

            username = instructor_profile.get('name', 'N/A')

            # Update course details
            course_details['instructor_id'] = instructor_id
            course_details['name'] = username

            # Save updated course details
            with open(course_path, 'w') as f:
                json.dump(course_details, f, indent=4)

            # Update instructor's profile with course assignment
            new_course_entry = {
                'course_code': course_code,
                'course_name': course_details['course_name'],
                'credited_units': course_details['credited_units'],
                'assigned_college_room': course_details['assigned_college_room'],
                'room_number': course_details['room_number'],
                'day': course_details['day'],
                'start_time': course_details['start_time'],
                'end_time': course_details['end_time']
            }

            if 'assigned_courses' not in instructor_profile:
                instructor_profile['assigned_courses'] = []

            if not any(course['course_code'] == course_code for course in instructor_profile['assigned_courses']):
                instructor_profile['assigned_courses'].append(new_course_entry)
                with open(instructor_profile_path, 'w') as f:
                    json.dump(instructor_profile, f, indent=4)
                print(f"Course {course_code} successfully assigned to instructor {instructor_id}.")
            else:
                print(f"Course {course_code} is already assigned to instructor {instructor_id}.")
        except Exception as e:
            print(f"Error assigning course to instructor: {e}")

    def remove_course(self):
        course_code = input("Enter Course Code to remove: ")
        
        # Debug: Check existing course files
        course_files = [f for f in os.listdir('data/courses') if f.endswith('_course.json')]
        print(f"Debug: Existing course files: {course_files}")
        
        # Check if course JSON file exists
        course_file_path = f'data/courses/{course_code}_course.json'
        
        # Debug: Check specific file path
        print(f"Debug: Checking file path {course_file_path}")
        print(f"Debug: File exists: {os.path.exists(course_file_path)}")
        
        # Read the course file to verify its contents
        try:
            with open(course_file_path, 'r') as f:
                course_details = json.load(f)
            
            print("Debug: Course details:")
            print(json.dumps(course_details, indent=4))
        except FileNotFoundError:
            print(f"Debug: File {course_file_path} not found")
        except json.JSONDecodeError:
            print(f"Debug: Error decoding JSON in {course_file_path}")
        
        # Check course in self.courses
        course = next((c for c in self.courses if c._course_code == course_code), None)
        
        if course or os.path.exists(course_file_path):
            # Remove from courses list
            self.courses = [c for c in self.courses if c._course_code != course_code]
            
            # Remove course from any instructors who have it assigned
            for instructor in self.instructors:
                instructor._assigned_courses = [
                    c for c in instructor._assigned_courses if c._course_code != course_code
                ]
                
                # Update instructor's JSON file
                try:
                    with open(f'data/users/{instructor._user_id}_instructor_profile.json', 'r') as f:
                        instructor_profile = json.load(f)
                    
                    # Remove the course from assigned courses
                    instructor_profile['assigned_courses'] = [
                        c for c in instructor_profile.get('assigned_courses', []) 
                        if c['course_code'] != course_code
                    ]
                    
                    # Save updated profile
                    with open(f'data/users/{instructor._user_id}_instructor_profile.json', 'w') as f:
                        json.dump(instructor_profile, f, indent=4)
                except FileNotFoundError:
                    pass
            
            # Remove course details file
            try:
                os.remove(course_file_path)
                print(f"Course {course_code} removed successfully!")
            except Exception as e:
                print(f"Error removing course file: {e}")
        else:
            print("Course not found.")

    def show_all_courses(self):
        courses_data = []
        
        instructor_data = {}
        instructor_dir = os.path.join('data', 'users')  # Construct the path

        # Debug: Check if the instructor directory exists
        if not os.path.exists(instructor_dir):
            print(f"Error: The directory '{instructor_dir}' does not exist.")
            return
        
        # Debug: List files in the instructor directory
        # print("Instructor files found:", os.listdir(instructor_dir))

        instructor_files = [f for f in os.listdir(instructor_dir) if f.endswith('_instructor_profile.json')]
        
        for instructor_file in instructor_files:
            try:
                with open(os.path.join(instructor_dir, instructor_file), 'r') as f:
                    instructor = json.load(f)
                    instructor_data[instructor['user_id']] = instructor['name']
            except Exception as e:
                print(f"Error loading {instructor_file}: {e}")
                continue
        
        # Load course files
        course_dir = os.path.join('data', 'courses')
        if not os.path.exists(course_dir):
            print(f"Error: The directory '{course_dir}' does not exist.")
            return
        
        course_files = [f for f in os.listdir(course_dir) if f.endswith('_course.json')]
        
        for course_file in course_files:
            try:
                with open(os.path.join(course_dir, course_file), 'r') as f:
                    course_details = json.load(f)
                
                instructor_id = course_details['instructor_id']
                username = course_details.get('username') or instructor_data.get(instructor_id, 'To be Assigned')
                
                courses_data.append([
                    course_details['course_code'],
                    course_details['course_name'],
                    course_details['credited_units'],
                    course_details['assigned_college_room'],
                    course_details['room_number'],
                    course_details['day'],
                    course_details['start_time'],
                    course_details['end_time'],
                    instructor_id if instructor_id else "To be Assigned",
                    username
                ])
            except Exception as e:
                print(f"Error processing {course_file}: {e}")
                continue
        
        # Display courses using tabulate
        if courses_data:
            print("\nCourse Details:")
            print(tabulate(courses_data, 
                        headers=["Code", "Name", "Credits", "College Room", "Room Number", "Day", 
                                "Start Time", "End Time", "Instructor ID", "Instructor Name"],
                        tablefmt="grid"))
        else:
            print("No courses found.")

    @staticmethod
    def get_total_courses(enrolled_courses):
        # Return the number of enrolled courses
        return len(enrolled_courses)

    def show_student_courses(self, student):
        try:
            # Load student's profile using their user ID
            with open(f'data/users/{student._user_id}_student_profile.json', 'r') as f:
                student_profile = json.load(f)
            
            # Extract enrolled courses
            enrolled_courses = student_profile.get('courses', [])
            
            # Check if the student has any enrolled courses
            if not enrolled_courses:
                print("No courses enrolled for this student.")
                return
            
            # Define day order
            day_order = {
                'Monday': 1, 
                'Tuesday': 2, 
                'Wednesday': 3, 
                'Thursday': 4, 
                'Friday': 5
            }

            # Sort courses by day and start time
            sorted_courses = sorted(
                enrolled_courses, 
                key=lambda x: (
                    day_order.get(x.get('day'), 6),  # Default to last if day not found
                    datetime.strptime(x.get('start_time', "23:59"), '%H:%M') 
                )
            )
            
            # Prepare course data for tabulation
            courses_data = []
            for course in sorted_courses:
                try:
                    # Load course details from its JSON file
                    course_file_path = os.path.join('data', 'courses', f"{course['course_code']}_course.json")
                    with open(course_file_path, 'r') as f:
                        course_details = json.load(f)
                    
                    # Append course details with instructor name to the list
                    courses_data.append([
                        course_details.get('course_code', 'N/A'),
                        course_details.get('course_name', 'N/A'),
                        course_details.get('credited_units', 'N/A'),
                        course_details.get('assigned_college_room', 'N/A'),
                        course_details.get('room_number', 'N/A'),
                        course_details.get('day', 'N/A'),
                        course_details.get('start_time', 'N/A'),
                        course_details.get('end_time', 'N/A'),
                        course_details.get('instructor_id', 'N/A'),
                        course_details.get('name', 'N/A')
                    ])
                except FileNotFoundError:
                    print(f"Course file not found for {course['course_code']}")
                except json.JSONDecodeError:
                    print(f"Error reading course file for {course['course_code']}")
            
            print("\nEnrolled Courses and Details:")
            print(tabulate(courses_data, 
                headers=["Course Code", "Course Name", "Credits", "College Room", "Room Number", 
                        "Day", "Start Time", "End Time", "Instructor ID", "Instructor Name"], 
                tablefmt="grid"))
            
            # Display the total number of enrolled courses (based on the sorted courses list)
            total_courses = Course.get_total_courses(enrolled_courses)
            print(f"Total Enrolled Courses: {total_courses}\n")

        except FileNotFoundError:
            print(f"No profile found for student {student._user_id}")
        except json.JSONDecodeError:
            print(f"Error reading profile for student {student._user_id}")

    def instructor_courses_menu(self, instructor):
        while True:
            print("\n--- COURSES MENU ---")
            print("1 - Show Courses and Details")
            print("2 - Show Students Enrolled in Course")
            print("3 - Back to Instructor Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                Course.show_instructor_courses(self, instructor)
            elif choice == '2':
                Course.view_students(instructor)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def get_total_instructor_courses(assigned_courses):
        return len(assigned_courses)
    
    def show_instructor_courses(self, instructor):
        try:
            # Load instructor's profile using their user ID
            with open(f'data/users/{instructor._user_id}_instructor_profile.json', 'r') as f:
                instructor_profile = json.load(f)
            
            # Extract assigned courses
            assigned_courses = instructor_profile.get('assigned_courses', [])
            
            # Check if the instructor has any assigned courses
            if not assigned_courses:
                print("No courses assigned to this instructor.")
                return
            
            # Define day order
            day_order = {
                'Monday': 1, 
                'Tuesday': 2, 
                'Wednesday': 3, 
                'Thursday': 4, 
                'Friday': 5
            }
            
            # Sort courses by day and start time
            sorted_courses = sorted(
                assigned_courses, 
                key=lambda x: (
                    day_order.get(x.get('day'), 6),  # Default to last if day not found
                    datetime.strptime(x.get('start_time', '23:59'), '%H:%M')
                )
            )
            
            # Prepare course data for tabulation
            courses_data = []
            for course in sorted_courses:
                course_code = course.get('course_code', 'N/A')
                
                # Get the number of students enrolled in the course
                enrolled_students_count = Course.get_enrolled_students_count(course_code)
                
                courses_data.append([
                    course_code,
                    course.get('course_name', 'N/A'),
                    course.get('credited_units', 'N/A'),
                    course.get('assigned_college_room', 'N/A'),
                    course.get('room_number', 'N/A'),
                    course.get('day', 'N/A'),
                    course.get('start_time', 'N/A'),
                    course.get('end_time', 'N/A'),
                    enrolled_students_count  # Add the number of enrolled students to the table
                ])
            
            print("Assigned Courses and Details:")
            # Display courses with student count using tabulate
            print(tabulate(courses_data, 
                        headers=["Course Code", "Course Name", "Credits", "College Room", "Room Number", "Day", "Start Time", "End Time", "Number of Enrolled Students"], 
                        tablefmt="grid"))
            
            total_instructor_courses = Course.get_total_instructor_courses(assigned_courses)
            print(f"Total Assigned Courses: {total_instructor_courses}\n")
        
        except FileNotFoundError:
            print(f"No profile found for instructor {instructor._user_id}")
        except json.JSONDecodeError:
            print(f"Error reading profile for instructor {instructor._user_id}")

    @staticmethod
    def get_enrolled_students_count(course_code):
        try:
            # Load course data
            with open(f'data/courses/{course_code}_course.json', 'r') as f:
                course_data = json.load(f)
            
            # Return the number of enrolled students
            return len(course_data.get('enrolled_students', []))
        
        except FileNotFoundError:
            print(f"Error: Course with Code {course_code} was not found.")
            return 0
        except json.JSONDecodeError:
            print("Error reading course data.")
            return 0
    
    def view_students(instructor):
        while True:
            print("\n--- VIEW STUDENTS ---")
            print("1 - View by Course Code")
            print("2 - Back to Course Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                # Get the course code the instructor wants to view students for
                course_code = input("Enter Course Code: ")
                
                # First, verify if this course is assigned to the instructor
                try:
                    with open(f'data/users/{instructor._user_id}_instructor_profile.json', 'r') as f:
                        instructor_profile = json.load(f)
                    
                    # Check if the course is assigned to this instructor
                    course_assigned = any(
                        course.get('course_code') == course_code 
                        for course in instructor_profile.get('assigned_courses', [])
                    )
                    
                    if not course_assigned:
                        print("This course is not assigned to you or course doesn't exist.")
                        continue
                except FileNotFoundError:
                    print("Instructor profile not found.")
                    continue
                
                # Collect students enrolled in this course
                students_data = []
                
                # Scan through all student profile files
                import os
                student_files = [f for f in os.listdir('data/users') if f.endswith('_student_profile.json')]
                
                for student_file in student_files:
                    try:
                        with open(os.path.join('data/users', student_file), 'r') as f:
                            student_profile = json.load(f)
                        
                        # Check if student is enrolled in the specified course
                        enrolled_in_course = any(
                            course.get('course_code') == course_code 
                            for course in student_profile.get('courses', [])
                        )
                        
                        if enrolled_in_course:
                            students_data.append([
                                student_profile['user_id'],
                                student_profile['name'],
                                student_profile['email'],
                                student_profile['major'],
                                student_profile['year_level'],
                                student_profile['semester'],
                                student_profile['academic_year'],
                            ])
                    except (FileNotFoundError, json.JSONDecodeError):
                        continue
                
                # Display students using tabulate
                if students_data:
                    print(f"\nStudents Enrolled in Course {course_code}:")
                    print(tabulate(students_data, 
                                headers=["Student ID", "Name", "Email", "Major", "Year Level", "Semester", "Academic Year"], 
                                tablefmt="grid"))
                    total_students = Course.get_enrolled_students_count(course_code)
                    print(f"Total Enrolled Students: {total_students}\n")
                else:
                    print(f"No students found enrolled in course {course_code}.")
            
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please try again.")



    def student_drop_course(student):
        # Define student file path
        student_file_path = f"data/users/{student._user_id}_student_profile.json"

        student_id = student._user_id if hasattr(student, '_user_id') else student.get('user_id')
        if not student_id:
            print("Error: Student ID not found.")
            return

        try:
            # Load student JSON data
            if not os.path.exists(student_file_path):
                print("Student file not found.")
                return

            with open(student_file_path, 'r') as student_file:
                student_data = json.load(student_file)

            # Display available courses
            if "courses" not in student_data or not student_data["courses"]:
                print("No courses found in your profile.")
                return

            # Prepare courses for tabular display
            table = []
            for course in student_data["courses"]:
                table.append([course["course_code"], course["course_name"], course["credited_units"], course["day"], f"{course['start_time']} - {course['end_time']}"])
            
            print("\nYour enrolled courses:")
            print(tabulate(table, headers=["Course Code", "Course Name", "Units", "Day", "Time"], tablefmt="grid"))

            # Prompt student to enter the course to drop
            course_code = input("\nEnter the course code of the course you want to drop: ").strip()
            
            # Check if the course exists
            course_found = None
            for course in student_data["courses"]:
                if course["course_code"] == course_code:
                    course_found = course
                    break
            
            if not course_found:
                print("You are not enrolled in this course or it does not exist.")
                return

            # Confirm the action
            confirm = input(f"Are you sure you want to drop the course '{course_code}: {course_found['course_name']}'? (yes/no): ").strip().lower()
            if confirm != "yes":
                print(f"Dropping of course {course_code} is cancelled.")
                return

            # Remove the course from student's profile
            student_data["courses"] = [
                course for course in student_data["courses"] if course["course_code"] != course_code
            ]

            # Save updated student data
            with open(student_file_path, 'w') as student_file:
                json.dump(student_data, student_file, indent=4)
            print(f"Course {course_code} successfully removed from your profile.")
            
            # Define course file path
            course_file_path = f"data/courses/{course_code}_course.json"
            if not os.path.exists(course_file_path):
                print("Course file not found, but it was removed from your profile.")
                return

            # Load course JSON data
            with open(course_file_path, 'r') as course_file:
                course_data = json.load(course_file)

            # Remove the student from the course's enrolled_students list
            course_data["enrolled_students"] = [
                student for student in course_data.get("enrolled_students", [])
                if student["student_id"] != student_id
            ]

            # Save updated course data
            with open(course_file_path, 'w') as course_file:
                json.dump(course_data, course_file, indent=4)
            print(f"Your enrollment in course '{course_code}' has been successfully removed.")

        except Exception as e:
            print(f"An error occurred: {e}")
