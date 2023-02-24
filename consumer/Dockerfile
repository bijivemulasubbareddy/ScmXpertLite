FROM python:3.9
WORKDIR /app
RUN pip install pymongo[srv]  kafka-python python-dotenv==0.19.2
COPY consumer.py .
CMD ["python","consumer.py"]