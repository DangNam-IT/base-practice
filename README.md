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
base-practice/
├────src/
    ├── app/
    │ ├── main.py       # Entry point, khởi tạo app
    │ ├── config.py     # config database structure
    │ ├── logger.py     # define, set up format for log (Debug, Info, Error, Warning) 
    │ ├── database.py   # Cấu hình kết nối DB & Session
    │ ├── models/       # SQLAlchemy Models (Database tables)
    │ │   ├── author.py
    │ │   ├── book.py
    │ │   └── user.py
    │ ├── schemas/      # Pydantic Models (Data validation/API Response)
    │ │   ├── books.py
    │ │   ├── authors.py
    │ │   ├── token.py
    │ │   └── books.py
    │ ├── service/      # Logic thao tác Database
    │ │   ├── crud_authors.py
    │ │   └── crud_books.py
    │ └── api/          # Thư mục chứa các route
    │    ├── auth.py
    │    ├── authors.py
    │    └── books.py
    ├── venv/ 
    ├── .gitignore
    ├── .env            # Biến môi trường (DB_URL, SECRET_KEY)
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

## 🚀 I. Vận Hành Ứng Dụng (Development Phase)

### 1. Cấu trúc HTTP & luồng Request
FastAPI xử lý Request dựa trên kiến trúc **Stateless**.
* **Flow:** Client Request → Middleware → Dependencies (Auth, DB) → Route Handler (Logic) → Response.

### 2. Cơ chế `yield` trong Dependency Injection
Sử dụng trong các hàm như `get_db` để quản lý tài nguyên.
* **Cơ chế:** Hoạt động giống như một *Context Manager*.
* **Luồng chạy:** 1. Chạy code trước `yield` (Mở kết nối DB).
    2. Tạm dừng và bàn giao đối tượng cho API.
    3. Sau khi API phản hồi, quay lại chạy code sau `yield` (Đóng kết nối qua `finally`).

### 3. Ý nghĩa của ký hiệu `@` (Decorators)
* **`@app.get() / @app.post()`**: Đăng ký hàm bên dưới trở thành một API Endpoint.
* **`@property`**: Biến một hàm thành một thuộc tính (không cần dùng dấu `()` khi gọi).
* **`@pytest.fixture`**: Đánh dấu một hàm là nguồn cung cấp tài nguyên cho việc test.

### 4. `Depends` vs `Query`
* **`Depends`**: Tiêm phụ thuộc (Dependency Injection). Dùng để chia sẻ logic (DB session, Security) giữa các router.
* **`Query`**: Ràng buộc và xác thực dữ liệu trực tiếp trên URL (ví dụ: `?limit=10&q=search`). Cho phép đặt `min_length`, `max_length`, `regex`.

### 5. Luồng xác thực JWT (JSON Web Token)
1. **Login:** Client gửi credentials -> Server xác thực và ký Token (với `SECRET_KEY`).
2. **Storage:** Client lưu Token (thường trong LocalStorage).
3. **Authorization:** Mỗi request sau đó, Client gửi kèm Header `Authorization: Bearer <token>`.
4. **Verification:** Server dùng `OAuth2PasswordBearer` bóc tách token và giải mã để định danh User.

---

## 🧪 II. Kiểm Thử Ứng Dụng (Testing Phase)

### 1. Cấu trúc HTTPX & TestClient
* **`TestClient`**: Dựa trên thư viện **HTTPX**, cho phép giả lập các request HTTP gửi vào app ngay trong bộ nhớ (In-memory) mà không cần mở cổng mạng thật.
* **Sync vs Async**: Mặc định `TestClient` chạy đồng bộ (Sync), phù hợp cho hầu hết các bài test CRUD đơn giản.

### 2. Pytest Fixtures (`@pytest.fixture`)
Dùng để thiết lập môi trường "sạch" trước mỗi bài test.
* **`scope="function"`**: Fixture được tạo lại cho mỗi hàm test (đảm bảo tính độc lập).
* **`autouse=True`**: Tự động chạy mà không cần khai báo tham số (ít dùng để tránh khó kiểm soát).

### 3. `with TestClient(app) as c:`
* Khởi tạo một phiên làm việc giả lập với ứng dụng. 
* Sử dụng `with` (Context Manager) để đảm bảo các sự kiện `startup` và `shutdown` của App được kích hoạt chính xác trong lúc test.

### 4. Ghi đè phụ thuộc (Dependency Overrides)
Đây là kỹ thuật quan trọng nhất để tách biệt môi trường Test và Production.
```python
app.dependency_overrides[get_db] = override_get_db
```
* **Cơ chế:** "Lừa" FastAPI sử dụng một hàm khác (thường kết nối tới SQLite In-memory) thay vì hàm `get_db` thật.
* **Dọn dẹp:** Phải gọi `.clear()` sau mỗi bài test để trả ứng dụng về trạng thái nguyên bản.

---

## 💾 III. Database Testing (SQLite In-Memory)

* **`sqlite:///:memory:`**: Cơ sở dữ liệu tồn tại hoàn toàn trên RAM. Tốc độ cực nhanh, tự xóa sạch khi bài test kết thúc.
* **`StaticPool`**: Ép SQLAlchemy sử dụng duy nhất một kết nối xuyên suốt, giúp dữ liệu không bị mất giữa các lần gọi `get_db` trong cùng một bài test.

---

## 🛠 IV. Mẹo nhỏ (Pro-tips)
* **Thứ tự Import:** Trong file `conftest.py`, luôn đặt `os.environ` lên đầu để đảm bảo app nhận cấu hình Test trước khi khởi tạo DB.
* **Autoflush:** Trong `sessionmaker`, `autoflush=True` giúp bạn thấy ngay dữ liệu vừa `add` khi thực hiện truy vấn ngay sau đó mà không cần gọi `flush()` thủ công.

Tôi là người ngoài, OK
