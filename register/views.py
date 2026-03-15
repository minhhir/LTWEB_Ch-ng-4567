import sqlite3
import os
from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from . import register_bp


# Hàm kết nối DB (Copy sang đây để module này dùng được)
def get_db_connection():
    db_path = os.path.join(current_app.root_path, 'data', 'website.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# Route bây giờ là /register/ (do prefix đã set là /register)
@register_bp.route('/', methods=['GET', 'POST'])
def create_account():
    username_error = ""
    email_error = ""
    password_error = ""

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # Validate
        is_valid = True
        if not username:
            username_error = "Username is required."
            is_valid = False
        if not email:
            email_error = "Email is required."
            is_valid = False
        if not password:
            password_error = "Password is required."
            is_valid = False

        if is_valid:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Tối ưu 2: Kiểm tra trùng cả username HOẶC email
                user = cursor.execute(
                    'SELECT id FROM user WHERE name = ? OR email = ?',
                    (username, email)
                ).fetchone()

                if user:
                    # Gán chung một lỗi hoặc tách riêng tùy ý bạn
                    username_error = "Username hoặc Email này đã tồn tại trong hệ thống."
                else:
                    # Lưu vào DB
                    hashed_password = generate_password_hash(password)
                    cursor.execute(
                        'INSERT INTO user (name, email, password) VALUES (?, ?, ?)',
                        (username, email, hashed_password)
                    )
                    conn.commit()

                    flash('Đăng ký thành công! Hãy đăng nhập.', 'success')
                    return redirect(url_for('auth.login'))

            except sqlite3.Error as e:
                flash(f'Lỗi Database: {e}', 'danger')
            finally:
                # Tối ưu 1: Luôn đóng kết nối ở đây
                if 'conn' in locals():
                    conn.close()
    return render_template('register.html',
                           username_error=username_error,
                           email_error=email_error,
                           password_error=password_error)