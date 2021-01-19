from flask import Flask, current_app, redirect, render_template, json, request
from views import *
import views
from flask_login import LoginManager
import os

lm = LoginManager() ##

@lm.user_loader ##
def load_user(user_id):
    return get_user(user_id)

def create_app():
    app = Flask(__name__) # create app
    app.config.from_object("settings")

    app.secret_key = 'hello' # ??

    app.add_url_rule("/", view_func=views.main)
    app.add_url_rule("/student_page", view_func=views.student_page, methods=["GET", "POST"]) # for student login
    app.add_url_rule("/teacher_page", view_func=views.teacher_page, methods=["GET", "POST"]) # for teacher login
    app.add_url_rule("/signUp", view_func=views.signUp,methods=["GET", "POST"])
    app.add_url_rule("/successful", view_func=views.successful)
    
    app.add_url_rule("/teacher_main_page", view_func=views.teacher_main_page, methods=["GET", "POST"])
    app.add_url_rule("/update_teacher", view_func=views.update_teacher, methods=["GET", "POST"])
    app.add_url_rule("/delete_teacher", view_func=views.delete_teacher, methods=["GET", "POST"])
    app.add_url_rule("/create_class", view_func=views.create_class,methods=["GET", "POST"])
    app.add_url_rule("/delete_class/<int:class_id>", view_func=views.delete_class, methods=["GET", "POST"])
    app.add_url_rule("/update_class/<int:class_id>", view_func=views.update_class, methods=["GET", "POST"])
    app.add_url_rule("/main_quizzes/<int:class_id>", view_func=views.main_quizzes, methods=["GET", "POST"])
    app.add_url_rule("/create_quiz/<int:class_id>", view_func=views.create_quiz, methods=["GET", "POST"])
    app.add_url_rule("/delete_quiz/<int:quiz_id>", view_func=views.delete_quiz, methods=["GET", "POST"])
    app.add_url_rule("/update_quiz/<int:quiz_id>", view_func=views.update_quiz, methods=["GET", "POST"])
    app.add_url_rule("/questions/<int:quiz_id>", view_func=views.questions, methods=["GET", "POST"])
    app.add_url_rule("/delete_question/<int:question_id>/<int:quiz_id>", view_func=views.delete_question, methods=["GET", "POST"])
    app.add_url_rule("/update_question/<int:question_id>/<int:quiz_id>", view_func=views.update_question, methods=["GET", "POST"])
    app.add_url_rule("/results/<int:quiz_id>", view_func=views.results, methods=["GET", "POST"])

    app.add_url_rule("/student_main_page", view_func=views.student_main_page, methods=["GET", "POST"])
    app.add_url_rule("/update_student", view_func=views.update_student, methods=["GET", "POST"])
    app.add_url_rule("/delete_student", view_func=views.delete_student, methods=["GET", "POST"])
    app.add_url_rule("/show_quizzes_to_student/<int:class_id>", view_func=views.show_quizzes_to_student, methods=["GET", "POST"])
    app.add_url_rule("/exam_page/<int:quiz_id>", view_func=views.exam_page, methods=["GET", "POST"])
    app.add_url_rule("/result/<int:quiz_id>", view_func=views.result, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout)

    lm.init_app(app) ##
    lm.login_view = "student_page" ##

    db = Database(os.environ.get("DATABASE_URL"))
    
    app.config["db"] = db
    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)