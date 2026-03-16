# 🐸 My Flask App

Ứng dụng web thương mại điện tử xây dựng bằng **Flask** theo kiến trúc **Blueprint**, hỗ trợ quản lý sản phẩm, giỏ hàng, đơn hàng và phân quyền người dùng.

---

## 📋 Tính năng

### 👤 Người dùng (User)
- Đăng ký / Đăng nhập / Đăng xuất
- Xem và tìm kiếm sản phẩm (từ database SQLite)
- Thêm sản phẩm vào giỏ hàng (session)
- Cập nhật số lượng / xóa sản phẩm khỏi giỏ
- Đặt hàng → tạo đơn hàng lưu vào DB
- Xem danh sách & chi tiết đơn hàng của mình
- Tra cứu điểm sinh viên (từ CSV)
- Đọc bài viết

### 🔧 Quản trị viên (Admin)
- CRUD sản phẩm (Thêm / Sửa / Xóa)
- Xem tất cả đơn hàng của mọi người dùng
- Cập nhật trạng thái đơn hàng + ngày giao

---

## 🗂️ Cấu trúc project

```
Chuong4_project/
├── app.py                  # Factory function, đăng ký Blueprint
├── init_db.py              # Tạo bảng orders (chạy 1 lần)
├── .env                    # SECRET_KEY (không push lên GitHub)
├── .gitignore
│
├── auth/                   # Blueprint: /auth
│   ├── __init__.py
│   └── views.py            # login, logout, profile
│
├── articles/               # Blueprint: /articles
│   ├── __init__.py
│   └── views.py            # Danh sách & chi tiết bài viết
│
├── scores/                 # Blueprint: /scores
│   ├── __init__.py
│   └── views.py            # Tra cứu điểm từ CSV
│
├── products/               # Blueprint: /products
│   ├── __init__.py
│   └── views.py            # Tìm kiếm sản phẩm từ SQLite
│
├── register/               # Blueprint: /register
│   ├── __init__.py
│   └── views.py            # Đăng ký tài khoản
│
├── cart/                   # Blueprint: /cart
│   ├── __init__.py
│   └── views.py            # Giỏ hàng, đặt hàng, xem đơn
│
├── admin/                  # Blueprint: /admin
│   ├── __init__.py
│   └── views.py            # CRUD sản phẩm, quản lý đơn hàng
│
├── static/
│   ├── frogfaviconhehehe.png
│   └── styles_registration.css
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── articles.html
│   ├── products.html
│   ├── scores.html
│   ├── cart.html
│   ├── orders.html
│   ├── order_detail.html
│   ├── order_success.html
│   └── admin/
│       ├── index.html
│       ├── add.html
│       ├── edit.html
│       ├── orders.html
│       └── order_detail.html
│
└── data/                   # ← KHÔNG push lên GitHub
    └── website.db
```

---

## 🗃️ Database Schema

```sql
-- Sản phẩm
CREATE TABLE storages (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    product VARCHAR(100),
    brand   VARCHAR(200),
    rating  VARCHAR(10),
    model   VARCHAR(1000),
    picture VARCHAR(1000),
    price   VARCHAR(1000),
    RAM     VARCHAR(100),
    details VARCHAR(1000)
);

-- Người dùng
CREATE TABLE user (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     VARCHAR(150),
    email    VARCHAR(150),
    password VARCHAR(200)
);

-- Đơn hàng
CREATE TABLE "order" (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INT,
    user_email    VARCHAR(200),
    user_address  VARCHAR(200),
    user_mobile   INT,
    purchase_date DATE,
    ship_date     DATE,
    status        INT DEFAULT 0
);

-- Chi tiết đơn hàng
CREATE TABLE order_details (
    order_id      INT,
    product_id    INT,
    price         NUMERIC,
    quantity      INT,
    purchase_date DATE
);

-- Lịch sử đặt hàng (legacy)
CREATE TABLE orders (
    user_email    VARCHAR(200),
    product_id    INT,
    purchase_date DATE
);
```

**Trạng thái đơn hàng:**

| Giá trị | Ý nghĩa |
|---------|---------|
| `0` | ⏳ Chờ xử lý |
| `1` | 🚚 Đang giao |
| `2` | ✅ Đã giao |
| `3` | ❌ Đã hủy |

---

## 🚀 Cài đặt & Chạy

### 1. Clone repo
```bash
git clone https://github.com/minhhir/LTWEB_Ch-ng-4567
```

### 2. Tạo virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

### 3. Cài dependencies
```bash
pip install flask werkzeug python-dotenv
```

### 4. Tạo file `.env`
```
SECRET_KEY=your-secret-key-here
```

### 5. Chuẩn bị database

Đặt file `website.db` vào thư mục `data/`, sau đó chạy:
```bash
python init_db.py
```

### 6. Chạy ứng dụng
```bash
python app.py
```

Mở trình duyệt tại: **http://127.0.0.1:5050**

---

## 🔑 Tài khoản mặc định

| Tài khoản | Mật khẩu | Quyền |
|-----------|----------|-------|
| `admin` | `123` | Administrator |
| `abc` | `123456789` | User |

> ⚠️ Đây là tài khoản demo. Thay đổi trước khi deploy thực tế.

---

## 📦 Dependencies

| Thư viện | Mục đích |
|----------|----------|
| `Flask` | Web framework |
| `werkzeug` | Password hashing |
| `python-dotenv` | Quản lý biến môi trường |
| `sqlite3` | Database (built-in Python) |

---

## 🛣️ Routes

| Blueprint | Route | Method | Chức năng |
|-----------|-------|--------|-----------|
| auth | `/auth/login` | GET/POST | Đăng nhập |
| auth | `/auth/logout` | GET | Đăng xuất |
| auth | `/auth/profile` | GET | Thông tin cá nhân |
| register | `/register/` | GET/POST | Đăng ký |
| products | `/products/` | GET | Tìm kiếm sản phẩm |
| scores | `/scores/search` | GET/POST | Tra cứu điểm |
| articles | `/articles/` | GET | Danh sách bài viết |
| articles | `/articles/<id>` | GET | Chi tiết bài viết |
| cart | `/cart/` | GET | Xem giỏ hàng |
| cart | `/cart/add` | POST | Thêm vào giỏ |
| cart | `/cart/update` | POST | Cập nhật giỏ |
| cart | `/cart/remove` | POST | Xóa 1 sản phẩm |
| cart | `/cart/clear` | POST | Xóa toàn bộ giỏ |
| cart | `/cart/proceed` | POST | Đặt hàng |
| cart | `/cart/orders` | GET | Đơn hàng của tôi |
| cart | `/cart/orders/<id>` | GET | Chi tiết đơn hàng |
| admin | `/admin/storages` | GET | DS sản phẩm (admin) |
| admin | `/admin/storages/add` | GET/POST | Thêm sản phẩm |
| admin | `/admin/storages/edit/<id>` | GET/POST | Sửa sản phẩm |
| admin | `/admin/storages/delete/<id>` | POST | Xóa sản phẩm |
| admin | `/admin/orders` | GET | DS đơn hàng (admin) |
| admin | `/admin/orders/<id>` | GET/POST | Xử lý đơn hàng |

---

## 👨‍💻 Tác giả

**Hoàng Năng Minh** — Flask Blueprint Project 🐸
