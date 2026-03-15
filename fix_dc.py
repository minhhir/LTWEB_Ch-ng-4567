import sqlite3
conn = sqlite3.connect('data/website.db')
# Kiểm tra dòng rác
rows = conn.execute("SELECT * FROM storages WHERE id = 'id'").fetchall()
print(f'Tìm thấy {len(rows)} dòng rác:', rows)
# Xóa dòng rác
conn.execute("DELETE FROM storages WHERE id = 'id'")
conn.commit()
print(f' Đã xóa! Còn lại: {conn.execute("SELECT COUNT(*) FROM storages").fetchone()[0]} sản phẩm')
conn.close()