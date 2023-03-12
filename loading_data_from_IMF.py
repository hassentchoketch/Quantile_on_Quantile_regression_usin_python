import os
import requests
import pandas as pd 

cwd = os.getcwd()

search_terms = ['CPI','GDP']
url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
for term in search_terms:
 key = 'DataStructure/IFS'  # Method / series
 dimension_list = requests.get(f'{url}{key}').json()\
            ['Structure']['KeyFamilies']['KeyFamily']\
            ['Components']['Dimension']
# for n, dimension in enumerate(dimension_list):
    # print(f'Dimension {n+1}: {dimension["@codelist"]}')
 key = f"CodeList/{dimension_list[2]['@codelist']}"
 fey_word = 'gross_domestic_product'
 code_list = requests.get(f'{url}{key}').json()\
  	    ['Structure']['CodeLists']['CodeList']['Code']
 for code in code_list:
    # if search_terms in code['Description']['#text']:
    if term in code['@value']:
       print(f"{code['Description']['#text']}: {code['@value']}")

codes = ['PCPI_IX','NGDP_R_SA_XDC']
start_period = 1955
end_eriod    = 2021 
df = pd.DataFrame()

for code in codes:
   key= f"CompactData/IFS/Q.US.{code}.?startPeriod={start_period}&endPeriod={end_eriod}"  # adjust codes here
# Navigate to series in API-returned JSON data
   series = requests.get(f"{url}{key}").json()["CompactData"]["DataSet"]["Series"]
   df[code] = [obs.get("@OBS_VALUE") for obs in series["Obs"]]
   
df.index = pd.to_datetime([obs.get("@TIME_PERIOD") for obs in series["Obs"]])
df.to_csv(cwd +'\\data.csv')
