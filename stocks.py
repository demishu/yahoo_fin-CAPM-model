import pandas as pd
stocks = pd.read_table('stocks.txt', header=None)
stocks = stocks.iloc[:, 0].unique().tolist()