#creating the UChicago course selection algorithm using the restrictions of the College

#COURSES CLASS
weekdays = "MTWRF"
class Course:
    def __init__(self, dept, num, title, days, start, end, pqs):
    
        if not isinstance(dept, str):
            raise TypeError("Department name must be a string.")
            
        if len(dept) != 4:
            raise ValueError("Department name must be 4 letters long.")
        
        if not isinstance(num, int):
            raise TypeError("Course number must be an integer.")
        
        if not 0 <= num <= 99999:
            raise ValueError("Course number must be between 0 and 99999, inclusive.")
       
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        
        if not isinstance(days, str):
            raise TypeError("Days input must be a string.")
        
        if any(letter not in 'MTWRF' for letter in days):
            raise ValueError("Days input is not a valid day.")
        
        for letter in days:
            if days.count(letter) > 1:
                raise ValueError("A day must not appear more than once.")
                
        if len(days) > 5:
            raise ValueError("A course can be given max. 5 times a week.")
            
        if not isinstance(start, int):
            raise TypeError("Time values must be integers.")

        if not isinstance(end, int):
            raise TypeError("Time values must be integers.")
            
        if start > end:
            raise ValueError("The end time cannot be before the start time.")
            
        if not 0.0 <= (start % 100) <= 0.59:
            raise ValueError("Start time minutes are not valid.")
            
        if not 0 <= (start // 100) <= 23:
            raise ValueError("Start time hour is not valid.")
            
        if not 0.0 <= (end % 100) <= 0.59:
            raise ValueError("End time minutes are not valid.")
            
        if not 0 <= (end // 100) <= 23:
            raise ValueError("End time hour is not valid.")
            
        if not isinstance(pqs, set):
            raise TypeError("Prerequisites must be a set.")
            
        self.dept = dept
        self.num = num
        self.title = title
        self.days = days
        self.start = start
        self.end = end
        self.pqs = pqs
            
    def course_code(self):
        return str(self.dept + " " + str(self.num))
    
    def with_title(self):
        return str(self.dept + " " + str(self.num) + ": " + self.title)
        
    def conflicts_with(self, second):
        for i in second.days:
            if i in self.days:
                if max(self.start, second.start) < min(self.end, second.end):
                    return True
                else:
                    return False
            else:
                return False
                
    def prereqs_met(self, passed_courses):
        for i in self.pqs:
            if i in passed_courses:
                return True
            else:
                return False

#STUDENTS CLASS

class Student:
    def __init__(self, name, sid):
        self.name = name
        self.sid = sid
        self.transcript = []
        self.enrollment = []
        
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        
        if not isinstance(sid, int):
            raise TypeError("Student ID must be an integer.")
        
    def gpa(self):
        if len(self.transcript) == 0:
            raise ValueError("No courses have been completed.")
        else:
            total_grades = []
            for i in self.transcript:
                if i[1] == "A":
                    total_grades.append(4.0)
                if i[1] == "A-":
                    total_grades.append(3.7)
                if i[1] == "B+":
                    total_grades.append(3.3)
                if i[1] == "B":
                    total_grades.append(3.0)
                if i[1] == "B-":
                    total_grades.append(2.7)
                if i[1] == "C+":
                    total_grades.append(2.3)
                if i[1] == "C":
                    total_grades.append(2.0)
                if i[1] == "C-":
                    total_grades.append(1.7)
                if i[1] == "D+":
                    total_grades.append(1.3)
                if i[1] == "D":
                    total_grades.append(1.0)
                if i[1] == "F":
                    total_grades.append(0.0)
            return sum(total_grades) / len(total_grades)
            
    def finish_quarter(self, list_grades):
        courses_enrolled = []
        for i in self.enrollment:
            courses_enrolled.append(course_code(i))
        for k in list_grades:
            if k[0] in courses_enrolled:
                self.transcript.append(k)
                for j in self.enrollment:
                    if course_code(j) == k[0]
                        self.enrollment.remove(j)
            else:
                raise ValueError("Course does not match with enrolled courses.")
                
    def enroll(self, courses_obj):
        for i in self.enrollment:
            if conflicts_with(i, courses_obj):
                raise ValueError("There is a schedule conflict."')
            else:
                new = set()
                for j in self.transcript:
                    if j[1] != "F":
                        new.append(j[0])
                        if prereqs_met(courses_obj, new):
                            self.enrollment.append(courses_obj)
                    else:
                        raise ValueError("The prereqs for the course are not met.")
