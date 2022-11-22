def clean_FAOSTAT(df):
    #drop numeric codes that do not apply
    cleaned_df = df.drop(['Area Code', 'Item Code', 'Source Code', 'Source', 'Element Code'], axis=1)
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
    df = df.set_index('Emission').transpose().fillna(0).reset_index()
    df['index'] = df['index'].str.lstrip('Y')
    return df.rename(columns={'index':'Year'}).set_index('Year')

#filter the emissions list to only contain the biggest contributers to argiculture
def list_emissions(emission_name, emission_activity_and_type):
    return list(filter(lambda emission: emission_name in emission[1],emission_activity_and_type))

#Because Area and Unit are the same value in every row (USA, Kilotonnes respectively), I will drop those. Set the column indicies to Activity
def create_emission_df(df, emission_list):
    return df[df['Element'].isin([el[1] for el in emission_list])].drop(['Area', 'Unit'], axis=1).reset_index(drop=True)

def clean_other_one():
    pass

def combine():
    pass

def visualize():
    pass

def convert_units():
    pass

def drop_na():
    pass
