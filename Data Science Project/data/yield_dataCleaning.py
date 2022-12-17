import pandas as pd
import numpy as np

df = pd.read_csv('worldwide_crop_consumption.csv')

def clean_yield(df):
    #define new data frame with only values from United States
    usa_temp=pd.DataFrame()
    usa_temp=df.loc[df["LOCATION"]=='USA']
    usa_temp.reset_index(inplace=True)
    #drop index and location
    usa_temp=usa_temp.drop(['index','LOCATION'],axis=1)
    #Define new dataframe,  will be returned 
    df_yield=pd.DataFrame(columns=['YEAR','RICE_TONNE_HA','RICE_THND_TONNE', 'RICE_THND_HA'
                                                ,'WHEAT_TONNE_HA','WHEAT_THND_TONNE', 'WHEAT_THND_HA'
                                                ,'MAIZE_TONNE_HA','MAIZE_THND_TONNE', 'MAIZE_THND_HA'
                                                ,'SOYBEAN_TONNE_HA','SOYBEAN_THND_TONNE', 'SOYBEAN_THND_HA'])
    #Make a list of all unique years
    years=[]
    years=usa_temp['TIME'].unique()
    #go through the list of unique years
    for year in years:
        location_list=[]
        #Save location of index, so we know where each value is 
        for i in usa_temp.index:
            if usa_temp['TIME'][i]==year:
                location_list.append(i)
            #define values so they may be useable in concat statement, all None since we dont know what they are yet    
            rice_t_ha=rice_th_t=rice_th_ha=WHEAT_t_ha=WHEAT_th_t=WHEAT_th_ha=MAIZE_t_ha=MAIZE_th_t=MAIZE_th_ha=SOYBEAN_t_ha=SOYBEAN_th_t=SOYBEAN_th_ha=None
            #go through list of indices and save value for each columns 
            for l in location_list:
                if usa_temp['SUBJECT'][l]=='RICE' and usa_temp['MEASURE'][l]=='TONNE_HA':
                    rice_t_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='RICE' and usa_temp['MEASURE'][l]=='THND_HA':
                    rice_th_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='RICE' and usa_temp['MEASURE'][l]=='THND_TONNE':
                    rice_th_t=usa_temp['Value'][l]

                if usa_temp['SUBJECT'][l]=='WHEAT' and usa_temp['MEASURE'][l]=='TONNE_HA':
                    WHEAT_t_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='WHEAT' and usa_temp['MEASURE'][l]=='THND_HA':
                    WHEAT_th_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='WHEAT' and usa_temp['MEASURE'][l]=='THND_TONNE':
                    WHEAT_th_t=usa_temp['Value'][l]

                if usa_temp['SUBJECT'][l]=='MAIZE' and usa_temp['MEASURE'][l]=='TONNE_HA':
                    MAIZE_t_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='MAIZE' and usa_temp['MEASURE'][l]=='THND_HA':
                    MAIZE_th_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='MAIZE' and usa_temp['MEASURE'][l]=='THND_TONNE':
                    MAIZE_th_t=usa_temp['Value'][l]

                if usa_temp['SUBJECT'][l]=='MAIZE' and usa_temp['MEASURE'][l]=='TONNE_HA':
                    MAIZE_t_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='MAIZE' and usa_temp['MEASURE'][l]=='THND_HA':
                    MAIZE_th_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='MAIZE' and usa_temp['MEASURE'][l]=='THND_TONNE':
                    MAIZE_th_t=usa_temp['Value'][l]

                if usa_temp['SUBJECT'][l]=='SOYBEAN' and usa_temp['MEASURE'][l]=='TONNE_HA':
                    SOYBEAN_t_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='SOYBEAN' and usa_temp['MEASURE'][l]=='THND_HA':
                    SOYBEAN_th_ha=usa_temp['Value'][l]
                if usa_temp['SUBJECT'][l]=='SOYBEAN' and usa_temp['MEASURE'][l]=='THND_TONNE':
                    SOYBEAN_th_t=usa_temp['Value'][l]
        
        #concat statment at end of each unique year loop to create new row 
        df_yield_temp=pd.DataFrame({'YEAR':[year],'RICE_TONNE_HA':[rice_t_ha],'RICE_THND_TONNE':[rice_th_t], 'RICE_THND_HA':[rice_th_ha],
                                                    'WHEAT_TONNE_HA':[WHEAT_t_ha],'WHEAT_THND_TONNE':[WHEAT_th_t], 'WHEAT_THND_HA':[WHEAT_th_ha],
                                                    'MAIZE_TONNE_HA':[MAIZE_t_ha],'MAIZE_THND_TONNE':[MAIZE_th_t], 'MAIZE_THND_HA':[MAIZE_th_ha],
                                                    'SOYBEAN_TONNE_HA':[SOYBEAN_t_ha],'SOYBEAN_THND_TONNE':[SOYBEAN_th_t], 'SOYBEAN_THND_HA':[SOYBEAN_th_ha]})

        df_yield=pd.concat([df_yield,df_yield_temp],ignore_index=True,axis=0)
        #make years our index
        df_yield.set_index('YEAR')
    return df_yield

out=pd.DataFrame(clean_yield(df))
out.to_csv('clean_production.csv')
print(out)


      