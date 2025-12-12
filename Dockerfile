# Use a lightweight Python image
FROM python:3.11-slim

# set workdir
WORKDIR /app

# copy requirements first (for caching)
COPY requirements.txt /app/requirements.txt

# install system deps (if any) and pip packages
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential \
    && pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && apt-get purge -y --auto-remove gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy app
COPY . /app

ENV PYTHONUNBUFFERED=1

# expose
EXPOSE 8000

# default cmd
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
