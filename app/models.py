from app import db


# бд зарегистрированных пользователей
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    group = db.Column(db.String, nullable=False)


# бд для результатов зарег пользователей

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    permutation_cipher = db.Column(db.String)
    cipher_magic_squares = db.Column(db.String)
    caesar_cipher = db.Column(db.String)
    vigenere_cipher = db.Column(db.String)
    gamma_code = db.Column(db.String)

    user = db.relationship('User')


class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class ResultStudents(db.Model):
    __tablename__ = 'result_students'
    id = db.Column(db.Integer, primary_key=True)
    id_stud = db.Column(db.Integer, db.ForeignKey('students.id'))
    permutation_cipher = db.Column(db.String)
    cipher_magic_squares = db.Column(db.String)
    caesar_cipher = db.Column(db.String)
    vigenere_cipher = db.Column(db.String)
    gamma_code = db.Column(db.String)

    students = db.relationship('Students')


class Teachers(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)

