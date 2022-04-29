from app import db, app

if __name__ == "__main__":
    db.create_all()  # создание бд
    app.run(debug=True)  # запуск приложения
