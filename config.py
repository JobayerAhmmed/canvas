import os



# 
# UPDATE THESE
# 
hw_no = 1
api_url = 'https://canvas.xyz.edu'

root_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(root_dir, 'data')
files_dir = os.path.join(root_dir, 'files')

hw_dir = os.path.join(data_dir, 'hw' + str(hw_no))
grader_dir = os.path.join(hw_dir, 'grader')
submissions_dir = os.path.join(hw_dir, 'submissions')
submissions_with_grader_dir = os.path.join(hw_dir, 'submissions_with_grader')
student_reports_dir = os.path.join(hw_dir, 'student_reports')

api_key = open(os.path.join(files_dir, 'api_key.txt')).read().strip()
course_id = open(os.path.join(files_dir, 'course_id.txt')).read().strip()
assignment_id = open(os.path.join(files_dir, 'assignment_id.txt')).read().strip()
student_id_start = open(os.path.join(files_dir, 'student_id_start.txt')).read().strip()
student_id_end = open(os.path.join(files_dir, 'student_id_end.txt')).read().strip()

file_students = os.path.join(hw_dir, 'students.xlsx')
file_grades = os.path.join(hw_dir, 'grades.xlsx')
file_grades_unsorted = os.path.join(hw_dir, 'grades_unsorted.xlsx')

file_excel_columns = os.path.join(files_dir, 'excel_columns.txt')
file_grader_dir_struct = os.path.join(files_dir, 'grader_dir_structure.txt')
output_head = open(os.path.join(files_dir, 'output_head.txt')).read().strip()

# 
# UPDATE THESE
#
due_date_str = '2024-10-16 23:59:59'
extended_due_date_str = '2024-10-19 23:59:59'


class ColumnDict:
    def __init__(self, columns):
        self.__dict__.update(columns)

    def values(self):
        """Return the values of the attributes as a list."""
        return list(self.__dict__.values())

    def items(self):
        """Return the key-value pairs as a list of tuples."""
        return list(self.__dict__.items())


column_dict = {}
with open(file_excel_columns, 'r') as file:
    for line in file:
        line = line.strip()
        if '=' in line:
            key, value = line.split('=', 1)
            column_dict[key.strip()] = value.strip()

columns = ColumnDict(column_dict)
