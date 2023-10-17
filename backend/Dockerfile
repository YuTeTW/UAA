#
FROM python:3.9-alpine

#
WORKDIR /UnifiAccess

#
COPY ./requirements.txt /UnifiAccess/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /UnifiAccess/requirements.txt

#
USER nonprivilegeduser

#
COPY ./app /UnifiAccess
