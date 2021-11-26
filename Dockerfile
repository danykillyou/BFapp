FROM python:3-alpine
COPY . /BFapp
RUN pip install -r BFapp/requirements.txt
CMD python BFapp/BFapp1.0.3.py