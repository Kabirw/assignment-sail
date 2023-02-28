FROM python:3.10

# copy crontab file to container
COPY crontab /etc/cron.d/crontab

# give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/crontab


COPY . /usr/src/app/Assignment

RUN pip install --trusted-host pypi.python.org -r /usr/src/app/Assignment/Requirements.txt

# start cron service
CMD ["cron", "-f"]
