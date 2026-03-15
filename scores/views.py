import csv
import os
from flask import render_template, request, current_app, session, redirect, url_for, flash
from . import scores_bp


@scores_bp.route('/search', methods=['GET', 'POST'])
def search_scores():
    # Kiểm tra đăng nhập
    if 'username' not in session:
        flash('Bạn cần đăng nhập để tra cứu điểm.', 'warning')
        return redirect(url_for('auth.login'))

    results = []
    keyword = ''
    gender_filter = ''  # Biến lưu giới tính được chọn

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').lower().strip()
        gender_filter = request.form.get('gender', '')  # Lấy giá trị từ drop-down

        # Đường dẫn đến file csv
        csv_path = os.path.join(current_app.root_path, 'data', 'gradedata.csv')

        try:
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # 1. Kiểm tra Tên (keyword nằm trong full_name)
                    full_name = (row['fname'] + ' ' + row['lname']).lower()
                    match_name = keyword in full_name

                    # 2. Kiểm tra Giới tính (Nếu chọn 'all' hoặc rỗng thì luôn đúng, ngược lại phải khớp)
                    match_gender = True
                    if gender_filter and gender_filter != 'all':
                        if row['gender'].lower() != gender_filter:
                            match_gender = False

                    # 3. Kết hợp cả 2 điều kiện (AND)
                    if match_name and match_gender:
                        results.append(row)

        except FileNotFoundError:
            flash('Không tìm thấy file dữ liệu điểm!', 'danger')

    # Trả về cả keyword và gender_filter để giữ trạng thái form sau khi submit
    return render_template('scores.html', results=results, keyword=keyword, gender_filter=gender_filter)