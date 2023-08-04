# 设置基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app/

# 安装依赖包
RUN pip install -r requirements.txt

# 运行 Django 项目
CMD python manage.py runserver 0.0.0.0:8080