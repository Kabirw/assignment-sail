import urllib3
from urllib3 import request
import certifi 
import json
import pandas as pd
import requests

#http = urllib3.PoolManager(
#       cert_reqs='CERT_REQUIRED',
#       ca_certs=certifi.where()) 
       
#url = https://api.github.com/repos/public-apis/public-apis/pulls?state=all
#r = request.get('GET', url)
#r.status       


url = 'https://api.github.com/repos/public-apis/public-apis/pulls?state=all'
headers = {'Accept': 'application/vnd.github.v3+json'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Convert the response content to a list of dictionaries
    data = response.json()
    
    # Create a pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    
    # Filter the DataFrame to only include the columns we want
    df = df[['id', 'html_url', 'state', 'title', ]]
else:
    print('Error: Failed to retrieve data')

# Print the first few rows of the DataFrame
print(df.head())