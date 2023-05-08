FROM python:3.10

WORKDIR /inspector
COPY /requirements.txt /inspector/requirements.txt

ADD /api /inspector/api

COPY pip.conf pip.conf
ENV PIP_CONFIG_FILE pip.conf
RUN pip install --no-cache-dir -r /inspector/requirements.txt

COPY ./core-0.1.0.tar.gz /inspector/core-0.1.0.tar.gz
RUN pip install --upgrade /inspector/core-0.1.0.tar.gz

COPY ./__main__.py /inspector/__main__.py
ENTRYPOINT ["python", "-u", "/inspector/__main__.py"]