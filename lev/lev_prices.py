import requests
import json
import pandas as pd
import os
import re

# categories
categories = {
  'Aguas': 17,
  'Doces': 21, 
  'Choco Kabkaj': 76, 
  'Molhos, Compotas e Cremes': 24, 
  'Nutricosmetica': 66, 
  'Padaria e Pastelaria': 25,
  'Pro e Pre Biotico': 67,
  'Refeições': 22, 
  'Snacks Salgados': 23,
  'Suplementos e Elixires': 19
  }

# setup HEADERS | per page max is 100, NEED TO CHANGE WHEN SCRIPT IS WORKING
payload = {}
headers = {
  'authority': 'levcms.live.afonso.se',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'authorization': 'Basic ${{secrets.LEV_TOKEN}}',
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

# get responses
response = []
for cat in categories:
    url = "https://levcms.live.afonso.se/wp-json/wc/v3/products?category=" + str(categories[cat]) + "&per_page=100&page=1&hide_empty=true&catalog_visibility=visible"
    r = requests.request("GET", url, headers=headers, data=payload)
    data = r.json()
    for i in data:
      response.append(i)

# write to file
with open("tempData.json", "w") as outfile:
    json.dump(response, outfile)

# create Dataframe
df0 = pd.read_json("tempData.json")
print(df0.columns)

quit()

# simplify Dataframe
values = []
text = []
for i in range(len(df0)):
    meta_norm = pd.json_normalize(df0.meta_data[i])
    raw_values = meta_norm[meta_norm['key'] == 'dropdown_3_dropdown_content'].value
    try:
        list_values = re.findall(r'\d+', raw_values.item())
        list_text = raw_values.item()
    except:
        list_values = [1]
        list_text = ""
    values.append(list_values)
    text.append(list_text)
s = pd.Series(data=values)
t = pd.Series(data=text)
df1 = df0.join(s.rename('quantidades'))
df2 = df1.join(t.rename('text'))
df3 = pd.DataFrame(df2, columns=['name', 'sku', 'price', 'quantidades', 'text', 'categories'])
df3_list = df3['quantidades'].to_list()
for item in range(len(df3_list)):
    df3_list[item] = df3_list[item][:3]
df4 = df3.join(pd.DataFrame(df3_list, columns=['units', 'weight', 'total_weight']))
df5 = df4.drop('quantidades', axis=1)

# write csv
df5.to_csv('lev_csv.csv')

# delete file
os.remove("tempData.json")

#print results
# print(df5.columns)
# print(df5)
