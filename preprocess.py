
THRESHOLD_MISSING = 5

def clean_FAOSTAT(df):
    #keep data only from FAO TIER 1 source, original data contains data for same year but from multiple sources
    #both sources have similar measurements
    #FAO TIER 1 is more complete than UNFCCC
    cleaned_df = df[df["Source Code"] == 3050] #FAO TIER 1
    #drop numeric codes that do not apply
    cleaned_df = cleaned_df.drop(['Area Code', 'Item Code', 'Source Code', 'Source', 'Element Code'], axis=1)
    #extract columns belonging to the USA
    cleaned_df = cleaned_df[cleaned_df['Area'] == 'United States of America']
    #rename Items column to Activity
    cleaned_df.rename(columns={'Item':'Activity'}, inplace=True)
    #reset the index
    cleaned_df = cleaned_df.reset_index(drop=True)
    return cleaned_df

#Clean up the emissions dataframe consisting of only emission activity/element and year
def create_emissions_frame(columns, df):
    df['Emission'] = df[columns[0]].astype(str) + '_' + df[columns[1]]
    df.drop(columns, axis=1, inplace=True)
    df.insert(0,'Emission', df.pop('Emission'))
    df = drop_year_no_data(df)
    df = df.set_index('Emission').transpose().fillna(0).reset_index()
    df['index'] = df['index'].str.lstrip('Y')
    return df.rename(columns={'index':'Year'}).set_index('Year')

#filter the emissions list to only contain the biggest contributers to argiculture
def list_emissions(emission_name, emission_activity_and_type):
    return list(filter(lambda emission: emission_name in emission[1],emission_activity_and_type))

#Because Area and Unit are the same value in every row (USA, Kilotonnes respectively), I will drop those. Set the column indicies to Activity
def create_emission_df(df, emission_list):
    return df[df['Element'].isin([el[1] for el in emission_list])].drop(['Area', 'Unit'], axis=1).reset_index(drop=True)

#drop columns where more than THRESHOLD_MISSING % of data is missing
def drop_year_no_data(df):
    #df columns currently are Year 19XX/2XXX
    for column in df:
        #if there is too much data missing for a particular year, drop it
        #initial check showed most data prior to 1990 is missing & is effectively being dropped
        if check_percent_data_missing(df[column]) > THRESHOLD_MISSING:
            df.drop(column, axis=1, inplace=True)
    return df

#check % of data missing in each column
def check_percent_data_missing(df):
    return df.isnull().sum()/df.shape[0] * 100

#a lot of data in set relates to emissions due to fires, keep emissions only related to agriculture
def keep_agriculture_data(df):
    columns_to_keep = []
    for column in df:
        if "agricult" in str(column).lower() or "farm" in str(column).lower():
            columns_to_keep.append(str(column))
    cleaned_df = df[columns_to_keep]
    return cleaned_df
