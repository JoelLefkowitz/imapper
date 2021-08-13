FROM python:3.8

WORKDIR /imapper
COPY . .

RUN pip install .
ENTRYPOINT [ "python", "-m", "src" ]
