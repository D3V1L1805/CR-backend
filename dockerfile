FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    default-jre \
    default-jdk \
    build-essential \
    && apt-get clean

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
ENV PATH="$JAVA_HOME/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5000

CMD ["uvicorn", "router:app", "--host", "0.0.0.0", "--port", "5000"]
