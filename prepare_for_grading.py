import os
import shutil
import zipfile

import pandas as pd

import config
from config import columns



def ready_submissions_for_grading():
    print('Making ready student submissions for grading ...')

    os.makedirs(config.submissions_with_grader_dir, exist_ok=True)

    df_grades = pd.read_excel(config.file_grades)

    for _, row in df_grades.iterrows():
        student_zip_file = os.path.join(config.submissions_dir, row[columns[0]] + '.zip')
        if not os.path.isfile(student_zip_file):
            continue

        student_submission_dir = os.path.join(config.submissions_dir, row[columns[0]])
        student_grading_dir = os.path.join(config.submissions_with_grader_dir, row[columns[0]])

        with open(config.file_grader_dir_struct, 'r') as file:
            dir_names = [line.strip() for line in file if line.strip()]
        student_grading_src_dir = os.path.join(student_grading_dir, *dir_names)

        copy_directory(config.grader_dir, student_grading_dir)
        remove_java_files(student_grading_src_dir)

        extract_zip(student_zip_file, student_submission_dir)
        copy_java_files(student_submission_dir, student_grading_src_dir)

        remove_zone_identifier(student_grading_dir)


def copy_directory(source_dir, target_dir):
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    os.makedirs(target_dir, exist_ok=True)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)

        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
        else:
            shutil.copy2(source_path, target_path)


def remove_java_files(directory):
    if not os.path.isdir(directory):
        print(f"The path '{directory}' is not a valid directory.")
        return

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item.endswith('.java'):
            os.remove(item_path)


def extract_zip(zip_file_path, extract_to_folder):
    os.makedirs(extract_to_folder, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)


def copy_java_files(source_directory, target_directory):
    os.makedirs(target_directory, exist_ok=True)

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.startswith('._'):
                continue
            if file.endswith('.java'):
                source_file_path = os.path.join(root, file)
                shutil.copy2(source_file_path, target_directory)


def remove_zone_identifier(directory):
    if not os.path.isdir(directory):
        print(f"The path '{directory}' is not a valid directory.")
        return
    
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('Zone.Identifier'):
                file_path = os.path.join(dirpath, filename)
                os.remove(file_path)


if __name__ == "__main__":
    ready_submissions_for_grading()