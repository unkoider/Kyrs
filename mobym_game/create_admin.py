from app import db, app
from app.models import User

def create_admin(username, password):
    with app.app_context():
        admin = User(username=username, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == '__main__':
    username = 'admin'  # Задайте имя пользователя администратора
    password = 'admin_password'  # Задайте пароль администратора
    create_admin(username, password)