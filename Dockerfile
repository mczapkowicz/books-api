FROM python:2.7
ADD . /my-books
WORKDIR /my-books
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]