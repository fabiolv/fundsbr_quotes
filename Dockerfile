FROM python:3.10

# RUN echo 'Installing bash and nano in Alpine'
# RUN apk add --no-cache bash nano

WORKDIR /app/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80

# CMD ["flask", "run", "--host 0.0.0.0", "--port 80"]
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]