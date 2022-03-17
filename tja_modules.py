# A module providing simple functions that will simplfy 
# the narative of my Google Colab notebooks.
last_update = '2022-03-07 version 3'

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

def pickle_to_google_drive(df, pickle_file_name):
    """Pickle a DataFrame to Google Drive"""
    from google.colab import drive

    drive.mount('/content/drive', force_remount=True)
    pickle_path = '/content/drive/MyDrive/Data Sets'
    pickle_path = pickle_path + '/' + pickle_file_name
    df.to_pickle(pickle_path)

    print(f"Data saved to: {pickle_path}.")

def load_pickle_from_google_drive(pickle_file_name):
    """Load pickle in Google Drive to Pandas DF or return False"""
    import pandas as pd
    from pathlib import Path
    from google.colab import drive

    drive.mount('/content/drive', force_remount=True)
    pickle_path = '/content/drive/MyDrive/Data Sets'
    pickle_path = pickle_path + '/' + pickle_file_name

    if Path(pickle_path).is_file():
      print(f"Data exists in Google Drive.\nImporting from:\n{pickle_path}.")
      df = pd.read_pickle(pickle_path)
      return(df)
    else:
      print(f"Data DOES NOT exist in Google Drive.\nReturning: False")
      return(False)



"""
BBC Football Data Modules
"""


def bbc_form_summary(bbc_league_table):
    '''
    Accept a list of a team's recent form scraped 
    from the 'Form' columns of footbal league tables 
    on the BBC website. 
      Return a summary of the recent form.
    '''
    form_list = bbc_league_table.split('.')
    form_summary = ""
    for i in form_list:
        if 'DDrew' in i:
            form_summary = form_summary + 'D'
        elif 'WWon' in i:
            form_summary = form_summary + 'W'
        elif 'LLost' in i:
            form_summary = form_summary + 'L'    
    return(form_summary)

def bbc_form_points(bbc_league_table):
    '''
    Accept a list of a team's recent form scraped 
    from the 'Form' columns of footbal league tables 
    on the BBC website. 
    Return a the number of points earned from the 
    recent form.
    '''
    form_list = bbc_league_table.split('.')
    #  form_list = bbc_league_table.loc[0].split('.')
    form_points = 0
    for i in form_list:
        if 'DDrew' in i:
            form_points = form_points + 1
        elif 'WWon' in i:
            form_points = form_points + 3
    return(form_points)



""" 
UK Government COVID Data Modules
"""

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






