import os

import pandas as pd
from canvasapi import Canvas
import progressbar

import config



def get_student_names_ids():
    print('Getting student names and ids ...')

    os.makedirs(config.hw_dir, exist_ok=True)

    canvas = Canvas(config.api_url, config.api_key)
    course = canvas.get_course(config.course_id)

    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    students = course.get_users(enrollment_type=['student'])
    bar.finish()

    student_data = []
    for student in students:
        student_data.append({'Student Name': student.name.replace(' ', '_'),
                             'Student ID': student.id})

    student_index = find_student_index_by_id(student_data,
                                             config.student_id_start)
    if student_index == -1:
        print(f"Cannot find student by id {config.student_id_start}")
    else:
        student_data = student_data[student_index:]

    student_index = find_student_index_by_id(student_data,
                                             config.student_id_end)
    if student_index == -1:
        print(f"Cannot find student by id {config.student_id_end}")
    else:
        student_data = student_data[:student_index+1]

    df = pd.DataFrame(student_data)
    df.to_excel(config.file_students, index=False)


def find_student_index_by_id(student_data, student_id):
    for index, student in enumerate(student_data):
        if student['Student ID'] == int(student_id):
            return index
    return -1


if __name__ == "__main__":
    get_student_names_ids()
