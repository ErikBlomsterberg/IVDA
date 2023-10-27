import pandas as pd

df = pd.read_csv('./Data/zurich.csv')  

print('\n', df.iloc[:, : 9].head(5))
print('\n', df.iloc[:, -9:].head(5))

 