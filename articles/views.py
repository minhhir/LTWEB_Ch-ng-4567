from flask import render_template, abort,session, redirect, url_for, flash
from . import articles_bp
# Dữ liệu mẫu hard-code
ARTICLES = [
    {'id': 1, 'title': 'Giới thiệu Flask Blueprint', 'content': 'Blueprint giúp chia nhỏ ứng dụng thành mô-đun.'},
    {'id': 2, 'title': 'Tổ chức dự án Flask', 'content': 'Sắp xếp theo gói (package) và template kế thừa.'},
    {'id': 3, 'title': 'Testing với Blueprint', 'content': 'Có thể cô lập và kiểm thử từng phần.'},
]
@articles_bp.route('/')
def article_list():
    # Bảo vệ route: Chưa login thì đá về login
    if 'username' not in session:
        flash('Bạn cần đăng nhập để xem bài viết.', 'warning')
        return redirect(url_for('auth.login'))
    # Trả về danh sách bài viết
    return render_template('articles.html', articles=ARTICLES)
@articles_bp.route('/<int:article_id>')
def article_detail(article_id):
    # Tìm bài theo id, nếu không có thì 404
    article = next((a for a in ARTICLES if a['id'] == article_id), None)
    if not article:
        abort(404)
    return render_template('articles.html', article=article)