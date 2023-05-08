FROM python:3.10

WORKDIR /publisher
COPY /requirements.txt /publisher/requirements.txt

ADD /api /publisher/api


COPY /pip.conf pip.conf
ENV PIP_CONFIG_FILE pip.conf
RUN pip install --no-cache-dir -r /publisher/requirements.txt

COPY ./dist/core-0.1.0.tar.gz /publisher/core-0.1.0.tar.gz
RUN pip install --upgrade /publisher/dist/core-0.1.0.tar.gz

COPY ./__main__.py /publisher
ENTRYPOINT ["python", "-u", "/publisher/__main__.py"]