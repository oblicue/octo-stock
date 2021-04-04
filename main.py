import threading
import numpy as np
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import requests
# add the stocks you would like - parses through and gets value of each stock
analyse = [
    "DIS",
    "AAPL",
    "COKE",
    "RBLX",
    "SBUX",
    "NKE",
    "HD",
    "NVDA",
    "DOGE-BTC"
]
#getting your api token from the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

#you can also add your own custom date instead of yesterdays date
date = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
print(f"DATE IS: {date}")

for i in analyse:
    r = requests.get(f'https://api.polygon.io/v1/open-close/{i}/{date}?unadjusted=true&apiKey={TOKEN}').text
    print(f"{i}: {r}")
