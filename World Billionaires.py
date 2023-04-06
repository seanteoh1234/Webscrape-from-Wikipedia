import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/The_World%27s_Billionaires"
data = requests.get(url).text
soup = BeautifulSoup(data,'html.parser')

test = (soup.find_all('p'))

for i in test:
    if 'In the 37th' in str(i):
        a = i.find_next('table')
        r = soup.find_all('table').index(a)

table = (soup.find_all('table')[r])

wealthiestman = pd.DataFrame(columns= ["No.","Name","Net Worth","Age","Nationality","Source of Wealth"])
for row in table.find_all('tr'):
    td = row.find_all('td')
    if td != []:
        no = td[0].text.strip()
        name = td[1].text.strip()
        net = td[2].text.strip()
        age = td[3].text.strip()
        nationality = td[4].text.strip()
        source = td[5].text.strip()
        wealthiestman = pd.concat([wealthiestman,pd.DataFrame({"No.":[no],"Name":[name],"Net Worth":[net],"Age":[age],"Nationality":[nationality],"Source of Wealth":[source]})])
print (wealthiestman)
