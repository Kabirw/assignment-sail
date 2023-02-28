import json
import pandas as pd
import requests
from datetime import datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import config 
import user_config
import logging


url = 'https://api.github.com/repos/public-apis/public-apis/pulls?state=all'
headers = {'Accept': 'application/vnd.github.v3+json'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Convert the response content to a list of dictionaries
    data = response.json()
    
    # Create a pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    
    # Filter the DataFrame to only include the columns we want
    df = df[['id', 'state', 'title', 'created_at','updated_at','closed_at','merged_at']]
else:
    print('Error: Failed to retrieve data')



df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d').dt.date
df['updated_at'] = pd.to_datetime(df['updated_at'], format='%Y-%m-%d').dt.date
df['closed_at'] = pd.to_datetime(df['closed_at'], format='%Y-%m-%d').dt.date
df['merged_at'] = pd.to_datetime(df['merged_at'], format='%Y-%m-%d').dt.date


now = datetime.today().date()
one_week_ago = now - timedelta(weeks=1)

filtered_df = df[(df['created_at'] >= one_week_ago) & (df['created_at'] <= now)]
name_counts = filtered_df['state']
total_count = len(name_counts)

sender_email = config.username
receiver_email = user_config.receiver_email
password = config.password

message = MIMEMultipart()
message["From"] = config.username
message["To"] = receiver_email
message["Subject"] = user_config.Subject

body = f'Hi, Here is an update from the past week.\nBelow you will find a summary of PRs raised in the past week. \nAlso total PRs raised in last week {total_count} '
message.attach(MIMEText(body, "plain"))

table_html = filtered_df.to_html(index=False)

#attachment = MIMEApplication(csv, _subtype='csv')
#attachment.add_header('content-disposition', 'attachment', filename='data.csv')

message.attach(MIMEText(table_html, 'html'))

logging.basicConfig(level=logging.DEBUG)

# create SMTP session
session = smtplib.SMTP(config.host, config.port)
session.starttls() # enable security
session.login(sender_email, password) # login with credentials
session.set_debuglevel(1)
text = message.as_string()
session.sendmail(sender_email, receiver_email, text)
session.quit()


print('Mail Sent')
#This code sends a plain text email from the sender's email address to the receiver's email address using the Gmail SMTP server. You can modify the code to include attachments or use HTML content instead of plain text by modifying the MIMEText and MIMEMultipart objects.




