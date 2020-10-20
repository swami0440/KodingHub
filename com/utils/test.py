import pandas as pd

d = {"2019-05-02 10:00:11": 10, "2019-05-02 11:00:11": 15,"2019-06-03 11:00:11": 20 }
df = pd.DataFrame(d.items(),columns=['Date', 'Value'])
df['date1'] = pd.to_datetime(df['Date'],format="")
df.drop(columns= ['Date'],inplace=True)

df['date_minus_time'] = df["date1"].apply(lambda df : pd.datetime.datetime(year=df.year, month=df.month, day=df.day))


#df=pd.to_datetime(df['Date_da'])
#df = df.set_index('Date_da')
print(df.dtypes)
print(df.groupby('date_minus_time')['Value'].sum())

#g = df.groupby(pd.Grouper(freq="M"))  # DataFrameGroupBy (grouped by Month)
#print(df.dtypes)
#df.groupby(['Date_da']).sum
#df = df.resample('M').mean()

#print({k.split()[0] : v  for (k,v) in d.items()})


#new = list[d.items()]

#print(new)