
class Student:
    def __init__(self, id, name, surname, email, password):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

class Teacher:
    def __init__(self, id, name, surname, email, password):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

class Class:
    def __init__(self, name, CRN, teacher_id):
        self.name = name
        self.CRN = CRN
        self.teacher_id = teacher_id
class Quiz:
    def __init__(self, id, title, time, class_id):
        questions = {}
        self.id = id
        self.title = title
        self.time = time
        self.class_id = class_id

class Question:
    def __init__(self,quest_id,quiz_id,form_question,form_A,form_B,form_C,form_D,correct):
        self.quest_id = quest_id
        self.quiz_id = quiz_id
        self.form_question = form_question
        self.form_A = form_A
        self.form_B = form_B
        self.form_C = form_C
        self.form_D = form_D
        self.correct = correct

class Result:
    def __init__(self, student_id, quiz_id, score):
        self.student_id = student_id
        self.quiz_id = quiz_id
        self.score = score
