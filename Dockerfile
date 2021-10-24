FROM python:3.8.2
ADD . /my-books
WORKDIR /my-books
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]