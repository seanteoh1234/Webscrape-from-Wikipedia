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
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Get Tesla Stock Data
Ticker = yfinance.Ticker('TSLA')
data = Ticker.history(period='max')
tesla_data = pd.DataFrame(data)
tesla_data.reset_index(inplace=True)

#Get Tesla Data for Revenue
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response = requests.get(url)
html_data = response.text
soup = BeautifulSoup(html_data,'html5lib')
tables = soup.find_all('table')
# loop through the tables and find the one containing "Tesla Quarterly Revenue"
for i, table in enumerate(tables):
    th = table.find_all('th')
    if "Tesla Quarterly Revenue" in str(th):
        print(f"Found Tesla Quarterly Revenue in table {i}")
        break
tesla_revenue = pd.DataFrame(columns = ['Date','Revenue'])

for data in tables[i].find_all('tr'):
    col = data.find_all('td')
    if col != []:
        date = col[0].text
        revenue = col[1].text
        tesla_revenue = pd.concat([tesla_revenue,pd.DataFrame({'Date':[date],'Revenue':[revenue]})],ignore_index=True)
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
print (tesla_revenue)

#Create Graph
make_graph(tesla_data, tesla_revenue, 'Tesla')
