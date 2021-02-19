# A module providing simple functions that will simplfy 
# the narative of my Google Colab notebooks.
date_of_last_edit = '2021-02-19'

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
    return("tja_modules is loaded\nVersion: {date_of_last_edit}")



