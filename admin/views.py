import sqlite3
import os
from flask import render_template, request, redirect, url_for, flash, session, current_app
from . import admin_bp


def get_db_connection():
    db_path = os.path.join(current_app.root_path, 'data', 'website.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'Administrator':
            flash('Bạn không có quyền truy cập trang này.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/storages')
@admin_required
def index():
    conn = get_db_connection()
    storages = conn.execute('SELECT * FROM storages').fetchall()
    conn.close()
    return render_template('admin/index.html', storages=storages)

@admin_bp.route('/storages/add', methods=['GET', 'POST'])
@admin_required
def add():
    if request.method == 'POST':
        product = request.form['product']
        brand   = request.form['brand']
        rating  = request.form['rating']
        model   = request.form['model']
        picture = request.form['picture']
        price   = request.form['price']
        RAM     = request.form['RAM']
        details = request.form['details']

        conn = get_db_connection()
        conn.execute(
            '''INSERT INTO storages
               (product, brand, rating, model, picture, price, RAM, details)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (product, brand, rating, model, picture, price, RAM, details)
        )
        conn.commit()
        conn.close()

        flash('✅ Thêm sản phẩm thành công!', 'success')
        return redirect(url_for('admin.index'))

    return render_template('admin/add.html')

@admin_bp.route('/storages/edit/<int:storage_id>', methods=['GET', 'POST'])
@admin_required
def edit(storage_id):
    conn = get_db_connection()
    storage = conn.execute(
        'SELECT * FROM storages WHERE id = ?', (storage_id,)
    ).fetchone()
    conn.close()

    if not storage:
        flash('Không tìm thấy sản phẩm.', 'danger')
        return redirect(url_for('admin.index'))

    if request.method == 'POST':
        product = request.form['product']
        brand   = request.form['brand']
        rating  = request.form['rating']
        model   = request.form['model']
        picture = request.form['picture']
        price   = request.form['price']
        RAM     = request.form['RAM']
        details = request.form['details']

        conn = get_db_connection()
        conn.execute(
            '''UPDATE storages
               SET product=?, brand=?, rating=?, model=?,
                   picture=?, price=?, RAM=?, details=?
               WHERE id=?''',
            (product, brand, rating, model, picture, price, RAM, details, storage_id)
        )
        conn.commit()
        conn.close()

        flash('✅ Cập nhật sản phẩm thành công!', 'success')
        return redirect(url_for('admin.index'))

    return render_template('admin/edit.html', storage=storage)

@admin_bp.route('/orders')
@admin_required
def orders():
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT o.*, COUNT(od.product_id) as item_count
        FROM "order" o
        LEFT JOIN order_details od ON od.order_id = o.id
        GROUP BY o.id
        ORDER BY o.purchase_date DESC
    ''').fetchall()
    conn.close()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/orders/<int:order_id>', methods=['GET', 'POST'])
@admin_required
def order_detail(order_id):
    conn = get_db_connection()

    if request.method == 'POST':
        new_status = request.form['status']
        ship_date  = request.form.get('ship_date', '')
        conn.execute(
            'UPDATE "order" SET status=?, ship_date=? WHERE id=?',
            (new_status, ship_date or None, order_id)
        )
        conn.commit()
        flash(f' Đã cập nhật trạng thái đơn hàng #{order_id}', 'success')

    order = conn.execute(
        'SELECT * FROM "order" WHERE id=?', (order_id,)
    ).fetchone()

    rows = conn.execute(
        '''SELECT od.product_id, od.price, od.quantity,
                  s.model, s.brand, s.picture
           FROM order_details od
           LEFT JOIN storages s ON s.id = od.product_id
           WHERE od.order_id = ?''',
        (order_id,)
    ).fetchall()
    conn.close()

    # Tính subtotal trong Python
    order_details = []
    for row in rows:
        item = dict(row)
        try:
            price = float(str(item['price']).replace(',', ''))
        except (ValueError, TypeError):
            price = 0.0
        item['subtotal'] = price * item['quantity']
        order_details.append(item)

    return render_template('admin/order_detail.html',
                           order=order,
                           order_details=order_details)

@admin_bp.route('/storages/delete/<int:storage_id>', methods=['POST'])
@admin_required
def delete(storage_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM storages WHERE id = ?', (storage_id,))
    conn.commit()
    conn.close()

    flash('🗑 Đã xóa sản phẩm.', 'warning')
    return redirect(url_for('admin.index'))