import os
import requests
import pandas as pd 

cwd = os.getcwd()

def get_imf_series_codes(search_terms = None ):
   url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
   series_codes = {}
   for term in search_terms: 
      key_family = 'DataStructure/IFS'  # Method / series
      dimension_list = requests.get(f'{url}{key_family}').json()\
            ['Structure']['KeyFamilies']['KeyFamily']\
            ['Components']['Dimension']
      key_dimention = f"CodeList/{dimension_list[2]['@codelist']}"
      code_list = requests.get(f'{url}{key_dimention}').json()\
  	    ['Structure']['CodeLists']['CodeList']['Code']
      for code in code_list:
         # if term in code['Description']['#text']:
         if term in code['@value']:
            series_codes[code['Description']['#text']] = code['@value']
   print(len(series_codes.keys()),len(series_codes.values()))
   return pd.DataFrame({'Series_name': series_codes.keys() ,'Series_code':series_codes.values()})        
 
def imf_data_query(series_codes = None, country_codes = None ,frequency=None, start_period = None,end_eriod=None):
   url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
   df = pd.DataFrame()
   for c_code in country_codes:
      for s_code in series_codes:
          key= f"CompactData/IFS/{frequency}.{c_code}.{s_code}.?startPeriod={start_period}&endPeriod={end_eriod}"  # adjust codes here
          # Navigate to series in API-returned JSON data
          series = (requests.get(f"{url}{key}").json()["CompactData"]["DataSet"]["Series"])
          df[s_code + '_'+c_code ] = [obs.get("@OBS_VALUE") for obs in series["Obs"]]
   df.index = pd.to_datetime([obs.get("@TIME_PERIOD") for obs in series["Obs"]])
   df.to_csv(cwd +'\\data.csv')
   return df 



search_term = ['CPI','GDP']
results = get_imf_series_codes(search_terms=search_term)
# print(results)

series_codes = ['PCPI_IX','NGDP_R_SA_XDC']
country_codes = ['US','GB']
df = imf_data_query(series_codes=series_codes , country_codes=country_codes,frequency= 'Q', start_period= '1990' ,end_eriod= '2021')
print(df)