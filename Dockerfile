#This i an image that install all requirements and execute the python script with arguments

FROM python:2
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./benchmark.py ./
CMD python ./benchmark.py $ARGS
