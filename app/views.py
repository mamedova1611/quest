from flask import render_template, request, redirect

from app import app, db
from app.ciphers.caesar_cipher import caesar
from app.ciphers.gamma_code import gamma
from app.ciphers.keys import key_single_permutation, matrix, key_vigenere, key_gamma, text_edit
from app.ciphers.cipher_magic_squares import magic_square
from app.ciphers.vigenere_cipher import vigenere
from app.models import User, Result, Students, ResultStudents, Teachers
from app.ciphers.permutation_cipher import single_permutation


# главная страница
@app.route('/')
def index():
    return render_template('index.html')


# правила квеста
@app.route('/regulations')
def regulations():
    return render_template('regulations.html')


# главная страница преподавателя
@app.route('/teacher', methods=['POST', 'GET'])
def index_teacher():
    if request.method == 'POST':
        if request.form['button'] == "Просмотреть результаты":
            return redirect('/result')
        if request.form['button'] == "Зарегистрировать студентов":
            return redirect('/registration_students')
    else:
        return render_template('teacher.html')


# результаты для препода
@app.route('/result')
def result():
    students = db.session.query(Students).all()
    results = db.session.query(ResultStudents).all()
    return render_template('result.html', users=students, results=results)


# регистрация студентов
@app.route('/registration_students', methods=['POST', 'GET'])
def registration_students():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if name == text_edit(name):
            if db.session.query(Students).filter_by(name=name).first():
                return render_template('registration_students.html',
                                       error='Такой пользователь уже был зарегистрирован.')
            else:
                student = Students(name=name, password=password)
                db.session.add(student)
                db.session.commit()
                result = ResultStudents(id_stud=student.id)
                db.session.add(result)
                db.session.commit()
                return render_template('registration_students.html',
                                       error='Студент зарегистрирован.')
        else:
            return render_template('registration_students.html',
                                   error='Ваш логин должен содержать только буквы русского алфавита без пробелов и '
                                         'друих символов')
    else:
        return render_template('registration_students.html')


# авторизация
@app.route('/authorization', methods=['POST', 'GET'])
def authorization():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if db.session.query(Teachers).filter_by(name=name, password=password).first():
            return redirect('/teacher')
        if db.session.query(Students).filter_by(name=name, password=password).first():
            student = db.session.query(Students).filter_by(name=name).first()
            result = db.session.query(ResultStudents).filter_by(id_stud=student.id).first()
            global NAME
            NAME = name
            global stud
            stud = True
            global KEY
            KEY = key_single_permutation(NAME)
            global MATRIX
            MATRIX = matrix()
            global KEY_VIGENERE
            KEY_VIGENERE = key_vigenere()
            global KEY_GAMMA
            KEY_GAMMA = key_gamma(NAME)
            return redirect('/1')
        else:
            return 'Такой пользователь не зарегестрирован, обратитесь к преподавателю для регистрации'
    else:
        return render_template('authorization.html')


# регистрация
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        group = request.form['group']
        if name == text_edit(name):
            if db.session.query(User).filter_by(name=name).first():
                return render_template('registration.html',
                                       error='Такой пользователь уже был зарегистрирован.')
            else:
                user = User(name=name, group=group)
                db.session.add(user)
                db.session.commit()
                result = Result(id_user=user.id)
                db.session.add(result)
                db.session.commit()
                global NAME
                NAME = name
                global stud
                stud = False
                global KEY
                KEY = key_single_permutation(NAME)
                global MATRIX
                MATRIX = matrix()
                global KEY_VIGENERE
                KEY_VIGENERE = key_vigenere()
                global KEY_GAMMA
                KEY_GAMMA = key_gamma(NAME)
                return redirect('/1')
        else:
            return render_template('registration.html',
                                   error='Ваш логин должен содержать только буквы русского алфавита без пробелов и '
                                         'друих символов')
    else:
        return render_template('registration.html')


# первое задание-шифр одинарной перестановки
@app.route('/1', methods=['POST', 'GET'])
def cipher_1():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == text_edit(answer):
            if stud is True:
                student = db.session.query(Students).filter_by(name=NAME).first()
                result_student = db.session.query(ResultStudents).filter_by(id_stud=student.id).first()
                if answer == single_permutation(NAME, KEY):
                    result_student.permutation_cipher = 'ключ - %s |\n ответ - %s |\n решено %s' % (KEY, answer, 'верно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/2')
                elif answer != single_permutation(NAME, KEY) and answer != '':
                    result_student.permutation_cipher = 'ключ - %s |\n ответ - %s |\n решено %s' % (KEY, answer, 'неверно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/2')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result_student.permutation_cipher = 'пропущенно'
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/2')
            else:
                user = db.session.query(User).filter_by(name=NAME).first()
                result = db.session.query(Result).filter_by(id_user=user.id).first()
                if answer == single_permutation(NAME, KEY):
                    result.permutation_cipher = 'верно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/2')
                elif answer != single_permutation(NAME, KEY) and answer != '':
                    result.permutation_cipher = 'неверно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/2')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result.permutation_cipher = 'пропущенно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/2')
        else:
            return render_template('permutation_cipher.html',
                                   error='Ваш ответ должен содержать только буквы русского алфавита без пробелов и '
                                         'друих символов')
    else:
        return render_template('permutation_cipher.html', key=KEY)


@app.route('/2', methods=['POST', 'GET'])
def cipher_2():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == text_edit(answer):
            if stud is True:
                student = db.session.query(Students).filter_by(name=NAME).first()
                result_student = db.session.query(ResultStudents).filter_by(id_stud=student.id).first()
                if answer == magic_square(NAME, MATRIX):
                    result_student.cipher_magic_squares = 'ключ - %s | ответ - %s | решено %s' % (
                        MATRIX, answer, 'верно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/3')
                elif answer != magic_square(NAME, MATRIX) and answer != '':
                    result_student.cipher_magic_squares = 'ключ - %s | ответ - %s | решено %s' % (
                        MATRIX, answer, 'неверно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/3')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result_student.cipher_magic_squares = 'пропущенно'
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/3')
            else:
                user = db.session.query(User).filter_by(name=NAME).first()
                result = db.session.query(Result).filter_by(id_user=user.id).first()
                if answer == magic_square(NAME, MATRIX):
                    result.cipher_magic_squares = 'верно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/3')
                elif answer != magic_square(NAME, MATRIX) and answer != '':
                    result.cipher_magic_squares = 'неверно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/3')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result.cipher_magic_squares = 'пропущенно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/3')
        else:
            return render_template('cipher_magic_squares.html',
                                   error='Ваш ответ должен содержать только буквы русского алфавита без пробелов и '
                                         'друих символов')
    else:
        return render_template('cipher_magic_squares.html', key=MATRIX)


@app.route('/3', methods=['POST', 'GET'])
def cipher_3():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == text_edit(answer):
            if stud is True:
                student = db.session.query(Students).filter_by(name=NAME).first()
                result_student = db.session.query(ResultStudents).filter_by(id_stud=student.id).first()
                if answer == caesar(NAME.upper()):
                    result_student.caesar_cipher = 'ответ - %s | решено %s' % (answer, 'верно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/4')
                elif answer != caesar(NAME.upper()) and answer != '':
                    result_student.caesar_cipher = 'ответ - %s | решено %s' % (answer, 'неверно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/4')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result_student.caesar_cipher = 'пропущенно'
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/4')
            else:
                user = db.session.query(User).filter_by(name=NAME).first()
                result = db.session.query(Result).filter_by(id_user=user.id).first()
                if answer == caesar(NAME.upper()):
                    result.caesar_cipher = 'верно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/4')
                elif answer != caesar(NAME.upper()) and answer != '':
                    result.caesar_cipher = 'неверно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/4')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result.caesar_cipher = 'пропущенно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/4')
        else:
            return render_template('caesar_cipher.html',
                                   error='Ваш ответ должен содержать только буквы русского алфавита без пробелов и '
                                         'друих символов')
    else:
        return render_template('caesar_cipher.html')


@app.route('/4', methods=['POST', 'GET'])
def cipher_4():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == text_edit(answer):
            if stud is True:
                student = db.session.query(Students).filter_by(name=NAME).first()
                result_student = db.session.query(ResultStudents).filter_by(id_stud=student.id).first()
                if answer == vigenere(NAME, KEY_VIGENERE):
                    result_student.vigenere_cipher = 'ключ - %s | ответ - %s | решено %s' % (
                        KEY_VIGENERE, answer, 'верно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/5')
                elif answer != vigenere(NAME, KEY_VIGENERE) and answer != '':
                    result_student.vigenere_cipher = 'ключ - %s | ответ - %s | решено %s' % (
                        KEY_VIGENERE, answer, 'неверно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/5')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result_student.vigenere_cipher = 'пропущенно'
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/5')
            else:
                user = db.session.query(User).filter_by(name=NAME).first()
                result = db.session.query(Result).filter_by(id_user=user.id).first()
                if answer == vigenere(NAME, KEY_VIGENERE):
                    result.vigenere_cipher = 'верно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/5')
                elif answer != vigenere(NAME, KEY_VIGENERE) and answer != '':
                    result.vigenere_cipher = 'неверно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/5')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result.vigenere_cipher = 'пропущенно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/5')
        else:
            return render_template('vigenere_cipher.html',
                                   error='Ваш ответ должен содержать только буквы русского алфавита без пробелов и '
                                         'друих символов')
    else:
        return render_template('vigenere_cipher.html')


@app.route('/5', methods=['POST', 'GET'])
def cipher_5():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == text_edit(answer):
            if stud is True:
                student = db.session.query(Students).filter_by(name=NAME).first()
                result_student = db.session.query(ResultStudents).filter_by(id_stud=student.id).first()
                if answer == gamma(NAME, KEY_GAMMA):
                    result_student.gamma_code = 'ключ - %s | ответ - %s | решено %s' % (KEY_GAMMA, answer, 'неверно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/end')
                elif answer != gamma(NAME, KEY_GAMMA) and answer != '':
                    result_student.gamma_code = 'ключ - %s | ответ - %s | решено %s' % (KEY_GAMMA, answer, 'неверно')
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/end')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result_student.gamma_code = 'пропущенно'
                    db.session.add(result_student)
                    db.session.commit()
                    return redirect('/end')
            else:
                user = db.session.query(User).filter_by(name=NAME).first()
                result = db.session.query(Result).filter_by(id_user=user.id).first()
                if answer == gamma(NAME, KEY_GAMMA):
                    result.gamma_code = 'верно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/end')
                elif answer != gamma(NAME, KEY_GAMMA) and answer != '':
                    result.gamma_code = 'неверно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/end')
                elif answer == '' or request.form['skip'] == "Пропустить":
                    result.gamma_code = 'пропущенно'
                    db.session.add(result)
                    db.session.commit()
                    return redirect('/end')
        else:
            return render_template('gamma_code.html',
                                   error='Ваш ответ должен содержать только буквы русского алфавита без пробелов и '
                                         'друих символов')
    else:
        return render_template('gamma_code.html')


@app.route('/end')
def victory():
    if stud is True:
        user = db.session.query(Students).filter_by(name=NAME).first()
        result = db.session.query(ResultStudents).filter_by(id_stud=user.id).first()
    else:
        user = db.session.query(User).filter_by(name=NAME).first()
        result = db.session.query(Result).filter_by(id_user=user.id).first()
    return render_template('victory.html', name=NAME, permutation_cipher=result.permutation_cipher,
                           cipher_magic_squares=result.cipher_magic_squares, caesar_cipher=result.caesar_cipher,
                           vigenere_cipher=result.vigenere_cipher, gamma_code=result.gamma_code)
