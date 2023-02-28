FROM python:3.10
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get update && apt-get -y install cron   

COPY crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab

RUN pip install --trusted-host pypi.python.org -r Requirements.txt

# start cron service
CMD ["cron", "-f"]



