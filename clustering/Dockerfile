# Sử dụng Python base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép mã nguồn vào container
COPY . /app

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Chạy script Python
CMD ["python", "main.py"]