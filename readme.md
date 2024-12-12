This project leverages the Canvas API to retrieve student data for an assignment of a course,
including assignment submissions, submission dates, and related metadata.
Submissions are downloaded, organized, and processed into a standardized
file structure, making it easy to review, grade, and analyze student work
efficiently.

You can use this repository to automate several manual steps in the grading
process, ultimately saving time and effort.


## Homework Description

Let assume that you are an instructor or teaching assistant, and there is a
programming assignment or homework in Canvas for which students will submit their code.
In the homework, suppose, students need to create a Java project.
The package structure of the project should be *edu.xyz.cs101.hw1*.
Students will create several Java files and write code in them.
Then, each student will compress the project and submit a zip file in Canvas.
The zip file name will be *FirstName_LastName_HW1.zip*.
For example, for student John Doe, the zip file name will be *John_Doe_HW1.zip*.

There will be rewards and penalty based on the submission date.
If a student submit before the deadline, s/he will get 1% extra grade of the received grades for each day.
On the other hand, if a student submit on the next day of the deadline, 10% penalty will be applied on the received grades.
And, if the submission is late beyond the next day of deadline, it will be 100% penalty.

The typicall directory structure in the project will be *John_Doe_HW1/src/edu/xyz/cs101/hw1*.
The Java files written by students are inside the *hw1* directory.
Let say you have an automatic grader that grades the project.
The directory structure in the grader project is same like the students, *grader/src/edu/xyz/cs101/hw1*.
To grade the project, you need to copy the student Java files into the *hw1* directory of the grader.
After this process, you will open the grader in Eclips IDE, run and grade the project.
When the grading is done, you will also create a output.txt file with comments and grades
for submitting that into Canvas as student feedback.

So, in this process, we will perform the following steps - 
1. Setup the environment
2. Generate access token in Canvas
3. Get student names and ids
4. Create an excel with student names, ids and other columns
5. Download the student submissions
6. Calculate late hours after deadline
7. Calculate early days before deadline
8. Prepare student submissions for grading
9. Set formulas in excel columns
10. Grade student submissions
11. Create student report files


## Step 1: Setup Environment 

1. We will use Python programming language. Make sure that Python 3 is installed.

    To check if Python 3 is installed on your system, you can use the command line
    - Open a Terminal (on Linux/macOS) or Command Prompt (on Windows).
    - Run the following command
        - `python3 --version` (on Linux/macOS)
        - `python --version` (on Windows)
    - If Python 3 is installed, you should see output showing the version number,
      like *Python 3.x.y* (where x and y are any number).

    If Python 3 is not installed, you need to install it.
    Follow the official documentation of Python or you can read the Python wiki 
    [page](https://wiki.python.org/moin/BeginnersGuide/Download) to install it.

    *In the rest of the instructions, we will use *python3* in all of the commands.
    You should use *python3* or *python* based on your system, whichever works for you.*

2. Download the repo [https://github.com/JobayerAhmmed/canvas](https://github.com/JobayerAhmmed/canvas)
as zip and extract it, or clone the repo using git.

3. Open a terminal and go to the *canvas* repo directory

4. Create a virtual environment to avoid system-wide installation of libraries
    - `python3 -m venv .venv` (.venv is the name of the virtual environment)

5. Activate the virtual environment
    - `source .venv/bin/activate` (Linux/macOS)
    - `.venv\Scripts\activate` (Windows)

6. Install necessary Python libraries.
    - `pip install canvasapi pandas openpyxl progressbar2`

    ***Note:** Whenever you need to work on this project, you need to activate
    the virtual environment, otherwise, Python might not find the installed libraries.
    When you are done, you can deactivate the environment using the command `deactivate`.*

## Step 2: Generate Access Token in Canvas

1. Login to Canvas from any browser

2. Go to *Account* -> *Settings*

3. Click on the *New Access Token* button and generate an access token

4. Copy and save the token in the *api_key.txt* file which is located 
under the *files* directory of *canvas* repo that you downloaded/cloned


## Step 3: Get Student Names and IDs

Suppose, there are 400 students in the course and you want to grade submissions
for a specific range of students, for example, from student John Doe to Jane Smith, 
according to the SpeedGrader in Canvas. If you want to grade all students, you
don't need to know the start and end student ids.

We need to know API endpoint, course ID, assignment ID, start and
end student IDs. Lets find those and update the files.

1. **API endpoint:** Open a browser and login to Canvas, if you have not done it yet.
The URL that you are in is typically the API endpoint, something like *https://canvas.xyz.edu*.
So copy the URL and update the value of `api_url` variable in *config.py* file.

2. **Assignment No (optional):** Set the `hw_no` variable value in *config.py* file. The default value is set to 1.

3. **Course ID:** Open the course by clicking on the course link.
Now, look into the URL and you will see something like *https://canvas.xyz.edu/courses/000000*.
Here, number 000000 is the course id. Update file *files/course_id.txt* with this number.

4. **Assignment ID:** Click on the *Assignments* (or, whatever name is used 
for assignments in your course) from the left menu.
Then, click on to the specific assignment, lets say, it is named as *hw1*.
Now, look into the URL and you will see something like *https://canvas.xyz.edu/courses/000000/assignments/1111111*.
Here, number 1111111 is the assignment id. Save this number to *files/assignment_id.txt*.

5. **Start and End Student IDs:** Click on the SpeedGrader. In SpeedGrader, you find each student's submission. 
You can move back and forth using the left/right arrow to find previous/next student's submission.
And, using the dropdown option &#8595;, you can see all the students' names.
Select student John Doe and look into the URL. You will see something like *student_id=222222* at the end of the URL.
222222 is the student ID for John Doe. Save the id to *files/student_id_start.txt*.
Do the same for Jane Smith and update file *files/student_id_end.txt*.

6. Get the student names and IDS, and save them in an excel file.
    - Go to the terminal that was previously opened or open a terminal in *canvas* directory
    - Run: `python3 get_students.py`
    - When finished, open file *students.xlsx* from *data/hw1* 
      and you will see students from John Doe to Jane Smith.
      The first name and last name are joined by underscore (_).


## Step 4: Create Excel with Columns

In SpeedGrader, the students are ordered by the last names.
File *students.xlsx* contains student names in the order found in SpeedGrader.
So, to make it easier finding the student submission directories in the file explorer, we will 
create a new excel with student names and ids, and this time, they will be **sorted**
by the first names. The excel will contain the following columns:

- `Student Name`
- `Student ID`
- `Submitted At`: date and time when the submission happened
- `Late Hours`: late hour count
- `Early Days`: early day count
- `Late Deduct`: >0 && <24 hours = 10% penalty, >=24 hours = 100% penalty
- `Early Points`: each day (max 10 days) yields 1% extra score of the total score

You can create other columns according to your needs.
Let say, you have other cloumns like - 

- `Auto Grading`: score given by the automatic grader
- `Manual Grading`: score obtained by manually checking the Java files are according to the requirments
- `Total`: total grade after summing all columns
- `Comments`: this column contains any comments or feedback you want to provide to the student

Now, lets create the excel.

1. Update file *files/excel_columns.txt* with the above column names. 
   Each line in the file should contain one column name key and column name separated by =. Do not change the
   order of the first five column names in the .txt file, from Student Name to
   Early Days, otherwise, the code will not work.

2. Run: `python3 create_excel.py`. It will create *grades.xlsx* file with the column names.


## Step 5: Download Submissions

In this step, you will download each student's latest submission from Canvas.
Also the *Submitted At* column will be updated in *grades.xlsx* file.

1. Update function `convert_utc_to_iowa()` in *utils.py* file. This function
   converts UTC time to Iowa local time. Just change the hours argument in timedelta.

2. Run: `python3 download_submissions.py`

3. Open *grades.xlsx* and you will find *Submitted At* column is updated with submission time.
   If the time is shown as #####, just increase the column width, and it will be visible as normla date and time.
   Also, the student submitted zip files will be at *data/hw1/submissions* directory.

## Step 6: Calculate Late Hours

1. Update `due_date_str` and `extended_due_date_str` variables in *config.py*.
   Due date is the date you expect the students to submit within.
   Extend due date is a 1-2 days of grace period, meaning students can submit till this date
   without any penalty. If you do not have any extended due date, use the same 
   date value of `due_date_str` to `extended_due_date_str`.

2. Run: `python3 calculate_late_hours.py`


## Step 7: Calculate Early Days

1. Run: `python3 calculate_early_days.py`


## Step 8: Set Equations in Excel

Open the *grades.xlsx* and set necessary equations in the columns so that they automatically
calculate values. These are sample formulas, you might need to change them according to your need.

1. Late Deduct: `=IF(AND(D2>0,D2<24),SUM(H2:I2)*(-0.1),IF(D2>=24,SUM(H2:I2)*(-1),0))`

2. Early Points: `=IF(AND(E2>0,E2<=10),SUM(H2:I2)*(E2*0.01),IF(E2>10,SUM(H2:I2)*(10*0.01),0))`

3. Total: `=CEILING(SUM(F2:I2),1)`


## Step 9: Prepare Submissions for Grading

In this step, you will extract all zip files, make a copy of the grader for each student,
and copy the Java files to *hw1* directory (last directory inside the grader).

1. Copy the grader into the *data/hw1* directory, (rename the grader directory to *grader* if it is not).
If the grader is a zip file, extract it using: `unzip data/hw1/HW1_Grader.zip -d data/hw1/grader`

2. Update file *files/grader_dir_structure.txt*
with the directory names. Each line should contain one directory name, starting from *src* to *hw1*.
In the homework description, you assumed that the directory structure of the 
grader is *grader/src/edu/xyz/cs101/hw1*.

3. Run: `python3 prepare_for_grading.py`

4. When done, you will find that each zip file is extracted in the *data/hw1/submissions* directory.
Moreover, there will be a new directory named *submissions_with_grader* inside the *data/hw1* directory.
Here, for each student, there will be a Java project. The grader is copied for each student and also
the Java files found inside *data/hw1/submissions/John_Doe/src/edu/xyz/cs101/hw1* 
are copied to *data/hw1/submissions_with_grader/John_Doe/src/edu/xyz/cs101/hw1*.
Now, all the submissions inside the *data/hw1/submissions_with_grader* are ready to grade.


## Step 10: Grading

1. Open each student's project in Eclipse from the *data/hw1/submissions_with_grader* directory and grade it.
2. Update *grades.xlsx* file for each student.

## Step 11: Create Student Report Files

When you are done with grading, you can create a report for each student with the grades
and your feedback, so that you can submit these to students in Canvas.

1. Run: `python3 unsort_grades.py`. In step 4, you sorted by student first names.
This script will create a new excel *grades_unsorted.xlsx* with the content of *grades.xlsx*,
but the students will be ordered according to the last name, which was initially 
in *students.xlsx* file, same as SpeedGrader. This will help in submitting the
grades manually in Canvas.

2. Update file *files/output_head.txt*. It contains the header of the formatted output you want to create.

3. Run: `python3 create_student_reports.py`. It will create a feedback file for each student inside *data/hw1/student_reports*.
The file will contain the column values from *grades_unsorted.xlsx* for each student.

4. YOU ARE DONE HERE! Now, go to the assignment in Canvas, open SpeedGrader, 
and submit the grades and feedback files for each student.

