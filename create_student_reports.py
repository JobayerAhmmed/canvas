import os
import shutil
import time

from openpyxl import load_workbook
import progressbar

import config
from config import columns
import utils



def create_output_txt():
    print('Creating student feedback files ...')

    wb = load_workbook(config.file_grades_unsorted, data_only=True)
    ws = wb.active

    headers = [cell.value for cell in ws[1]]
    student_name_index = headers.index(columns[0])
    submitted_at_index = headers.index(columns[2])

    for row in ws.iter_rows(min_row=2, values_only=True):
        student_name = str(row[student_name_index])
        submitted_at = str(row[submitted_at_index])
        if submitted_at == 'None':
            continue

        output_file_name = f'{student_name}.txt'
        output_file = os.path.join(config.submissions_with_grader_dir, 
                                   student_name, output_file_name)

        output_content = config.output_head + '\n\n'

        try:
            with open(output_file, 'w') as file:
                file.write(output_content)
                for col_name, value in zip(headers, row):
                    file.write(f"{col_name}: {value}\n")
        except Exception as e:
            print(f"Error for student {student_name}: {e}")

 
def copy_output_txt():
    print('Copying student feedback files ...')

    os.makedirs(config.student_reports_dir, exist_ok=True)

    wb = load_workbook(config.file_grades_unsorted, data_only=True)
    ws = wb.active

    student_name_col = utils.find_column(ws, columns[0])

    bar = progressbar.ProgressBar(max_value=ws.max_row,
                                  redirect_stdout=True).start()
    i = 1
    for row in range(2, ws.max_row + 1):
        student_name = ws.cell(row=row, column=student_name_col).value
        file_name = f'{student_name}.txt'
        src_file = os.path.join(config.submissions_with_grader_dir, student_name, file_name)
        dst_file = os.path.join(config.student_reports_dir, file_name)
        try:
            shutil.copy(src_file, dst_file)
        except FileNotFoundError:
            print(f"Error: The file {src_file} does not exist.")
        except PermissionError:
            print(f"Error: Permission denied to access {dst_file}.")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(1)
        i += 1
        bar.update(i)
    bar.finish()


if __name__ == "__main__":
    create_output_txt()
    copy_output_txt()
