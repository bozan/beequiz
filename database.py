from classes import Class, Student, Teacher, Quiz, Question, Result
import psycopg2
import psycopg2.extras
#from user import Studentt
from passlib.hash import pbkdf2_sha256 as hasher
from views import *

class Database():
    def __init__(self):
        self.classes = {}
        self._last_class_key = 0
        self.teachers = {}
        self._last_teacher_key = 0
        self.students = {}
        self._last_student_key = 0
        self.quizzes = {}
        self._last_quiz_key = 0
        self._last_question_key = 0

        self.connection = psycopg2.connect(user="postgres",
                                    password="postgres21",
                                    database="beequiz")
        self.cur = self.connection.cursor()
# TEACHER #
    def add_teacher(self,new_teacher):
        with self.connection as conn:
            cursor = conn.cursor()
            insert_query = "INSERT INTO teacher (teacher_id, teacher_name, teacher_surname,teacher_email,teacher_password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query,(new_teacher.id,new_teacher.name,new_teacher.surname,new_teacher.email,new_teacher.password))
            conn.commit()
        self._last_teacher_key += 1
        self.teachers[self._last_teacher_key] = new_teacher
        return self._last_teacher_key

    def get_teacher(self,useremail=None,id=None):
        if id is not None:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                select_query = "SELECT * FROM teacher WHERE teacher_id =%s"
                cursor.execute(select_query,[id])
                result = cursor.fetchone()
            return result
        else:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                select_query = "SELECT * FROM teacher WHERE teacher_email =%s"
                cursor.execute(select_query,[useremail])
                result = cursor.fetchone()
            return result

    def get_teachers(self): # for last registered person (index.html)
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT * FROM teacher"
            cursor.execute(select_query)
            all_teachers = cursor.fetchall()
        return all_teachers

    def get_teacher_password(self,tid): # student
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT teacher_password FROM teacher WHERE teacher_id =%s"
            cursor.execute(select_query,[tid])
            current_pass = cursor.fetchone()
        return current_pass[0]

    def update_teacher(self,tid,name,surname,email,new_password):
        if name :
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                update_query = "UPDATE teacher SET teacher_name = %s WHERE teacher_id = %s"
                cursor.execute(update_query,(name,tid))
                self.connection.commit()
            session['name'] = name

        if surname :
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                update_query = "UPDATE teacher SET teacher_surname = %s WHERE teacher_id = %s"
                cursor.execute(update_query,(surname,tid))
                self.connection.commit()
            session['surname'] = surname

        if email :
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                update_query = "UPDATE teacher SET teacher_email = %s WHERE teacher_id = %s"
                cursor.execute(update_query,(email,tid))
                self.connection.commit()
            session['email'] = email

        if new_password and new_password !="":
            print("if new password exists")
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                update_query = "UPDATE teacher SET teacher_password = %s WHERE teacher_id = %s"
                cursor.execute(update_query,(new_password,tid))
                self.connection.commit()


    def delete_teacher(self,tid):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            delete_query = "DELETE FROM teacher WHERE teacher_id =%s"
            cursor.execute(delete_query,[tid])
            self.connection.commit()

    def check_exists_teacher_id(self,teacher_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            check_query = "SELECT EXISTS (select true from teacher where teacher_id=%s)"
            cursor.execute(check_query,[teacher_id])
            boolean = cursor.fetchone()
        return boolean[0]

    def check_exists_teacher_email(self,teacher_email):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            check_query = "SELECT EXISTS (select true from teacher where teacher_email=%s)"
            cursor.execute(check_query,[teacher_email])
            boolean = cursor.fetchone()
        return boolean[0]



# STUDENT #
    def add_student(self,new_student):
        with self.connection as conn:
            cursor = conn.cursor()
            insert_query = "INSERT INTO student (student_id, student_name, student_surname,student_email,student_password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query,(new_student.id,new_student.name,new_student.surname,new_student.email,new_student.password))
            conn.commit()
        self._last_student_key += 1
        self.students[self._last_student_key] = new_student
        return self._last_student_key

    def get_student(self,useremail=None,id=None):
        if id is not None:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                select_query = "SELECT * FROM student WHERE student_id =%s"
                cursor.execute(select_query,[id])
                result = cursor.fetchone()
            return result
        else:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                select_query = "SELECT * FROM student WHERE student_email =%s"
                cursor.execute(select_query,[useremail])
                result = cursor.fetchone()
            return result

    def get_students(self): # for last registered person (index.html)
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT * FROM student"
            cursor.execute(select_query)
            all_students = cursor.fetchall()
        return all_students

    def get_student_password(self,sid): # student
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT student_password FROM student WHERE student_id =%s"
            cursor.execute(select_query,[sid])
            current_pass = cursor.fetchone()
        return current_pass[0]


    def update_student(self,sid,name,surname,email,new_password):
        if name :
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                update_query = "UPDATE student SET student_name = %s WHERE student_id = %s"
                cursor.execute(update_query,(name,sid))
                self.connection.commit()
            session['s-name'] = name

        if surname :
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                update_query = "UPDATE student SET student_surname = %s WHERE student_id = %s"
                cursor.execute(update_query,(surname,sid))
                self.connection.commit()
            session['s-surname'] = surname

        if email :
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                update_query = "UPDATE student SET student_email = %s WHERE student_id = %s"
                cursor.execute(update_query,(email,sid))
                self.connection.commit()
            session['s-email'] = email

        if new_password :
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                update_query = "UPDATE student SET student_password = %s WHERE student_id = %s"
                cursor.execute(update_query,(new_password,sid))
                self.connection.commit()

    def delete_student(self,sid):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            delete_query = "DELETE FROM student WHERE student_id =%s"
            cursor.execute(delete_query,[sid])
            self.connection.commit()

    def check_exists_student_id(self,student_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            check_query = "SELECT EXISTS (select true from student where student_id=%s)"
            cursor.execute(check_query,[student_id])
            boolean = cursor.fetchone()
        return boolean[0]

    def check_exists_student_email(self,student_email):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            check_query = "SELECT EXISTS (select true from student where student_email=%s)"
            cursor.execute(check_query,[student_email])
            boolean = cursor.fetchone()
        return boolean[0]


# CLASS  #
    def add_class(self, new_class):
        with self.connection as conn:
            cursor = conn.cursor()
            insert_query = "INSERT INTO class (class_name, class_code, teacher_id) VALUES (%s, %s, %s)"
            cursor.execute(insert_query,(new_class.name,new_class.CRN,new_class.teacher_id))
            conn.commit()

        self._last_class_key += 1
        self.classes[self._last_class_key] = new_class
        return self._last_class_key

    def get_class(self,class_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT * FROM class WHERE class_code =%s"
            cursor.execute(select_query,[class_id])
            the_class  = cursor.fetchone()
            if the_class is None:
                return None
        return the_class

    def get_t_classes(self,teacher_id): # get specific classes belong to the theacher_id
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT * FROM class WHERE teacher_id =%s"
            cursor.execute(select_query,[teacher_id])
            all_t_classes  = cursor.fetchall()
        return all_t_classes


    def get_classes(self):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT * FROM class"
            cursor.execute(select_query)
            all_classes  = cursor.fetchall()
        return all_classes

    def delete_class(self,class_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            delete_query = "DELETE FROM class WHERE class_code =%s"
            cursor.execute(delete_query,[class_id])
            self.connection.commit()

    def update_class(self,class_id,new_name):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            update_query = "UPDATE class SET class_name = %s WHERE class_code = %s"
            cursor.execute(update_query,(new_name,class_id))
            self.connection.commit()

    def get_classes_with_teachers(self): # for last added lectures(index.html) with teacher name surname email
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT class_code, class_name, teacher_name,teacher_surname,teacher_email FROM teacher INNER JOIN class ON teacher.teacher_id = class.teacher_id"
            cursor.execute(select_query)
            all_lectures  = cursor.fetchall()
        return all_lectures
    
    def check_exists_class_code(self,class_code):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            check_query = "SELECT EXISTS (select true from class where class_code=%s)"
            cursor.execute(check_query,[class_code])
            boolean = cursor.fetchone()
        return boolean[0]
    
    def count_class_of_teacher(self,teacher_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            count_query = "SELECT teacher_id, COUNT(teacher_id) AS number_of_class FROM class WHERE teacher_id =%s GROUP BY teacher_id"
            cursor.execute(count_query,[teacher_id])
            number  = cursor.fetchone()
        return number[1]



# QUESTION #

# QUIZ #

    def add_quiz(self, new_quiz):
        with self.connection as conn:
            self._last_quiz_key += 1
            cursor = conn.cursor()
            insert_query = "INSERT INTO quiz (quiz_id, quiz_title, quiz_time, class_code) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query,(self._last_quiz_key,new_quiz.title,new_quiz.time,new_quiz.class_id))
            conn.commit()
        self.quizzes[self._last_quiz_key] = new_quiz
        return self._last_quiz_key
    
    def get_quiz(self,quiz_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT * FROM quiz WHERE quiz_id =%s"
            cursor.execute(select_query,[quiz_id])
            the_quiz  = cursor.fetchone()
            if the_quiz is None:
                return None
        return the_quiz

    def get_c_quizzes(self,class_id):  # get specific quizzes belong to the class_id
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT * FROM quiz WHERE class_code =%s"
            cursor.execute(select_query,[class_id])
            all_c_quizzes  = cursor.fetchall()
        return all_c_quizzes

    def delete_quiz(self,quiz_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            delete_query = "DELETE FROM quiz WHERE quiz_id =%s"
            cursor.execute(delete_query,[quiz_id])
            self.connection.commit()

    def update_quiz(self,quiz_id,new_name):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            update_query = "UPDATE quiz SET quiz_title = %s WHERE quiz_id = %s"
            cursor.execute(update_query,(new_name,quiz_id))
            self.connection.commit()

    def add_question_into_quiz(self,quiz_id,new_question):
        with self.connection as conn:
            self._last_question_key += 1
            cursor = conn.cursor()
            insert_query = "INSERT INTO question (quiz_id, question, a, b, c, d, correct) VALUES (%s,%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query,(quiz_id, new_question.form_question, new_question.form_A, new_question.form_B, new_question.form_C, new_question.form_D, new_question.correct))
            conn.commit()
        return None


    def get_questions(self,quiz_id): # get specific questions belong to the quiz_id
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            select_query = "SELECT * FROM question WHERE quiz_id =%s"
            cursor.execute(select_query,[quiz_id])
            all_questions  = cursor.fetchall() #şimdilik tek soruluk
        return all_questions  


    def get_q_number(self,quiz_id): # get question number in quiz_id
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            count_query = "SELECT COUNT (*) FROM question WHERE quiz_id =%s"
            cursor.execute(count_query,[quiz_id])
            quest_number  = cursor.fetchone()
        return quest_number[0]


    def update_question(self,question_id,new_name):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            update_query = "UPDATE question SET correct = %s WHERE question_id = %s"
            cursor.execute(update_query,(new_name,question_id))
            self.connection.commit()

    def delete_question(self,question_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            delete_query = "DELETE FROM question WHERE question_id =%s"
            cursor.execute(delete_query,[question_id])
            self.connection.commit()


    def add_score(self,student_id,quiz_id,score):
        with self.connection as conn:
            cursor = conn.cursor()
            insert_query = "INSERT INTO result (student_id,quiz_id,score) VALUES (%s,%s,%s)"
            cursor.execute(insert_query,(student_id,quiz_id,score))
            conn.commit()


    def  get_score(self,student_id,quiz_id): #for students
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            score_query = "SELECT * FROM result WHERE student_id =%s and quiz_id =%s"
            cursor.execute(score_query,(student_id,quiz_id))
            the_score  = cursor.fetchone()
        return the_score[2]

    def get_average_score(self,quiz_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            avg_query = "SELECT AVG(score)::numeric(10,2) FROM result where quiz_id = %s"
            cursor.execute(avg_query,[quiz_id])
            the_average  = cursor.fetchone()
        return the_average[0]
        

    def quiz_done_before(self,student_id,quiz_id): #check whether the quiz is done before 
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            check_query = "SELECT EXISTS (select true from result where student_id=%s and quiz_id =%s)"
            cursor.execute(check_query,(student_id,quiz_id))
            boolean = cursor.fetchone()
        return boolean[0]
        
    def get_scores_with_students(self,quiz_id): # get scores of students with their name ,surname ,id
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            scores_query = "SELECT quiz_id, score, student_name, student_surname, student.student_id FROM student INNER JOIN result ON student.student_id = result.student_id WHERE quiz_id = %s order by score desc"
            cursor.execute(scores_query,[quiz_id])
            the_scores  = cursor.fetchall()
        return the_scores







