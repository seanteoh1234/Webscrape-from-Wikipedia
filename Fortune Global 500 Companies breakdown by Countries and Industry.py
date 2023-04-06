import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/Fortune_Global_500"
requestGet = requests.get(url).text
a = BeautifulSoup(requestGet,'html.parser')
tables = a.find_all('table')
for e,i in enumerate (a.find_all('table')):
    if "$486 billion" in str(i):
        index = e

fortuneGlobal = pd.DataFrame(columns=["Rank","Company","Country","Industry","Revenue in USD"])
for row in tables[index].tbody.find_all('tr'):
    col = row.find_all('td')
    if col != []:
        rank = col[0].text.strip()
        company = col[1].text.strip()
        country = col[2].text.strip()
        industry = col[3].text.strip()
        revenue = col[4].text.strip()
        fortuneGlobal = pd.concat([fortuneGlobal, pd.DataFrame({"Rank":[rank],"Company":[company],"Country":[country],"Industry":[industry],"Revenue in USD":[revenue]})],ignore_index=True)
print (fortuneGlobal)
