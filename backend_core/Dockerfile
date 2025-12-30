# Sử dụng Python 3.11 Slim (nhẹ, tối ưu)
FROM python:3.11-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Thư mục làm việc
WORKDIR /app

# Cài đặt dependencies hệ thống (cần cho psycopg2)
RUN apt-get update && apt-get install -y netcat-openbsd gcc && rm -rf /var/lib/apt/lists/*

# Cài đặt Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy source code
COPY . .

ENTRYPOINT ["/entrypoint.sh"]