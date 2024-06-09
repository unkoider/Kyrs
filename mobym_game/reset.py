from app import db, app
from app.models import User

def reset_passwords():
    with app.app_context():
        users = User.query.all()
        for user in users:
            user.set_password('new_default_password')
        db.session.commit()
        print("Passwords reset")

if __name__ == '__main__':
    reset_passwords()
