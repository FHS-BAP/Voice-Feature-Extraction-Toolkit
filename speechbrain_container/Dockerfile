FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Update and install required packages
RUN apt-get update && \
    apt-get install -y ffmpeg
    
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]