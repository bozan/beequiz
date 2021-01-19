CREATE TABLE TEACHER (
    teacher_id INTEGER PRIMARY KEY, 
    teacher_name VARCHAR(20) NOT NULL,
    teacher_surname VARCHAR(20) NOT NULL,
    teacher_email VARCHAR(30) UNIQUE NOT NULL,
    teacher_password VARCHAR(400) NOT NULL
);

CREATE TABLE STUDENT (
    student_id INTEGER PRIMARY KEY,
    student_name VARCHAR(20) NOT NULL,
    student_surname VARCHAR(20) NOT NULL,
    student_email VARCHAR(30) UNIQUE NOT NULL,
    student_password VARCHAR(400) NOT NULL
);

CREATE TABLE CLASS (
    class_code INTEGER PRIMARY KEY,
    teacher_id INTEGER NOT NULL,
    class_name VARCHAR(50) UNIQUE NOT NULL,
FOREIGN KEY (teacher_id) REFERENCES TEACHER(teacher_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE QUIZ (
    quiz_id SERIAL PRIMARY KEY,
    quiz_title VARCHAR(100) NOT NULL,
    quiz_time INTERVAL,
    class_code INTEGER NOT NULL,
    FOREIGN KEY (class_code) REFERENCES CLASS(class_code) ON UPDATE CASCADE ON DELETE CASCADE
);

 CREATE TABLE QUESTION (
	question_id SERIAL PRIMARY KEY,
	question varchar(400) NOT NULL,
	A varchar(300) NOT NULL,
	B varchar(300) NOT NULL,
	C varchar(300) NOT NULL,
	D varchar(300) NOT NULL,
	correct varchar(2) NOT NULL,
	quiz_id INTEGER NOT NULL,
	FOREIGN KEY (quiz_id) REFERENCES QUIZ(quiz_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE RESULT (
    student_id INTEGER ,
    quiz_id INTEGER,
    score FLOAT,
    PRIMARY KEY (student_id,quiz_id),
    FOREIGN KEY (quiz_id) REFERENCES QUIZ(quiz_id) ON UPDATE CASCADE ON DELETE CASCADE);