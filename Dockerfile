FROM ubuntu:20.04

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y curl gnupg2

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

ARG ACCEPT_EULA=Y

RUN apt-get update && apt-get install -y g++ python3-pip msodbcsql17 mssql-tools && ln -s /usr/bin/python3 /usr/bin/python

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

#RUN source ~/.bashrc
#add opencensus-ext-azure
RUN apt-get install -y unixodbc-dev

RUN python -m pip install --upgrade pip

COPY ./django_project_frontend/ /code/

RUN useradd django && chown -R django /code

RUN pip install -r requirements.txt

USER django

CMD python manage.py runserver 0.0.0.0:8000