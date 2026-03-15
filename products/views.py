import sqlite3
import os
from flask import render_template, request, current_app, session, redirect, url_for, flash
from . import products_bp

# Hàm kết nối Database
def get_db_connection():
    db_path = os.path.join(current_app.root_path, 'data', 'website.db')
    conn = sqlite3.connect(db_path)
    #truy cập cột bằng tên (row['model']) thay vì số (row[4])
    conn.row_factory = sqlite3.Row
    return conn

@products_bp.route('/', methods=['GET', 'POST'])
def search_products():
    if 'username' not in session:
        flash('Bạn cần đăng nhập để xem sản phẩm.', 'warning')
        return redirect(url_for('auth.login'))
    results = []
    keyword = request.args.get('q', '') or request.form.get('searchInput', '')
    keyword = keyword.strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if keyword:
            # Dấu ? sẽ được thay thế tự động bởi biến trong tuple, chống SQL Injection
            query = """
                    SELECT DISTINCT * FROM storages 
                    WHERE model LIKE ? 
                    OR brand LIKE ? 
                    OR details LIKE ?
                """
            search_param = f'%{keyword}%'
            cursor.execute(query, (search_param, search_param, search_param))
            results = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM storages LIMIT 20")
            results = cursor.fetchall()

        conn.close()

    except sqlite3.Error as e:
        flash(f'Lỗi kết nối CSDL: {e}', 'danger')

    return render_template('products.html', results=results, keyword=keyword)