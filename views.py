from flask import render_template,current_app, request, redirect,url_for,session,flash
from classes import Class, Student, Teacher, Quiz, Question, Result
from database import Database
from functools import wraps
from passlib.hash import pbkdf2_sha256 as hasher
db = Database()
def main():
    db = current_app.config["db"]
    list_teachers = db.get_teachers()
    list_students = db.get_students()
    list_lectures = db.get_classes_with_teachers()
    return render_template("index.html",teachers = reversed(list_teachers),students = reversed(list_students),lectures = reversed(list_lectures))

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
           # flash('You need to login', 'danger')
            return redirect(url_for('main'))

    return wrap

def signUp():
    if request.method == "POST":
        form_name = request.form["fname"]
        form_surname = request.form["lname"]
        form_id = request.form["ownid"]
        form_email = request.form["Email"]
        form_password = hasher.hash(request.form["password"])
        form_person = request.form["person"]
        db = current_app.config["db"]
        if request.form["password"] != request.form["confirm_password"]: #for error
            password_error = "Passwords not matching! Try Again"
            return render_template('signup.html',password_error = password_error)

        if db.check_exists_student_id(form_id) or db.check_exists_teacher_id(form_id): #for error
            error = "The ID exists! Try Again"
            return render_template('signup.html',error = error)

        if db.check_exists_student_email(form_email) or db.check_exists_teacher_email(form_email): #for error
            error = "The email has already used!"
            return render_template('signup.html',error = error)

        if form_person == "teacher":
            teacher = Teacher(form_id,form_name,form_surname,form_email,form_password)
            teacher_key = db.add_teacher(teacher)
            return redirect(url_for("successful", teacher_key = teacher_key))

        elif form_person == "student":
            student = Student(form_id,form_name,form_surname,form_email,form_password)
            student_key = db.add_student(student)
            return redirect(url_for("successful", student_key = student_key))
        else: 
            return "person is not chosen!"
    else:
        return render_template('signup.html')

def successful():
    return render_template("successful.html")


def student_page():  # student sign in page
    if request.method == "POST":
        user = Student("","","","","")
        user.email = request.form['email']
        user.password = request.form['password']
        result = db.get_student(user.email)

        if result:
            password2 = result['student_password']
            if hasher.verify(user.password,password2):
                session['logged_in'] = True
                session['s-email'] = user.email
                session['s-name'] = result['student_name']
                session['s-surname'] = result['student_surname']
                session['s-id'] = result['student_id']
                flash('You are now logged in', 'success') #??
                return redirect(url_for('student_main_page',name=result['student_name']))
            else:
                error = " Wrong password!"
                return render_template('student_sign.html',error = error)

        else:
            error = " Email not found!"
            return render_template('student_sign.html',error = error)

    return render_template('student_sign.html')


def teacher_page(): # teacher sign in page
    if request.method == "POST":
        user = Teacher("","","","","")
        user.email = request.form['email']
        user.password = request.form['password']
        result = db.get_teacher(user.email)

        if result:
            password2 = result['teacher_password']
            if hasher.verify(user.password,password2):
                session['logged_in'] = True
                session['email'] = user.email
                session['name'] = result['teacher_name']
                session['surname'] = result['teacher_surname']
                session['id'] = result['teacher_id']

                flash('You are now logged in', 'success') #??

                return redirect(url_for('teacher_main_page'))
            else:
                error = " wrong password !"
                return render_template('teacher_sign.html',error = error)

        else:
            error = " email not found !"
            return render_template('teacher_sign.html',error = error)

    return render_template('teacher_sign.html')



@is_logged_in
def teacher_main_page():
    db = current_app.config["db"]
    name = session['name']
    surname = session['surname']
    email = session['email']
    tid = session['id']
    teacher_ = db.get_teacher(None,tid)
    list_classes = db.get_t_classes(tid)
    number_of_classes = db.count_class_of_teacher(tid)
    return render_template("teacher_main_classes.html",classes = list_classes,teacher_ = teacher_, tid=tid, number_of_classes = number_of_classes)

@is_logged_in
def update_teacher():
    db = current_app.config["db"]
    if request.method =="POST":
        new_name = request.form["new_name"]
        new_surname = request.form["new_surname"]
        new_email = request.form["new_email"]
        old_password = request.form["cur_password"]
        if request.form["new_password"] == '':
            new_password = ''
        else:
            new_password = hasher.hash(request.form["new_password"])

        if db.check_exists_teacher_email(new_email) or db.check_exists_student_email(new_email): #for error
            teacher_ = db.get_teacher(None,session['id'])
            error = "The email exists! Try Again"
            return render_template("update.html",error=error,teacher_id = session['id'],teacher_ = teacher_)

        db_password = db.get_teacher_password(session['id'])
        if old_password != '' and request.form["new_password"] != '':
            if hasher.verify(old_password,db_password) == 0 :  # if old password is wrong it returns false
                teacher_ = db.get_teacher(None,session['id'])
                error = "The current password is wrong! Try again"
                return render_template("update.html",error=error,teacher_id = session['id'],teacher_ = teacher_)
        if (old_password == '') ^ (request.form["new_password"] == ''):
            teacher_ = db.get_teacher(None,session['id'])
            error = "Password can not change, fill the blank correctly!"
            return render_template("update.html",error=error,teacher_id= session['id'],teacher_ = teacher_)

        db.update_teacher(session['id'],new_name,new_surname,new_email,new_password)
        return redirect(url_for("teacher_main_page"))

    else:
        teacher_ = db.get_teacher(None,session['id'])
        return render_template("update.html",teacher_id = session['id'],teacher_ = teacher_)

@is_logged_in
def delete_teacher():
    db = current_app.config["db"]
    db.delete_teacher(session['id'])
    list_teachers = db.get_teachers()
    list_students = db.get_students()
    list_lectures = db.get_classes_with_teachers()
    message = "Your account has been deleted successfully"
    return render_template("index.html",message = message,teachers = reversed(list_teachers),students = reversed(list_students),lectures = reversed(list_lectures))


@is_logged_in
def create_class():
    if request.method == "POST":
        form_class_code = request.form["class_code"]
        form_class_name = request.form["class_name"]
        new_class = Class(form_class_name,form_class_code,session['id'])
        db = current_app.config["db"]

        if db.check_exists_class_code(form_class_code):
            error = "The CRN exists !  Enter class code again"
            return render_template("create_class.html",error = error)
        class_key = db.add_class(new_class)

        return redirect(url_for("teacher_main_page", class_key = class_key))
    else:
        return render_template("create_class.html")


@is_logged_in
def delete_class(class_id):
    db = current_app.config["db"]
    db.delete_class(class_id)
    return redirect(url_for("teacher_main_page"))

@is_logged_in
def update_class(class_id):
    db = current_app.config["db"]
    if request.method =="POST":
        new_name = request.form["new_name"]
        db.update_class(class_id,new_name)
        return redirect(url_for("teacher_main_page"))

    else:
        class_ = db.get_class(class_id)
        return render_template("update.html",class_id = class_id,class_ = class_)

@is_logged_in
def main_quizzes(class_id):
    db = current_app.config["db"]
    list_quizzes = db.get_c_quizzes(class_id)
    tid = session['id']
    list_classes = db.get_t_classes(tid)
    return render_template("teacher_main_quizzes.html",classes = list_classes,class_id = class_id, quizzes = sorted(list_quizzes))


@is_logged_in
def create_quiz(class_id):
    if request.method =="POST":
        db = current_app.config["db"]
        form_quiz_title = request.form["title"]
        form_quiz_time = request.form["time"]
        new_quiz = Quiz(" ",form_quiz_title,form_quiz_time,class_id)
        quiz_id = db.add_quiz(new_quiz)
        quest_id = 1
        form_question = request.form["question"]
        form_A = request.form["A"]
        form_B = request.form["B"]
        form_C = request.form["C"]
        form_D = request.form["D"]
        correct = request.form["correct"]
        new_question = Question(quest_id, quiz_id, form_question, form_A, form_B, form_C, form_D, correct)
        db.add_question_into_quiz(quiz_id,new_question)

        i = 1
        while True:
            i += 1
            quest_id += 1
            if f"question-{i}" not in request.form :
                break
            form_question = request.form[f"question-{i}"]
            form_A = request.form[f"A-{i}"]
            form_B = request.form[f"B-{i}"]
            form_C = request.form[f"C-{i}"]
            form_D = request.form[f"D-{i}"]
            correct = request.form[f"correct-{i}"]
            new_question = Question(quest_id, quiz_id, form_question, form_A, form_B, form_C, form_D, correct)
            db.add_question_into_quiz(quiz_id,new_question)

        return redirect(url_for("main_quizzes", class_id = class_id,quiz_key = quiz_id))
    else:
        return render_template("create_quiz.html",class_id = class_id)

@is_logged_in
def delete_quiz(quiz_id):
    db = current_app.config["db"]
    quiz_ = db.get_quiz(quiz_id)
    db.delete_quiz(quiz_id)
    return redirect(url_for("main_quizzes",class_id = quiz_[3]))

@is_logged_in
def update_quiz(quiz_id):
    db = current_app.config["db"]
    if request.method =="POST":
        new_name = request.form["new_name"]
        db.update_quiz(quiz_id,new_name)
        quiz_ = db.get_quiz(quiz_id)
        return redirect(url_for("main_quizzes",class_id = quiz_[3]))

    else:
        quiz_ = db.get_quiz(quiz_id)
        return render_template("update.html",quiz_id = quiz_id ,quiz_ = quiz_)

@is_logged_in
def questions(quiz_id):
    db = current_app.config["db"]
    list_questions = db.get_questions(quiz_id)
    quiz_ = db.get_quiz(quiz_id)
    quest_number = db.get_q_number(quiz_id)
    return render_template("questions.html", quiz_id =quiz_id,quiz = quiz_, questions_data = list_questions,question_number = quest_number)


@is_logged_in
def update_question(question_id,quiz_id):
    db = current_app.config["db"]
    if request.method =="POST":
        new_name = request.form["correct"]
        db.update_question(question_id,new_name)
        return redirect(url_for('questions',quiz_id = quiz_id))

    else:
        questions =  db.get_questions(quiz_id)
        question_ = questions[0]
        return render_template("update.html",question_ = question_)

def delete_question(question_id,quiz_id):
    db = current_app.config["db"]
    db.delete_question(question_id)
    return redirect(url_for("questions",quiz_id = quiz_id))
    


@is_logged_in
def results(quiz_id):
    db = current_app.config["db"]
    results = db.get_scores_with_students(quiz_id)
    quiz_ = db.get_quiz(quiz_id)
    average = db.get_average_score(quiz_id)
    class_id = quiz_[3]
    number = len(results)
    return render_template("results.html", results = results, class_id = class_id,number= number,average = average)



# STUDENT's OPERATIONS

@is_logged_in
def student_main_page(): # show all classes
    db = current_app.config["db"]
    name = session['s-name']
    surname = session['s-surname']
    list_classes = db.get_classes_with_teachers()
    
    return render_template("show_classes.html",classes =list_classes,name=name,surname =surname)

@is_logged_in
def update_student():
    db = current_app.config["db"]
    if request.method =="POST":
        new_name = request.form["new_name"]
        new_surname = request.form["new_surname"]
        new_email = request.form["new_email"]
        old_password = request.form["cur_password"]
        if request.form["new_password"] == '':
            new_password = ''
        else:
            new_password = hasher.hash(request.form["new_password"])

        if db.check_exists_teacher_email(new_email) or db.check_exists_student_email(new_email): #for error
            student_ = db.get_student(None,session['s-id'])
            error = "The email exists! Try Again"
            return render_template("update.html",error=error,student_id = session['s-id'],student_ = student_)

        db_password = db.get_student_password(session['s-id'])
        if old_password != '' and request.form["new_password"] != '':
            if hasher.verify(old_password,db_password) == 0 :  # if old password is wrong it returns false
                student_ = db.get_student(None,session['s-id'])
                error = "The current password is wrong! Try again"
                return render_template("update.html",error=error,student_id = session['s-id'],student_ = student_)
        if (old_password == '') ^ (request.form["new_password"] == ''):
            student_ = db.get_student(None,session['s-id'])
            error = "Password can not change, fill the blank correctly!"
            return render_template("update.html",error=error,student_id = session['s-id'],student_ = student_)

        db.update_student(session['s-id'],new_name,new_surname,new_email,new_password)
        return redirect(url_for("student_main_page"))

    else:
        student_ = db.get_student(None,session['s-id'])
        return render_template("update.html",student_id = session['s-id'],student_=student_)

@is_logged_in
def delete_student():
    db = current_app.config["db"]
    db.delete_student(session['s-id'])
    list_teachers = db.get_teachers()
    list_students = db.get_students()
    list_lectures = db.get_classes_with_teachers()
    message = "Your account has been deleted successfully"
    return render_template("index.html",message = message,teachers = reversed(list_teachers),students = reversed(list_students),lectures = reversed(list_lectures))

@is_logged_in
def show_quizzes_to_student(class_id):
    db = current_app.config["db"]
    list_quizzes = db.get_c_quizzes(class_id)
    name = session['s-name']
    surname = session['s-surname']

    return render_template("show_quizzes.html",quizzes = sorted(list_quizzes),class_id=class_id,name = name,surname=surname)

@is_logged_in
def exam_page(quiz_id):
    db = current_app.config["db"]
    correct_answers = []
    student_answers = []
    if request.method == "POST":
        student_id = session["s-id"]
        questions_ = db.get_questions(quiz_id)
        q_number = db.get_q_number(quiz_id)
        each_point = round((100 / q_number),2) # point of each question
        student_point = 100

        for i in range(q_number):
            correct_answers.append(questions_[i][6])
            student_answers.append(request.form[f"btnradio-{i+1}"])
            print(request.form[f"btnradio-{i+1}"])

        for i in range(q_number):
            print("-->>>",student_answers[i])
            print("-->>>",correct_answers[i])
            if correct_answers[i] != student_answers[i]:
                student_point -= each_point

        
        db.add_score(student_id,quiz_id,round(student_point,2))

        return redirect(url_for('result',quiz_id = quiz_id))
    else:
        if db.quiz_done_before(session["s-id"],quiz_id): 
            quiz_ = db.get_quiz(quiz_id)
            error = "You have completed this exam before."
            return render_template('quiz_start.html',error = error,quiz = quiz_)
        list_questions = db.get_questions(quiz_id)
        quiz_ = db.get_quiz(quiz_id)
        return render_template("quiz_start.html", quiz_id = quiz_id,quiz = quiz_, questions_data = list_questions,student_id = session["s-id"])

@is_logged_in
def result(quiz_id):
    db = current_app.config["db"]
    quiz_ = db.get_quiz(quiz_id)
    student_id = session["s-id"]
    student_name = session["s-name"]
    score = db.get_score(student_id,quiz_id)
    if score == 100:
        full = True
    else:
        full = False

    return render_template("result.html", student_name = student_name,student_id = student_id, score=score, quiz = quiz_,full=full)

@is_logged_in
def logout():
    session.clear()
    flash('You have been successfully logged out', 'success')
    return redirect(url_for('main'))




