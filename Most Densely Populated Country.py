import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/World_population"
data  = requests.get(url).text
soup = BeautifulSoup(data,"html.parser")
tables = soup.find_all('table')

#finding table index using captions which is written as a child in the desired table.
for index,table in enumerate(tables):
    if ("10 most densely populated countries" in str(table)):
        table_index = index
        # print (table)

population_data = pd.DataFrame(columns=["Rank", "Country", "Population", "Area", "Density"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        # print (col)
        rank = col[0].text
        country = col[1].text.strip()
        population = col[2].text.strip()
        area = col[3].text.strip()
        density = col[4].text.strip()
        population_data = pd.concat([population_data, pd.DataFrame({"Rank":[rank], "Country":[country], "Population":[population], "Area":[area], "Density":[density]})], ignore_index=True)
print (population_data)
