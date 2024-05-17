FROM python:3.11-slim

# set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libatlas-base-dev \
  libgdal-dev \
  gfortran


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the src to the folder
COPY ./src /app/src

# start the server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]