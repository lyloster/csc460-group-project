from preprocess import *
import pandas as pd

#open
df = pd.read_csv('FAOSTAT_data_1961_2019.csv')
cleaned_df = clean_FAOSTAT(df)
print(cleaned_df.head())

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

print(CO2_df.columns)
print(CO2_df.head())
print(CH4_df.columns)
