from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add')
def add_student():
    return render_template('add_student.html')


@app.route('/save', methods=['POST'])
def save_student():

    name = request.form['name']
    roll_no = request.form['roll_no']
    branch = request.form['branch']
    year = request.form['year']
    email = request.form['email']
    phone = request.form['phone']

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO students
        (name,roll_no,branch,year,email,phone)
        VALUES(?,?,?,?,?,?)
        ''',
        (name,roll_no,branch,year,email,phone)
    )

    conn.commit()
    conn.close()

    return "Student Saved Successfully!"


@app.route('/students')
def students():

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'students.html',
        students=students
    )


@app.route('/edit/<int:id>')
def edit_student(id):

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_student.html',
        student=student
    )


@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):

    name = request.form['name']
    roll_no = request.form['roll_no']
    branch = request.form['branch']
    year = request.form['year']
    email = request.form['email']
    phone = request.form['phone']

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        UPDATE students
        SET name=?,
            roll_no=?,
            branch=?,
            year=?,
            email=?,
            phone=?
        WHERE id=?
        ''',
        (
            name,
            roll_no,
            branch,
            year,
            email,
            phone,
            id
        )
    )

    conn.commit()
    conn.close()

    return "Student Updated Successfully!"


@app.route('/delete/<int:id>')
def delete_student(id):

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return "Student Deleted Successfully!"



@app.route('/search', methods=['POST'])
def search_student():

    keyword = request.form['keyword']

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM students
        WHERE name LIKE ?
        OR roll_no LIKE ?
        """,
        (
            '%' + keyword + '%',
            '%' + keyword + '%'
        )
    )

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'students.html',
        students=students
    )

@app.route('/add_marks')
def add_marks():
    return render_template('add_marks.html')


@app.route('/save_marks', methods=['POST'])
def save_marks():

    student_id = request.form['student_id']

    c_marks = int(request.form['c_marks'])
    python_marks = int(request.form['python_marks'])
    dbms_marks = int(request.form['dbms_marks'])
    java_marks = int(request.form['java_marks'])

    total = c_marks + python_marks + dbms_marks + java_marks

    percentage = total / 4

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    else:
        grade = "D"

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO marks
        (student_id,c_marks,python_marks,
        dbms_marks,java_marks,total,
        percentage,grade)
        VALUES(?,?,?,?,?,?,?,?)
        ''',
        (
            student_id,
            c_marks,
            python_marks,
            dbms_marks,
            java_marks,
            total,
            percentage,
            grade
        )
    )

    conn.commit()
    conn.close()

    return "Marks Saved Successfully!"


@app.route('/marks')
def view_marks():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM marks")
    data = cursor.fetchall()

    conn.close()

    return render_template('marks.html', marks=data)
    
@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM marks")
    total_marks = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(percentage) FROM marks")
    highest_percentage = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(percentage) FROM marks")
    average_percentage = cursor.fetchone()[0]

    cursor.execute("""
        SELECT students.name, marks.percentage, marks.grade
        FROM students
        JOIN marks
        ON students.roll_no = marks.student_id
        ORDER BY marks.percentage DESC
        LIMIT 1
    """)

    topper = cursor.fetchone()  
    print(topper)

    conn.close()

    if highest_percentage is None:
        highest_percentage = 0

    if average_percentage is None:
        average_percentage = 0

    return render_template(
        'dashboard.html',
        total_students=total_students,
        total_marks=total_marks,
        highest_percentage=round(highest_percentage, 2),
        average_percentage=round(average_percentage, 2),
        topper=topper
    )



@app.route('/check')
def check():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM marks")
    marks = cursor.fetchall()

    conn.close()

    return f"Students: {students}<br><br>Marks: {marks}"

if __name__ == '__main__':
    app.run(debug=True)