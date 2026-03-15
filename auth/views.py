from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import check_password_hash
from . import auth_bp  # ← BẮT BUỘC PHẢI CÓ


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('auth.profile'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        import sqlite3, os
        db_path = os.path.join(current_app.root_path, 'data', 'website.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        user = conn.execute(
            'SELECT * FROM user WHERE name = ?', (username,)
        ).fetchone()
        conn.close()

        if user:
            pw = user['password']
            if (pw.startswith('scrypt:') and check_password_hash(pw, password)) \
               or pw == password:
                session['username'] = user['name']
                session['role'] = 'User'
                flash('Đăng nhập thành công!', 'success')
                return redirect(url_for('index'))

        # Fallback hardcode admin/123
        if username == 'admin' and password == '123':
            session['username'] = 'admin'
            session['role'] = 'Administrator'
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))

        flash('Sai tên đăng nhập hoặc mật khẩu.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất thành công.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Vui lòng đăng nhập để xem thông tin.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('profile.html', user=session)