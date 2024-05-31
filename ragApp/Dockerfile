FROM python:3.10-slim


WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ["./requirementsRag.txt", "rag.py","main.py", "./"]

RUN pip install -r requirementsRag.txt

EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



#docker run -it --rm ragapp:latest python rag.py
#docker run -it --rm -v ${pwd}/app/:/app/ --entrypoint /bin/bash ragapp