
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
import io
import calendar
from datetime import datetime
from fbprophet import Prophet
import os

def get_forecast_surface_change_plot_as_bytes():
    # Read in the raw temperature and emissions datasets (they are in CSV format) 
    raw_t = pd.read_csv('./Temp.csv', skiprows=1)
    # Create new dataframe with an index for each month
    # First create the date range
    date_rng = pd.date_range(start='1/1/1880', end='1/03/2019', freq='M')
    #print(date_rng[0])
    #print(type(date_rng[5]))
    # Next create the empty DataFrame, which we will populate using the actual data
    t = pd.DataFrame(date_rng, columns=['date'])
    # Create a column for the anomoly values
    t['Avg_Anomaly_deg_C'] = None
    #Set the index of the DataFrame to the date column (DateTime index)
    t.set_index('date', inplace=True)
    #print(t.head())
    # We only want the monthly data, lets only select that and leave out the seasonal columns
    raw_t = raw_t.iloc[:,:13]
    #raw_t.head()
    # Apply function to each row of raw data 
    _ = raw_t.apply(lambda row: populate_df_with_anomolies_from_row(row,t), axis=1)

    # Apply above function to all anomaly values in DataFrame
    t['Avg_Anomaly_deg_C'] = t['Avg_Anomaly_deg_C'].apply(lambda raw_value: clean_anomaly_value(raw_value))
    # 'Forward fill' to take care of NaN values
    t.fillna(method='ffill', inplace=True)
    # Import Matplotlib
    import matplotlib.pyplot as plt
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()

    # Create a new DataFrame with which we will create/train our Prophet model 
    t_prophet = pd.DataFrame()
    t_prophet['ds'] = t.index
    t_prophet['y'] = t['Avg_Anomaly_deg_C'].values
    
    # Instantiate model and fit to data (just like with sklearn model API)
    m = Prophet()
    m.fit(t_prophet)

    # Generate future dataframe containing predictions (we are doing this for 20 years into the future)
    future = m.make_future_dataframe(freq='m', periods=81*12, include_history=True)
    forecast = m.predict(future)

    return forecast[['ds','yhat']]

def populate_df_with_anomolies_from_row(row,t):
    year = row['Year']
    # Anomaly values (they seem to be a mixture of strings and floats)
    monthly_anomolies = row.iloc[1:]
    # Abbreviated month names (index names)
    months = monthly_anomolies.index
    for month in monthly_anomolies.index:
        # Get the last day for each month 
        last_day = calendar.monthrange(year,datetime.strptime(month, '%b').month)[1]
        # construct the index with which we can reference our new DataFrame (to populate) 
        date_index = datetime.strptime(f'{year} {month} {last_day}', '%Y %b %d')
        # Populate / set value @ above index, to anomaly value
        t.loc[date_index] = monthly_anomolies[month]

def clean_anomaly_value(raw_value):
    try:
        return float(raw_value)
    except:
        return np.NaN

def convertToCSV():
    # df1 = get_forecast_surface_change_plot_as_bytes() 
    # print(df1.tail())   
    # df1.to_csv('predictTemp.csv')
    # print("completed temp predict")
    df2 = get_global_forecast_carbon_dioxide_change_plot_as_bytes()
    print(df2.tail(12))   
    df2.to_csv('predictCo2.csv')

    print("completed Co2 predict")




def get_global_forecast_carbon_dioxide_change_plot_as_bytes():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_world = raw_e[raw_e['Country Name']=='World'].loc[:,'1960':'2018']
    raw_e_world = raw_e_world.T
    raw_e_world.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    world = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    world_v = world.apply(lambda row: populate_df_world(row,raw_e_world), axis=1)
    world['Global CO2 Emissions per Capita'] = world_v
    world.set_index('date', inplace=True)
    world.fillna(method='ffill', inplace=True)
    world[world.index.year>2011]
    world_resampled = world.resample('A').mean()
    #fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    #ax.plot(world, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    #ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='Global CO2 Emission over Time')
    # Enable grid
    #ax.grid()
    world_prophet = pd.DataFrame()
    world_prophet['ds'] =world.index
    world_prophet['y'] = world['Global CO2 Emissions per Capita'].values
    m = Prophet(daily_seasonality=False,weekly_seasonality=False,yearly_seasonality=False)
    m.fit(world_prophet)
    future = m.make_future_dataframe(freq='m', periods=82*12, include_history=True)
    forecast = m.predict(future)

    return forecast[['ds','yhat']]
    


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_world(row,raw_e_world):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_world.loc[index]
    return value
    
convertToCSV()
# get_global_forecast_carbon_dioxide_change_plot_as_bytes()
