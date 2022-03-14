import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.ensemble import RandomForestRegressor

temp = pd.read_csv('sealevel.csv')
temp = temp[["Year","GMSL_noGIA"]]
df = pd.DataFrame(columns = ['Year', 'Sea Height Variation'])
count = 0
value = 0
for i in range(temp.shape[0]):
    value += temp.iloc[i][1]
    count += 1
    if (i > 0 and temp.iloc[i][0] != temp.iloc[i-1][0]):
        value -= temp.iloc[i][1]
        df = df.append({'Year' : temp.iloc[i-1][0], 'Sea Height Variation': value / count}, ignore_index=True)
        count = 0
        value = temp.iloc[i][1]
df = df.append({'Year' : temp.iloc[-1][0], 'Sea Height Variation' : value / count}, ignore_index=True)

model = RandomForestRegressor()
#model.fit(df.iloc[:,0], df.iloc[:,1])

print(df.tail())
plt.figure(figsize=(10,8))
plt.title("Sea Levels over time")
plt.xlabel("Year")
plt.ylabel("Sea Height Variation (mm)")
plt.plot(df.iloc[:,0],df.iloc[:,1])
plt.savefig("plot.png")
print(df.head())