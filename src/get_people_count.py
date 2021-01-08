import sys
import pandas as pd

data_df = pd.read_csv(sys.argv[1], header=None)
print(len(data_df[1].unique()))
