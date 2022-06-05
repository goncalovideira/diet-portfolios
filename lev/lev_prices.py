import requests
import json
import pandas as pd
import os

# setup URL and HEADERS | per page max is 100, NEED TO CHANGE WHEN SCRIPT IS WORKING
url = "https://levcms.live.afonso.se/wp-json/wc/v3/products?category=22&per_page=2&page=1&hide_empty=true&catalog_visibility=visible"
payload={}
headers = {
  'authority': 'levcms.live.afonso.se',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'authorization': 'Basic ${{secrets.lev_token}}',
  'origin': 'https://lev.pt',
  'referer': 'https://lev.pt/',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'cross-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
}

# get response
response = requests.request("GET", url, headers=headers, data=payload)

# write to file
with open("tempData.json", "w") as outfile:
    json.dump(response.json(), outfile)

quit()

# create Dataframe
df = pd.read_json("tempData.json")

# delete file
os.remove("tempData.json")

#print results
print(df.columns)
print(df['price'])