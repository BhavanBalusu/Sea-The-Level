import pandas as pd
#import matplotlib
#matplotlib.use('Agg')
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




def get_surface_change_plot():
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

    # Create figure, title and plot resampled data
    plt.figure(figsize=(10,8))
    plt.title("Temperature Anomaly Data Resampled by Mean")
    plt.xlabel('Time')
    plt.ylabel('Temperature Mean Anomaly (°Celsius)')
    plt.plot(t.resample('A').mean(), color='#1C7C54', linewidth=1.0)
    plt.savefig("Temperature.png")

def get_forecast_surface_change_plot():
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
    future = m.make_future_dataframe(freq='m', periods=80*12, include_history=True)
    forecast = m.predict(future)
    #print(forecast)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))

    # Plot the resulting forecast
    m.plot(forecast)
    #temp_cv = cross_validation(m, horizon = '365 days')
    #temp_p = performance_metrics(temp_cv)
    #print(temp_p.head(5))
    plt.title("Temperature Anomaly Forecast", fontsize=10)
    plt.xlabel("Years", fontsize=10)
    plt.ylabel("Temperature Anomaly (°Celsius)", fontsize=10)
    plt.savefig("TempPredict.png")
    
    
    


# Function definition
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



# Import Numpy, as library meant for large arrays - we will use it that we 
import numpy as np

# Define function to convert values to floats, and return a 'NaN = Not a Number' if this is not possible
def clean_anomaly_value(raw_value):
    try:
        return float(raw_value)
    except:
        return np.NaN



def get_global_carbon_dioxide_change_plot():
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
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(world, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='Global CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    plt.savefig("carbon.png")
    


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_world(row,raw_e_world):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_world.loc[index]
    return value

def get_global_forecast_carbon_dioxide_change_plot():
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
    future = m.make_future_dataframe(freq='m', periods=31*12, include_history=True)
    forecast = m.predict(future)
    m.plot(forecast)
    plt.title("Forecasted Values for CO2 Emissions per Capita for World")
    plt.xlabel("Time (years)")
    plt.ylabel("Emissions (Metric Tons per Capita)")
    plt.savefig("carbonPredict.png")
    


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_world(row,raw_e_world):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_world.loc[index]
    return value

def get_usa_carbon_dioxide_change_plot():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_usa = raw_e[raw_e['Country Name']=='United States'].loc[:,'1960':'2018']
    raw_e_usa = raw_e_usa.T
    raw_e_usa.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    usa = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    usa_v = usa.apply(lambda row: populate_df_usa(row,raw_e_usa), axis=1)
    usa['Global CO2 Emissions per Capita'] = usa_v
    usa.set_index('date', inplace=True)
    usa.fillna(method='ffill', inplace=True)
    usa[usa.index.year>2011]
    usa_resampled = usa.resample('A').mean()
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(usa_resampled, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='USA CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    plt.savefig("USA.png")
    


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_usa(row,raw_e_usa):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_usa.loc[index]
    return value

def get_china_carbon_dioxide_change_plot():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_china = raw_e[raw_e['Country Name']=='China'].loc[:,'1960':'2018']
    raw_e_china = raw_e_china.T
    raw_e_china.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    china = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    china_v = china.apply(lambda row: populate_df_china(row,raw_e_china), axis=1)
    china['Global CO2 Emissions per Capita'] = china_v
    china.set_index('date', inplace=True)
    china.fillna(method='ffill', inplace=True)
    china[china.index.year>2011]
    china_resampled = china.resample('A').mean()
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(china_resampled, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='China CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    plt.savefig("China.png")
    


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_china(row,raw_e_china):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_china.loc[index]
    return value

def get_india_carbon_dioxide_change_plot():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_india = raw_e[raw_e['Country Name']=='India'].loc[:,'1960':'2018']
    raw_e_india = raw_e_india.T
    raw_e_india.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    india = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    india_v = india.apply(lambda row: populate_df_india(row,raw_e_india), axis=1)
    india['Global CO2 Emissions per Capita'] = india_v
    india.set_index('date', inplace=True)
    india.fillna(method='ffill', inplace=True)
    india[india.index.year>2011]
    india_resampled = india.resample('A').mean()
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(india_resampled, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='India CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    
    plt.savefig("India.png")


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_india(row,raw_e_india):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_india.loc[index]
    return value

def get_uk_carbon_dioxide_change_plot():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_uk = raw_e[raw_e['Country Name']=='United Kingdom'].loc[:,'1960':'2018']
    raw_e_uk = raw_e_uk.T
    raw_e_uk.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    uk = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    uk_v = uk.apply(lambda row: populate_df_uk(row,raw_e_uk), axis=1)
    uk['Global CO2 Emissions per Capita'] = uk_v
    uk.set_index('date', inplace=True)
    uk.fillna(method='ffill', inplace=True)
    uk[uk.index.year>2011]
    uk_resampled = uk.resample('A').mean()
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(uk_resampled, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='United Kingdom CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    plt.savefig("UK.png")


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_uk(row,raw_e_uk):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_uk.loc[index]
    return value
    
def get_australia_carbon_dioxide_change_plot():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_australia = raw_e[raw_e['Country Name']=='Australia'].loc[:,'1960':'2018']
    raw_e_australia = raw_e_australia.T
    raw_e_australia.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    australia = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    australia_v = australia.apply(lambda row: populate_df_australia(row,raw_e_australia), axis=1)
    australia['Global CO2 Emissions per Capita'] = australia_v
    australia.set_index('date', inplace=True)
    australia.fillna(method='ffill', inplace=True)
    australia[australia.index.year>2011]
    australia_resampled = australia.resample('A').mean()
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(australia_resampled, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='Australia CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    plt.savefig("Australia.png")


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_australia(row,raw_e_australia):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_australia.loc[index]
    return value

def get_japan_carbon_dioxide_change_plot():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_japan = raw_e[raw_e['Country Name']=='Japan'].loc[:,'1960':'2018']
    raw_e_japan = raw_e_japan.T
    raw_e_japan.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    japan = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    japan_v = japan.apply(lambda row: populate_df_japan(row,raw_e_japan), axis=1)
    japan['Global CO2 Emissions per Capita'] = japan_v
    japan.set_index('date', inplace=True)
    japan.fillna(method='ffill', inplace=True)
    japan[japan.index.year>2011]
    japan_resampled = japan.resample('A').mean()
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(japan_resampled, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='Japan CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    plt.savefig("Japan.png")


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_japan(row,raw_e_japan):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_japan.loc[index]
    return value

def get_germany_carbon_dioxide_change_plot():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_germany = raw_e[raw_e['Country Name']=='Germany'].loc[:,'1960':'2018']
    raw_e_germany = raw_e_germany.T
    raw_e_germany.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    germany = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    germany_v = germany.apply(lambda row: populate_df_germany(row,raw_e_germany), axis=1)
    germany['Global CO2 Emissions per Capita'] = germany_v
    germany.set_index('date', inplace=True)
    germany.fillna(method='ffill', inplace=True)
    germany[germany.index.year>2011]
    germany_resampled = germany.resample('A').mean()
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(germany_resampled, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='Germany CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    plt.savefig("Germany.png")


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_germany(row,raw_e_germany):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_germany.loc[index]
    return value

def get_nigeria_carbon_dioxide_change_plot():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_nigeria = raw_e[raw_e['Country Name']=='Nigeria'].loc[:,'1960':'2018']
    raw_e_nigeria = raw_e_nigeria.T
    raw_e_nigeria.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    nigeria = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    nigeria_v = nigeria.apply(lambda row: populate_df_nigeria(row,raw_e_nigeria), axis=1)
    nigeria['Global CO2 Emissions per Capita'] = nigeria_v
    nigeria.set_index('date', inplace=True)
    nigeria.fillna(method='ffill', inplace=True)
    nigeria[nigeria.index.year>2011]
    nigeria_resampled = nigeria.resample('A').mean()
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(nigeria_resampled, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='Nigeria CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    plt.savefig("Nigeria.png")


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_nigeria(row,raw_e_nigeria):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_nigeria.loc[index]
    return value    

def get_brazil_carbon_dioxide_change_plot():
    raw_e = pd.read_csv('./API_EN.ATM.CO2E.PC_DS2_en_csv_v2_713061.csv', skiprows=3)
    raw_e_brazil = raw_e[raw_e['Country Name']=='Brazil'].loc[:,'1960':'2018']
    raw_e_brazil = raw_e_brazil.T
    raw_e_brazil.columns = ['value']
    date_rng = pd.date_range(start='31/12/1960', end='31/12/2018', freq='y')
    brazil = pd.DataFrame(date_rng, columns=['date'])
    # Populate the new DataFrame using the values from the raw data slice
    brazil_v = brazil.apply(lambda row: populate_df_brazil(row,raw_e_brazil), axis=1)
    brazil['Global CO2 Emissions per Capita'] = brazil_v
    brazil.set_index('date', inplace=True)
    brazil.fillna(method='ffill', inplace=True)
    brazil[brazil.index.year>2011]
    brazil_resampled = brazil.resample('A').mean()
    fig, ax = plt.subplots(figsize=(10,8))
    # Plot co2 emissions data with specific colour and line thickness
    ax.plot(brazil_resampled, color='#3393FF', linewidth=2.5)
    # Set axis labels and graph title
    ax.set(xlabel='Time (years)', ylabel='Emissions (Metric Tons per Capita)', title='Brazil CO2 Emissions over Time')
    # Enable grid
    ax.grid()
    plt.savefig("Brazil.png")


# Define function to pull value from raw data, using DateIndex from new DataFrame row
def populate_df_brazil(row,raw_e_brazil):
    #print(row)
    index = str(row['date'].year)
    value = raw_e_brazil.loc[index]
    return value

def get_carbon_offset_plot():
    objects = ('World', 'India', 'China', 'United Kingdom', 'United States', 'Nigeria', 'Brazil', 'Australia', 'Japan', 'Germany')
    y_pos = np.arange(len(objects))
    number_of_trees = [5000,156,584,105,995,18,49,58,157,132]
    plt.subplots(figsize=(20,8))
    plt.bar(y_pos, number_of_trees, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xlabel('Country')
    plt.ylabel('Tree Offset (millions of trees)')
    plt.title('Tree Offset for Countries')
    plt.savefig("carbonOffset.png")


get_surface_change_plot()
get_forecast_surface_change_plot()
get_global_carbon_dioxide_change_plot()
get_global_forecast_carbon_dioxide_change_plot()
get_usa_carbon_dioxide_change_plot()
get_china_carbon_dioxide_change_plot()
get_india_carbon_dioxide_change_plot()
get_uk_carbon_dioxide_change_plot()
get_australia_carbon_dioxide_change_plot()
get_japan_carbon_dioxide_change_plot()
get_germany_carbon_dioxide_change_plot()
get_nigeria_carbon_dioxide_change_plot()
get_brazil_carbon_dioxide_change_plot()
get_carbon_offset_plot()