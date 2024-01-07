FROM python:3.13-rc-alpine

RUN mkdir /project
WORKDIR /project
RUN mkdir /images

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
