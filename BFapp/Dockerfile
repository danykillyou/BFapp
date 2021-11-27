FROM python:3.9
COPY . /BFapp
ADD odbcinst.ini /etc/odbcinst.ini
RUN apt-get update
RUN apt-get install -y tdsodbc unixodbc-dev
RUN apt install unixodbc-bin -y
RUN apt-get clean -y
RUN pip install -r BFapp/requirements.txt
CMD python BFapp/BFapp1.0.3.py