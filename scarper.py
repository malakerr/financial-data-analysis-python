import pandas as pd
import requests
from bs4 import BeautifulSoup

#Methode 1 : Using BeautifulSoup to scrape the data from the website

#Step 1 : Send a GET request to the website
url_netflix = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"
data = requests.get(url_netflix).text

#Step 2 : Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(data, 'html.parser')

# Step 3: Identify the HTML tags
netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])

# Step 4: Extract the data
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text
    
    # Finally we append the data of each row to the table
    netflix_data = pd.concat([netflix_data,pd.DataFrame({"Date":[date], "Open":[Open], "High":[high], "Low":[low], "Close":[close], "Adj Close":[adj_close], "Volume":[volume]})], ignore_index=True)    
print(netflix_data.head())

#Methode 2 : Using Pandas to scrape the data from the website

#Step 1 : Send a GET request to the website
read_html_pandas_data = pd.read_html(url_netflix)
#Step 2 : Extract the data
netflix_data_pandas = read_html_pandas_data[0]
print(netflix_data_pandas.head())