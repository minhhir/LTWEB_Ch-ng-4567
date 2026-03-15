import sqlite3
import os
from flask import render_template, request, session, current_app, flash, redirect, url_for
from . import cart_bp


def get_db_connection():
    db_path = os.path.join(current_app.root_path, 'data', 'website.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form.get('quantity', 1))

    conn = get_db_connection()
    product = conn.execute(
        'SELECT model, price, picture, details FROM storages WHERE id = ?',
        (product_id,)
    ).fetchone()
    conn.close()

    if not product:
        flash('Không tìm thấy sản phẩm!', 'danger')
        return redirect(url_for('products.search_products'))

    product_dict = {
        'id':       product_id,
        'name':     product['model'],
        'price':    product['price'],
        'picture':  product['picture'],
        'details':  product['details'],
        'quantity': quantity
    }

    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += quantity
            break
    else:
        cart.append(product_dict)

    session['cart'] = cart
    session.modified = True

    flash(f'Đã thêm "{product_dict["name"]}" vào giỏ! '
          f'(Giỏ đang có {len(cart)} sản phẩm)', 'success')
    return redirect(url_for('products.search_products'))

@cart_bp.route('/')
def view_cart():
    cart = session.get('cart', [])
    return render_template('cart.html', carts=cart)

@cart_bp.route('/update', methods=['POST'])
def update_cart():
    cart = session.get('cart', [])
    new_cart = []

    for product in cart:
        product_id = str(product['id'])

        # Nếu checkbox delete được tick → bỏ qua (xóa sản phẩm)
        if f'delete-{product_id}' in request.form:
            continue

        # Nếu có trường quantity trong form → cập nhật
        if f'quantity-{product_id}' in request.form:
            quantity = int(request.form[f'quantity-{product_id}'])
            # Nếu quantity = 0 → cũng xóa
            if quantity <= 0:
                continue
            product['quantity'] = quantity

        new_cart.append(product)

    session['cart'] = new_cart
    session.modified = True

    flash(f'Đã cập nhật giỏ hàng! ({len(new_cart)} sản phẩm)', 'info')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    product_id = request.form['product_id']
    cart = session.get('cart', [])
    session['cart'] = [i for i in cart if i['id'] != product_id]
    session.modified = True
    flash('🗑 Đã xóa sản phẩm khỏi giỏ hàng.', 'info')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    flash('🗑 Đã xóa toàn bộ giỏ hàng.', 'warning')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/proceed', methods=['POST'])
def proceed_cart():
    if 'username' not in session:
        flash('Vui lòng đăng nhập để đặt hàng.', 'warning')
        return redirect(url_for('auth.login'))

    cart = session.get('cart', [])
    if not cart:
        flash('Giỏ hàng trống, không thể đặt hàng!', 'danger')
        return redirect(url_for('cart.view_cart'))

    try:
        conn = get_db_connection()
        # Lấy user_id từ bảng user theo username
        user = conn.execute(
            'SELECT id, email FROM user WHERE name = ?',
            (session['username'],)
        ).fetchone()
        user_id    = user['id']    if user else None
        user_email = user['email'] if user else session['username']
        #Tạo 1 đơn hàng trong bảng "order"
        cursor = conn.execute(
            '''INSERT INTO "order" (user_id, user_email, purchase_date, status)
               VALUES (?, ?, DATE('now'), 0)''',
            (user_id, user_email)
        )
        order_id = cursor.lastrowid  # Lấy ID đơn hàng vừa tạo
        # Lưu từng sản phẩm vào order_details
        for item in cart:
            # Làm sạch price: bỏ dấu phẩy → float
            price_clean = str(item['price']).replace(',', '')
            try:
                price = float(price_clean)
            except ValueError:
                price = 0.0

            conn.execute(
                '''INSERT INTO order_details
                   (order_id, product_id, price, quantity, purchase_date)
                   VALUES (?, ?, ?, ?, DATE('now'))''',
                (order_id, item['id'], price, item['quantity'])
            )
        conn.commit()
        conn.close()
        #Xóa giỏ, lưu order_id để hiển thị trang success
        session.pop('cart', None)
        session['last_order_id'] = order_id
        session.modified = True

        flash('🎉 Đặt hàng thành công!', 'success')
        return redirect(url_for('cart.order_success'))
    except Exception as e:
        flash(f'Lỗi khi tạo đơn hàng: {e}', 'danger')
        return redirect(url_for('cart.view_cart'))

@cart_bp.route('/success')
def order_success():
    order_id = session.pop('last_order_id', None)
    return render_template('order_success.html', order_id=order_id)

@cart_bp.route('/orders')
def orders():
    if 'username' not in session:
        flash('Vui lòng đăng nhập.', 'warning')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()

    # Lấy user_id từ username trong session
    user = conn.execute(
        'SELECT id FROM user WHERE name = ?',
        (session['username'],)
    ).fetchone()

    if not user:
        flash('Không tìm thấy thông tin người dùng.', 'danger')
        return redirect(url_for('index'))

    user_orders = conn.execute(
        'SELECT * FROM "order" WHERE user_id = ? ORDER BY purchase_date DESC',
        (user['id'],)
    ).fetchall()
    conn.close()
    return render_template('orders.html', orders=user_orders)

@cart_bp.route('/orders/<int:order_id>')
def order_detail(order_id):
    if 'username' not in session:
        flash('Vui lòng đăng nhập.', 'warning')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()

    user = conn.execute(
        'SELECT id FROM user WHERE name = ?',
        (session['username'],)
    ).fetchone()

    order = conn.execute(
        'SELECT * FROM "order" WHERE id = ? AND user_email = ?',
        (order_id, session['username'])
    ).fetchone()

    if not order:
        conn.close()
        flash('Không tìm thấy đơn hàng.', 'danger')
        return redirect(url_for('cart.orders'))

    rows = conn.execute(
        '''SELECT od.product_id, od.price, od.quantity,
                  s.model, s.brand, s.picture
           FROM order_details od
           LEFT JOIN storages s ON s.id = od.product_id
           WHERE od.order_id = ?''',
        (order_id,)
    ).fetchall()
    conn.close()

    order_details = []
    for row in rows:
        item = dict(row)  # Convert sang dict để thêm key mới
        try:
            price = float(str(item['price']).replace(',', ''))
        except (ValueError, TypeError):
            price = 0.0
        item['subtotal'] = price * item['quantity']
        order_details.append(item)

    return render_template('order_detail.html',
                           order=order,
                           order_details=order_details)