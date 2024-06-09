from app import app, db
from app.models import User, Player, Item, Achievement, Inventory, Record

if __name__ == '__main__':
    app.run(debug=True)