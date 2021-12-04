import requests
import pandas as pd

result = requests.get(
    f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&interval=5min&apikey=GH1N9SQU05XP2NNG&datatype=csv"
)
with open("stocks.csv", 'wb') as file:
    file.write(result.content)
df = pd.read_csv('stocks.csv')
print(df)