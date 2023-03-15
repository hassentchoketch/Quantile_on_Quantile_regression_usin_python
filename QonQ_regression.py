import os 
import pandas as pd 
import numpy as np 
import statsmodels.formula.api as smf

pd.options.mode.chained_assignment = None
# import plotly.graph_objects as go

def Q_QR(df,x,y,quarters=None):
  df1=df[[x,y]]
  results = []
  xx = np.linspace(min(df1[x]),max(df1[x]),len(quarters))
  for q in(quarters):
    slopes = []
    for i in range(len(xx)):
          df1['z']= df1[x].values-xx[i]
          r = smf.quantreg(f'{y}~z',df1)
          reg=r.fit(q=q)
          slopes.append(reg.params["z"])
    results.append(slopes)
  return results



df = pd.read_csv('data.csv').drop(columns ='Unnamed: 0').set_index('date')
print(df.info())

results = Q_QR(df,'PCPI_IX_US','NGDP_R_SA_XDC_US',quarters= np.arange(0.01,0.99,0.25).tolist())
matrix = np.asarray(results).T
print(results)