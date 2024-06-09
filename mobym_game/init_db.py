from app import app, db
from app.models import User, Player, Achievement, Item, Inventory, Record
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    
    hashed_password1 = generate_password_hash('password')
    hashed_password2 = generate_password_hash('password')
    hashed_password_admin = generate_password_hash('admin')

    user1 = User(username='user1', password=hashed_password1, is_admin=False)
    user2 = User(username='user2', password=hashed_password2, is_admin=False)
    admin = User(username='admin', password=hashed_password_admin, is_admin=True)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(admin)
    db.session.commit()

    player1 = Player(user_id=1, name='Player1', level=1, ads_disabled=False, donation=50.00)
    player2 = Player(user_id=2, name='Player2', level=2, ads_disabled=True, donation=100.00)
    db.session.add(player1)
    db.session.add(player2)
    db.session.commit()

    achievement1 = Achievement(player_id=1, name='First Run', progress=100)
    achievement2 = Achievement(player_id=1, name='Collector', progress=50)
    achievement3 = Achievement(player_id=2, name='First Run', progress=100)
    achievement4 = Achievement(player_id=2, name='Speedster', progress=75)
    db.session.add(achievement1)
    db.session.add(achievement2)
    db.session.add(achievement3)
    db.session.add(achievement4)
    db.session.commit()

    item1 = Item(name='Double Jump', description='Allows player to jump twice in a row', price=10.00, purchasable=True)
    item2 = Item(name='Magnet', description='Attracts nearby coins', price=15.00, purchasable=True)
    item3 = Item(name='Invincibility', description='Temporarily makes the player invincible', price=20.00, purchasable=False)
    item4 = Item(name='Speed Boost', description='Increases player speed for a short period', price=12.00, purchasable=True)
    db.session.add(item1)
    db.session.add(item2)
    db.session.add(item3)
    db.session.add(item4)
    db.session.commit()

    inventory1 = Inventory(player_id=1, item_id=1, quantity=2, pregame=True)
    inventory2 = Inventory(player_id=1, item_id=2, quantity=1, pregame=False)
    inventory3 = Inventory(player_id=2, item_id=3, quantity=1, pregame=True)
    db.session.add(inventory1)
    db.session.add(inventory2)
    db.session.add(inventory3)
    db.session.commit()
