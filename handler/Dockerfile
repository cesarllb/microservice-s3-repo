FROM python:3.10

WORKDIR /handler
COPY ./requirements.txt /handler/requirements.txt

ADD /bus_publisher /handler/bus_publisher

COPY pip.conf pip.conf
ENV PIP_CONFIG_FILE pip.conf
RUN pip install --no-cache-dir -r /handler/requirements.txt

COPY ./core-0.1.0.tar.gz /handler/core-0.1.0.tar.gz
RUN pip install --upgrade /handler/core-0.1.0.tar.gz

COPY ./__main__.py /handler/__main__.py
ENTRYPOINT ["python", "-u", "/handler/__main__.py"]