# A module providing simple functions that will simplfy 
# the narative of my Google Colab notebooks.
last_update = '2021-02-19'

def one_hot_encode(df, cols):
    import pandas as pd
    # Encode columns of categorical data
    # Prefix the new column names with the original column name
    # Drop one of the resulting columns to minimise columns overall
    # Drop the original column
    for col in cols:
        df = pd.concat([df, pd.get_dummies(df[col], prefix=col, drop_first=True)], axis=1).drop([col], axis=1)
        print(f"One-hot encoded: {col}")
    return(df)

def split_data(df, label, train_col):
    # Split into train and test data and drop the "Train" column
    y_train = df[df[train_col] == 1][label]
    y_test = df[df[train_col] == 0][label]
    x_train = df[df[train_col] == 1].drop([label], axis=1).drop([train_col], axis=1)
    x_test = df[df[train_col] == 0].drop([label], axis=1).drop([train_col], axis=1)
    return(x_train, y_train, x_test, y_test)

def scale_data(df, cols):
    # Scale data in a pandas data frame
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    df[cols] = scaler.fit_transform(df[cols])
    for col in cols:
        print(f"Scaled: {col}")
    return(df)

def drop_columns(df, cols):
    # Drop columns that are not required
  for col in cols:
    df.drop([col], axis=1, inplace=True)
    print(f"Dropped column: {col}")
  return df

def test_module_load():
    print(f"tja_modules is loaded\nVersion: {last_update} ")

def load_local_json_file(file_name):
    if os.path.isfile(file_name):
        with open(file_name) as f:
            data = json.load(f) 
        return(data) 

def save_data_to_json_file(data, file_name):
    """Save data to JSON file"""
    with open(file_name, 'w') as f:
            json.dump(data, f) 

""" UK Government COVID Data Modules"""

def load_data(metrics, area_type):
    """Load data either from online source or locally cached JSON"""
    data_format = 'json'
    cache_file = f"data/uk_covid_data_{area_type.upper()}.{data_format}"
    data_source = 'https://api.coronavirus.data.gov.uk'

    if os.path.isfile(cache_file):
        # Use locally cached data if available
        #print(f"Area: {area_name}...Loading cached data from {cache_file}...")
        with open(cache_file) as f:
            data = json.load(f)   

    else:
        # Download new data if no local cache available
        print(f"Area Type: {area_type.title()}")
        print(f"...Loading new data from {data_source}")
        
        url = self._create_api_v2_call(data_format, metrics, area_type)
        print("...API version: v2")
        response = get(url, timeout=10)
        if response.status_code >= 400:
            raise RuntimeError(f'Request failed: { response.text }')
        #print(f"...Server Response... {response.status_code}")
        data = response.json()
        # Cache the data locally
        print(f"...Saving data to disk at {cache_file}...")
        self._save_data_to_file(data, cache_file) 

    return(data)


    def create_api_v2_call(data_format, metrics, area_type, *area_name):
        """Create the URL to download from the UK Government API v2 """
        filters_and_format = {
                'areaType': area_type,
                'format': data_format
                }   
        # If area name is provided add it to the URL
        # If no area name is provided the API will return data for all areas 
        if area_name:
            area_name = area_name[0]
            filters_and_format['areaName'] = area_name
        
        encoded_filters_and_format = urlencode(filters_and_format, quote_via=urllib.parse.quote)

        data_structure = []
        for metric in metrics:
            data_structure.append(f"metric={metric}")
        data_structure_str = str.join('&', data_structure)
        
        api_params = encoded_filters_and_format + "&" + data_structure_str
        endpoint = self.settings.uk_data_url + "/v2/data/?" + api_params
        return(endpoint)






