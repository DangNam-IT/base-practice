#chuẩn bị layer để xây dựng các layer khác trên layer này để tạo image phục vụ việc tạo container
FROM python:3.11-slim

#chỉ định thư mục làm việc trong container, các lệnh bên dưới sẽ được thực thi dựa trên thư mục này
WORKDIR /app
 
#set up các biến môi trường để tối ưu hóa hiệu suất và quản lý cache của pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1        \
    PIP_NO_CACHE_DIR=1          \
    PYTHONPATH=/app/src

# cài đặt gói tin, cập nhật và cài đặt các gói cần thiết, sau đó xóa cache để giảm kích thước image
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \ 
    && rm -rf /var/lib/apt/lists/*

#cài các dependencies cần thiết cho ứng dụng, sử dụng pip để cài đặt các gói được liệt kê trong requirements.txt. Hơn hết, khi mã nguồn của ứng dụng thay đổi,
# Docker sẽ chỉ cần cài đặt lại các gói nếu requirements.txt thay đổi, giúp tăng tốc quá trình xây dựng image
# Nếu không đổi, lấy cache của layer này
COPY requirements.txt .

#cài đặt các gói trong requirements.txt 
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy toàn bộ source code vào /app
COPY . .

#thông báo cổng cho compose nếu có
EXPOSE 8000

#Check status container, nếu có lỗi sẽ tự động restart container
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')."

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]