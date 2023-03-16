import os 
import pandas as pd 
import numpy as np 
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt 


def Q_QR(df= None , x= None, y=None,path= None,quarters=np.arange(0.01,0.9,0.05), plot = True):
  df1=df[[x,y]]
  slope_results = []
  intrcept_results = []
  xx = np.linspace(min(df1[x]),max(df1[x]),len(quarters))
  for q in(quarters):
    slopes = []
    intercepts = []
    for i in range(len(xx)):
          df1['z']= df1[x]-xx[i]
          r = smf.quantreg(f'{y}~z',df1)
          reg=r.fit(q=q)
          slopes.append(reg.params["z"])
          intercepts.append(reg.params['Intercept'])
    slope_results.append(slopes)
    intrcept_results.append(intercepts)
  matrix_slope = np.array(slope_results).T 
  matrix_intercept = np.array(intrcept_results).T

  if plot:   
    fig = plt.figure(figsize=(16,8))
    # fig, ax = plt.subplots(1, 2)
    ax1 = fig.add_subplot(111, projection='3d')
    ax2 = fig.add_subplot(112, projection='3d')
    X, Y = np.meshgrid(quarters, quarters) 
    surf1 =ax1.plot_surface(X, Y, matrix_slope , cmap= 'viridis',alpha = 0.7 )
    surf2 =ax2.plot_surface(X, Y, matrix_intercept , cmap= 'viridis',alpha = 0.7 )
    fig.colorbar(surf1)
    fig.colorbar(surf2)
    ax1.set_xlabel(f'{df.columns[0]}_Quartiles')
    ax1.set_ylabel(f'{df.columns[1]}_Quartiles')
    ax1.set_zlabel('Slope')
    ax2.set_xlabel(f'{df.columns[0]}_Quartiles')
    ax2.set_ylabel(f'{df.columns[1]}_Quartiles')
    ax2.set_zlabel('Intercept')
    plt.title(f'Quantile-on-Quantile Process for the {df.columns[0]}  Coefficients',fontdict = {'fontsize': 18,'fontweight': 16})
    plt.tight_layout()
    fig.savefig(path + '\\plot.png')
    plt.show()
    slopes =pd.DataFrame(matrix_slope)
    intercepts = pd.DataFrame(matrix_intercept)
    slopes.to_csv(path+'\\slopes.csv')
    intercepts.to_csv(path+'\\intercepts.csv')
  return slopes ,intercepts


cwd = os.getcwd()
df = pd.read_csv(f'C:\Users\Hassen\Desktop\Quantile_on_Quantile_regression_usin_python\data.csv').drop(columns ='Unnamed: 0').set_index('date')
df_slopes,df_interceptes = Q_QR(df = df,x ='NGDP_R_SA_XDC_US',y ='PCPI_IX_US', path = cwd)
print(cwd)