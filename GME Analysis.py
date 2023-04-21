import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True,)
    fig.show()
        
    
#Get GME Stock Price Data
gme = yfinance.Ticker('GME')
a = gme.history(period='max')
gme_data = pd.DataFrame(a)
gme_data.reset_index(inplace=True)
print(gme_data)

#Get GME Revenue Data
link = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
linkData = requests.get(link).text
soup = BeautifulSoup(linkData,'html5lib')
tables = soup.find_all('table')
for i,table in enumerate(tables):
    headers = table.find_all('th')
    if 'GameStop Quarterly Revenue' in str(headers):
        identification = f'GameStop Quarterly Revenue is found in table {i}'
      
gme_revenue = pd.DataFrame(columns=['Date','Revenue'])

for data in tables[1].find_all('tr'):
    col = data.find_all('td')
    if col != []:
        date = col[0].text
        column = col[1].text
        gme_revenue = pd.concat([gme_revenue,pd.DataFrame({'Date':[date],'Revenue':[column]})],ignore_index=True)
gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace(',|\$',"")
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue']!='']

#Create Table
make_graph(gme_data, gme_revenue, 'GameStop')