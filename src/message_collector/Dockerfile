FROM python:3.10.13-alpine3.18

COPY . .

RUN pip install -r requirements.txt && rm requirements.txt

CMD ["python", "__main__.py"]