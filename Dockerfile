FROM python:3.9

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /polka

# Install dependencies using pip install
RUN pip install numpy==1.24.2
RUN pip install pandas==1.5.2
RUN pip install Django==4.2.4
RUN pip install celery
RUN pip install redis
RUN pip install openpyxl
RUN pip install django-background-tasks==1.2.5
RUN pip install django-compat==1.0.15
RUN pip install django-cors-headers==4.2.0
RUN pip install django-crontab==0.7.1
RUN pip install tqdm==4.64.1
RUN pip install requests==2.25.0
RUN pip install bittensor==6.4.2

# Install Redis (without cron)
RUN apt-get update && apt-get install -y redis-server

# Install RabbitMQ
RUN apt-get install -y rabbitmq-server

# Copy the entire content of the current directory to /polka/ directory in the image
COPY . /polka/

# Expose the port your Django application will run on (e.g., 8000)
EXPOSE 8000

# Start Redis, RabbitMQ, the Celery worker, and Celery Beat, and your Django application
CMD (service rabbitmq-server start && python manage.py runserver 0.0.0.0:8000 & celery -A polka worker --loglevel=info >worker.log &  celery -A polka beat --loglevel=info)
