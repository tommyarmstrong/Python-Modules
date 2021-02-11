def one_hot_encode(df, cols):
	import pandas as pd
	# Encode columns of categorical data
	# Prefix the new column names with the original column name
	# Drop one of the resulting columns to minimise columns overall
	# Drop the original column
	for col in cols:
		df = pd.concat([df, pd.get_dummies(df[col], prefix=col, drop_first=True)], axis=1).drop([col], axis=1)
		print(f"One-hot encoded {col}")
	return(df)

def split_data(df, label, train_col):
	# Split into train and test data and drop the "Train" column
	y_train = df[df[train_col] == 1][label]
	y_test = df[df[train_col] == 0][label]
	x_train = df[df[train_col] == 1].drop([label], axis=1)
	x_test = df[df[train_col] == 0].drop([label], axis=1)
	return(x_train, y_train, x_test, y_test)

def test_module_load():
	return("tja_modules is loaded")



