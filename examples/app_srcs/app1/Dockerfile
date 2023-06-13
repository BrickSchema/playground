FROM python:3
COPY . /app1
WORKDIR /app1
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "index.py"]
