FROM python:3.10-alpine
WORKDIR /bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /bot
CMD ["python", "src/main.py"]