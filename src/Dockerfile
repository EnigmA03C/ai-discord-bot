FROM python:latest
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
EXPOSE 5000

RUN useradd app
USER app

CMD [ "python", "src/Luna.py"]