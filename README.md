Để giúp bạn bắt đầu nhanh, mình hệ thống lại bài tập **Hệ thống Quản lý Thư viện (Library Management System)** dưới dạng file Markdown để bạn dễ dàng lưu lại làm Checklist.
---
# 📚 Project: Library Management System (Python BE)
## 🛠 Tech Stack
- **Framework:** FastAPI (hoặc Flask)
- **Database:** PostgreSQL (hoặc SQLite để bắt đầu nhanh)
- **ORM:** SQLAlchemy (hoặc Tortoise-ORM)
- **Validation:** Pydantic
- **Auth:** JWT (JSON Web Tokens)
## 📂 Cấu trúc thư mục (Layered Architecture)
```text
library_project/
├── app/
│ ├── main.py # Entry point, khởi tạo app
│ ├── database.py # Cấu hình kết nối DB & Session
│ ├── models.py # SQLAlchemy Models (Database tables)
│ ├── schemas.py # Pydantic Models (Data validation/API Response)
│ ├── crud.py # Logic thao tác Database
│ └── api/ # Thư mục chứa các route
│ ├── auth.py # Đăng ký/Đăng nhập
│ └── books.py # Quản lý sách
├── .env # Biến môi trường (DB_URL, SECRET_KEY)
├── requirements.txt
└── README.md
```
## 🗄 Thiết kế Database (Schemas)
1. **Authors:** `id`, `name`, `bio`.
2. **Books:** `id`, `title`, `isbn`, `author_id` (FK), `is_available` (bool).
3. **Users:** `id`, `username`, `hashed_password`, `role` (admin/user).
## 🚀 Chức năng chính (CRUD & Auth)
### 1. Quản lý Sách & Tác giả
- [ ] **Create:** Thêm sách mới (Validate ISBN, kiểm tra Author tồn tại).
- [ ] **Read:** Lấy danh sách sách kèm thông tin Tác giả (dùng `join`).
- [ ] **Update:** Cập nhật thông tin hoặc trạng thái sách.
- [ ] **Delete:** Xóa sách (nên thực hiện xóa mềm).
- [ ] **Search:** Tìm kiếm theo tiêu đề hoặc lọc theo tác giả.
### 2. Xác thực & Phân quyền
- [ ] Đăng ký / Đăng nhập trả về **JWT Token**.
- [ ] User thường: Chỉ được xem sách.
- [ ] Admin: Được quyền Thêm/Sửa/Xóa.
## 🌟 Checklist để "Ghi điểm" (Fresher+)
- [ ] **Pagination:** Phân trang cho API lấy danh sách sách (`limit`, `offset`).
- [ ] **Logging:** Ghi log lại các lỗi (Exception) vào file thay vì dùng `print`.
- [ ] **Type Hinting:** Sử dụng Type Hints của Python 3.10+ triệt để.
- [ ] **API Docs:** Tận dụng Swagger UI (mặc định trong FastAPI) để viết mô tả cho từng API.
- [ ] **Unit Test:** Viết tối thiểu 5-10 test cases với `pytest`.
---
**Cách bắt đầu nhanh:**
1. Tạo môi trường ảo: `python -m venv venv`
2. Cài đặt thư viện: `pip install fastapi uvicorn sqlalchemy psycopg2-binary`
3. Code file `database.py` đầu tiên để kết nối DB.
