FROM python:3.8
WORKDIR /imapper

COPY setup.py setup.cfg ./
RUN mkdir -p src
RUN pip install .

COPY . .
ENTRYPOINT [ "python", "-m", "src" ]
 