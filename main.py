from preprocess import *
from model import *
import pandas as pd

df = pd.read_csv('FAOSTAT_data_1961_2019.csv')
cleaned_df = clean_FAOSTAT(df)

#create an emission activity and emission type list. Each value is a tuple, 0th -> activity, 1st -> type of emission
emission_activity_and_type = list(cleaned_df.groupby(['Activity','Element']).indices.keys())

'''Anthropogenic climate change is caused by multiple climate pollutants, with CO2, CH4, and N2O the three largest individual contributors to global warming. Agriculture and food production is associated with all three of these gases, but direct agricultural emissions are unusual in being dominated by CH4 and N2O.'''

#filter the emissions list to only contain the biggest contributers to argiculture
CO2_gas_list = list_emissions("CO2", emission_activity_and_type)
CH4_gas_list = list_emissions("CH4", emission_activity_and_type)
N2O_gas_list = list_emissions("N2O", emission_activity_and_type)

#Because Area and Unit are the same value in every row (USA, Kilotonnes respectively), I will drop those. Set the column indicies to Activity
CO2_df = create_emission_df(cleaned_df, CO2_gas_list)
CH4_df = create_emission_df(cleaned_df, CH4_gas_list)
N2O_df = create_emission_df(cleaned_df, N2O_gas_list)

#filter the emissions list to only contain the biggest contributers to argiculture
CO2_df = create_emissions_frame(['Activity', 'Element'], CO2_df)
CH4_df = create_emissions_frame(['Activity', 'Element'], CH4_df)
N2O_df = create_emissions_frame(['Activity', 'Element'], N2O_df)

#drop highly correlated features
CO2_df = drop_correlations(CO2_df)
CH4_df = drop_correlations(CH4_df)
N2O_df = drop_correlations(N2O_df)

#the features that remain are not related to forests and fires but agrivulture
#all features have a correlation less than abs(THRESHOLD_CORRELATION)
CO2_df = remove_fire_data(CO2_df)
CH4_df = remove_fire_data(CH4_df)
N2O_df = remove_fire_data(N2O_df)

#import crop yields data
prod_amt=pd.read_csv('clean_production.csv')
prod_amt.drop(columns=['Unnamed: 0'],inplace=True)
prod_amt.rename(columns={"YEAR":"Year"},inplace=True)
prod_amt['Year']=prod_amt['Year'].astype("str")

#CO2 and crop yields
#merge the two df
drop_columns_CO2 = 'Year_x'
crops_CO2_df = merge_df(prod_amt, CO2_df, drop_columns_CO2)
#augment the data since it has one entry per year between 1990 and 2016
crops_CO2_augmented = augment_df(crops_CO2_df)
#select features for CO2
features_CO2 = ["On-farm energy use_Emissions (CO2)",                        
				"IPCC Agriculture_Emissions (CO2eq) (AR5)",       
				"Emissions on agricultural land_Emissions (CO2)", 
				"Farm-gate emissions_Emissions (CO2eq) (AR5)"]
#labels apply to all models
labels_all = ['RICE_TONNE_HA',
			  'WHEAT_TONNE_HA',
			  'MAIZE_TONNE_HA',
			  'SOYBEAN_TONNE_HA']
#build linear regression model for crop yields and CO2
crops_CO2_score, crops_CO2_mse, crops_CO2_mrse = run_model(crops_CO2_df, features_CO2, labels_all)
print("Crops_CO2_r^2_score = ", crops_CO2_score, 
	  "Crops_CO2_mse = ", crops_CO2_mse, 
	  "Crops_CO2_mrse = ", crops_CO2_mrse)

#crop yields and CH4
#merge crop yield and CH4
drop_columns_CH4 = ["Year_x", "Year_y"]
crops_CH4_df = merge_df(prod_amt, CH4_df, drop_columns_CH4)
#augment data frame since it has one entry per years 1990-2016
crops_CH4_augmented = augment_df(crops_CH4_df)
#select features sepecific to CH4
features_CH4 = ["Enteric Fermentation_Emissions (CH4)",    
				"Manure Management_Emissions (CH4)",
				"On-farm energy use_Emissions (CH4)" ]
#build linear regression model
crops_CH4_score, crops_CH4_mse, crops_CH4_mrse = run_model(crops_CH4_df, features_CH4, labels_all)
print("Crops_CH4_r^2_score = ", crops_CH4_score, 
	  "Crops_CH4_mse = ", crops_CH4_mse, 
	  "Crops_CH4_mrse = ", crops_CH4_mrse)

#crop yields and N2O
#merge crop yields and N20
drop_columns_N2O = ["Year_x", "Year_y"]
crops_N2O_df = merge_df(prod_amt, N2O_df, drop_columns_N2O)
#augment data frame since it has one entry per years 1990-2016
crops_N2O_augmented = augment_df(crops_N2O_df)
#select features specific to N2O
features_N2O = ['Manure Management_Emissions (N2O)',
				'Synthetic Fertilizers_Direct emissions (N2O)',
				'On-farm energy use_Emissions (N2O)',
				'Manure applied to Soils_Direct emissions (N2O)',
				'Crop Residues_Direct emissions (N2O)',
				'Drained organic soils (N2O)_Emissions (N2O)',
				'IPCC Agriculture_Direct emissions (N2O)']
#build linear regression model for N2O
crops_N2O_score, crops_N2O_mse, crops_N2O_mrse = run_model(crops_N2O_df, features_N2O, labels_all)
print("Crops_N2O_r^2_score = ", crops_N2O_score, 
	  "Crops_N2O_mse = ", crops_N2O_mse, 
	  "Crops_N2O_mrse = ", crops_N2O_mrse)