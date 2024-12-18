# official Python slim image for a lighter build
FROM python:3.10-slim

# working directory inside the container
WORKDIR /app

# system dependencies for PostgreSQL and other libraries
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# requirements first for Docker caching optimization
COPY requirements.txt requirements.txt

# python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy rest of application code into the container
COPY . .

# port exposure
EXPOSE 8000

# database migrations and Django development server start
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
