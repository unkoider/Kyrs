from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import User, Player, Item, Achievement, Inventory, Record
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import (AdminUserForm, AdminPlayerForm, AdminItemForm, 
                       AdminAchievementForm, AdminInventoryForm, AdminRecordForm)

# Декоратор для проверки прав администратора
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return decorated_view

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game')
@login_required
def game():
    return render_template('game.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        player = Player(user_id=user.id, name=username, level=1, ads_disabled=False, donation=0)
        db.session.add(player)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    player = Player.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', player=player)

@app.route('/items')
def item_list():
    items = Item.query.all()
    return render_template('item_list.html', items=items)

@app.route('/analytics')
def analytics_report():
    records = Record.query.all()
    return render_template('analytics_report.html', records=records)

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    players = Player.query.all()
    items = Item.query.all()
    achievements = Achievement.query.all()
    inventories = Inventory.query.all()
    records = Record.query.all()
    return render_template('admin_dashboard.html', 
                           users=users, players=players, items=items, 
                           achievements=achievements, inventories=inventories, 
                           records=records)

# User management
@app.route('/admin/user/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user_view():
    form = AdminUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='New User')

@app.route('/admin/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user_view(id):
    user = User.query.get_or_404(id)
    form = AdminUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='Edit User', user=user)

@app.route('/admin/user/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user_view(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

# Player management
@app.route('/admin/player/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_player_view():
    form = AdminPlayerForm()
    if form.validate_on_submit():
        player = Player(user_id=form.user_id.data, name=form.name.data, 
                        level=form.level.data, ads_disabled=form.ads_disabled.data, 
                        donation=form.donation.data)
        db.session.add(player)
        db.session.commit()
        flash('Player created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='New Player')

@app.route('/admin/player/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_player_view(id):
    player = Player.query.get_or_404(id)
    form = AdminPlayerForm(obj=player)
    if form.validate_on_submit():
        player.user_id = form.user_id.data
        player.name = form.name.data
        player.level = form.level.data
        player.ads_disabled = form.ads_disabled.data
        player.donation = form.donation.data
        db.session.commit()
        flash('Player updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='Edit Player', player=player)

@app.route('/admin/player/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_player_view(id):
    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    flash('Player deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

# Item management
@app.route('/admin/item/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_item_view():
    form = AdminItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, description=form.description.data, 
                    price=form.price.data, purchasable=form.purchasable.data)
        db.session.add(item)
        db.session.commit()
        flash('Item created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='New Item')

@app.route('/admin/item/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_item_view(id):
    item = Item.query.get_or_404(id)
    form = AdminItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        item.purchasable = form.purchasable.data
        db.session.commit()
        flash('Item updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='Edit Item', item=item)

@app.route('/admin/item/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_item_view(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

# Achievement management
@app.route('/admin/achievement/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_achievement_view():
    form = AdminAchievementForm()
    if form.validate_on_submit():
        achievement = Achievement(name=form.name.data, description=form.description.data)
        db.session.add(achievement)
        db.session.commit()
        flash('Achievement created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='New Achievement')

@app.route('/admin/achievement/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_achievement_view(id):
    achievement = Achievement.query.get_or_404(id)
    form = AdminAchievementForm(obj=achievement)
    if form.validate_on_submit():
        achievement.name = form.name.data
        achievement.description = form.description.data
        db.session.commit()
        flash('Achievement updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='Edit Achievement', achievement=achievement)

@app.route('/admin/achievement/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_achievement_view(id):
    achievement = Achievement.query.get_or_404(id)
    db.session.delete(achievement)
    db.session.commit()
    flash('Achievement deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

# Inventory management
@app.route('/admin/inventory/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_inventory_view():
    form = AdminInventoryForm()
    if form.validate_on_submit():
        inventory = Inventory(player_id=form.player_id.data,
                              item_id=form.item_id.data,
                              quantity=form.quantity.data)
        db.session.add(inventory)
        db.session.commit()
        flash('Inventory created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='New Inventory')

@app.route('/admin/inventory/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_inventory_view(id):
    inventory = Inventory.query.get_or_404(id)
    form = AdminInventoryForm(obj=inventory)
    if form.validate_on_submit():
        inventory.player_id = form.player_id.data
        inventory.item_id = form.item_id.data
        inventory.quantity = form.quantity.data
        db.session.commit()
        flash('Inventory updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='Edit Inventory', inventory=inventory)

@app.route('/admin/inventory/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_inventory_view(id):
    inventory = Inventory.query.get_or_404(id)
    db.session.delete(inventory)
    db.session.commit()
    flash('Inventory deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

# Record management
@app.route('/admin/record/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_record_view():
    form = AdminRecordForm()
    if form.validate_on_submit():
        record = Record(player_id=form.player_id.data,
                        description=form.description.data)
        db.session.add(record)
        db.session.commit()
        flash('Record created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='New Record')

@app.route('/admin/record/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_record_view(id):
    record = Record.query.get_or_404(id)
    form = AdminRecordForm(obj=record)
    if form.validate_on_submit():
        record.player_id = form.player_id.data
        record.description = form.description.data
        db.session.commit()
        flash('Record updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', form=form, title='Edit Record', record=record)

@app.route('/admin/record/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_record_view(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('Record deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))