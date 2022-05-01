#%%
# import relevant package(s)
import geopandas as gpd
import pandas as pd
import numpy as np


#%%
# read Shapefile
world_map = gpd.read_file("../Assignments/Assignment5_6_8_9_10_11_12/Data/Shapefile_World/world-administrative-boundaries.shp")


#%%
# read Covid Data
covid_data = pd.read_csv ('../Assignments/Assignment5_6_8_9_10_11_12/Data/COVID-19 Cases.csv')
# we have covid data from one source and the shapefile from another.
# between these sources, we need country names to join them before we can generate geo-plots.
# however, these two sources have some mismatch that we are handling manually so that we can join them.
# covid_data.iloc[85017]['Country_Region'] = 'United States of America'
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Antigua and Barbuda", "Antigua & Barbuda")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Bosnia and Herzegovina", "Bosnia & Herzegovina")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Brunei", "Brunei Darussalam")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Burma", "Myanmar")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Cabo Verde", "Cape Verde")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Congo \(Brazzaville\)", "Congo")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Congo \(Kinshasa\)", "Democratic Republic of the Congo")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Cote d'Ivoire", "CÃ´te d'Ivoire")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Czechia", "Czech Republic")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Eswatini", "Swaziland")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Iran", "Iran (Islamic Republic of)")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Korea, South", "Republic of Korea")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Kosovo", "Serbia")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Laos", "Lao People's Democratic Republic")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Libya", "Libyan Arab Jamahiriya")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Moldova", "Moldova, Republic of")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("North Macedonia", "The former Yugoslav Republic of Macedonia")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Russia", "Russian Federation")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Syria", "Syrian Arab Republic")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Taiwan\*", "Taiwan")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("Tanzania", "United Republic of Tanzania")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("US", "United States of America")
covid_data['Country_Region'] = covid_data['Country_Region'].str.replace("United Kingdom", "U.K. of Great Britain and Northern Ireland")

#%%
# helper section to ID the max values for confirmed cases and deaths during the entire timeframe
date = np.unique(np.array(list(covid_data['Date'])))
world_map_country_name = list(world_map['name'])
world_map_country_name.sort()
datewise_data = {}
for d in range(0, len(date)):
    column_names = ["name", "countConfirmed", "countDeaths"]
    each_date_df = pd.DataFrame(columns = column_names)
    for c in range(0, len(world_map_country_name)):
        if(world_map_country_name[c] in list(covid_data['Country_Region'])):
            countConfirmed = int(np.nansum(
                covid_data.loc[(covid_data['Case_Type']=='Confirmed')
               & (covid_data['Date']==date[d]) 
               & (covid_data['Country_Region']==world_map_country_name[c])]['Cases']
                ))
            countDeaths = int(np.nansum(
                covid_data.loc[(covid_data['Case_Type']=='Deaths')
               & (covid_data['Date']==date[d]) 
               & (covid_data['Country_Region']==world_map_country_name[c])]['Cases']
                ))
            each_date_df = each_date_df.append({"name":world_map_country_name[c], "countConfirmed":countConfirmed, "countDeaths":countDeaths}, ignore_index=True)
            
        else:
            if(world_map_country_name[c]=='West Bank'):
                countConfirmed = int(np.nansum(
                    covid_data.loc[(covid_data['Case_Type']=='Confirmed')
                   & (covid_data['Date']==date[d])
                   & (covid_data['Country_Region']=='West Bank and Gaza')]['Cases']
                    ))
                countDeaths = int(np.nansum(
                    covid_data.loc[(covid_data['Case_Type']=='Deaths')
                   & (covid_data['Date']==date[d])
                   & (covid_data['Country_Region']=='West Bank and Gaza')]['Cases']
                    ))
                countConfirmed_wb = int(countConfirmed/5*3)
                countDeaths_wb = int(countDeaths/5*3)
                each_date_df = each_date_df.append({"name":"West Bank", "countConfirmed":countConfirmed_wb, "countDeaths":countDeaths_wb}, ignore_index=True)
                
            elif (world_map_country_name[c]=='Gaza Strip'):
                countConfirmed = int(np.nansum(
                    covid_data.loc[(covid_data['Case_Type']=='Confirmed')
                   & (covid_data['Date']==date[d])
                   & (covid_data['Country_Region']=='West Bank and Gaza')]['Cases']
                    ))
                countDeaths = int(np.nansum(
                    covid_data.loc[(covid_data['Case_Type']=='Deaths')
                   & (covid_data['Date']==date[d])
                   & (covid_data['Country_Region']=='West Bank and Gaza')]['Cases']
                    ))
                countConfirmed_wb = int(countConfirmed/5*3)
                countDeaths_wb = int(countDeaths/5*3)
                countConfirmed_g = countConfirmed - countConfirmed_wb
                countDeaths_g = countDeaths - countDeaths_wb
                each_date_df = each_date_df.append({"name":"Gaza Strip", "countConfirmed":countConfirmed_g, "countDeaths":countDeaths_g}, ignore_index=True)
            else:
                each_date_df = each_date_df.append({"name":world_map_country_name[c], "countConfirmed":0, "countDeaths":0}, ignore_index=True)
    datewise_data[date[d]] = each_date_df
    print('Completed:', d,'/',len(date))

#%%
# calculate max of confirmed and death cases per day for the entire period
maxCountConfirmed = 0
maxCountDeaths = 0
for d in date:
    maxVal = max(datewise_data[d]['countConfirmed'])
    if(maxVal>maxCountConfirmed):
        maxCountConfirmed = maxVal
    maxVal = max(datewise_data[d]['countDeaths'])
    if(maxVal>maxCountDeaths):
        maxCountDeaths = maxVal
print(maxCountConfirmed, maxCountDeaths)

#%%
# use 'Cook Islands' to uniform color in between diff. days.
date = np.unique(np.array(list(covid_data['Date'])))
country = np.unique(np.array(list(covid_data['Country_Region'])))
world_map_country_name = list(world_map['name'])
world_map_country_name.sort()
datewise_data = {}
for d in range(0, len(date)):
    column_names = ["name", "countConfirmed", "countDeaths"]
    each_date_df = pd.DataFrame(columns = column_names)
    for c in range(0, len(world_map_country_name)):
        if(world_map_country_name[c] in list(covid_data['Country_Region'])):
            countConfirmed = int(np.nansum(
                covid_data.loc[(covid_data['Case_Type']=='Confirmed')
               & (covid_data['Date']==date[d]) 
               & (covid_data['Country_Region']==world_map_country_name[c])]['Cases']
                ))
            countDeaths = int(np.nansum(
                covid_data.loc[(covid_data['Case_Type']=='Deaths')
               & (covid_data['Date']==date[d]) 
               & (covid_data['Country_Region']==world_map_country_name[c])]['Cases']
                ))
            each_date_df = each_date_df.append({"name":world_map_country_name[c], "countConfirmed":countConfirmed, "countDeaths":countDeaths}, ignore_index=True)
            
        else:
            if(world_map_country_name[c]=='West Bank'):
                countConfirmed = int(np.nansum(
                    covid_data.loc[(covid_data['Case_Type']=='Confirmed')
                   & (covid_data['Date']==date[d])
                   & (covid_data['Country_Region']=='West Bank and Gaza')]['Cases']
                    ))
                countDeaths = int(np.nansum(
                    covid_data.loc[(covid_data['Case_Type']=='Deaths')
                   & (covid_data['Date']==date[d])
                   & (covid_data['Country_Region']=='West Bank and Gaza')]['Cases']
                    ))
                countConfirmed_wb = int(countConfirmed/5*3)
                countDeaths_wb = int(countDeaths/5*3)
                each_date_df = each_date_df.append({"name":"West Bank", "countConfirmed":countConfirmed_wb, "countDeaths":countDeaths_wb}, ignore_index=True)
                
            elif (world_map_country_name[c]=='Gaza Strip'):
                countConfirmed = int(np.nansum(
                    covid_data.loc[(covid_data['Case_Type']=='Confirmed')
                   & (covid_data['Date']==date[d])
                   & (covid_data['Country_Region']=='West Bank and Gaza')]['Cases']
                    ))
                countDeaths = int(np.nansum(
                    covid_data.loc[(covid_data['Case_Type']=='Deaths')
                   & (covid_data['Date']==date[d])
                   & (covid_data['Country_Region']=='West Bank and Gaza')]['Cases']
                    ))
                countConfirmed_wb = int(countConfirmed/5*3)
                countDeaths_wb = int(countDeaths/5*3)
                countConfirmed_g = countConfirmed - countConfirmed_wb
                countDeaths_g = countDeaths - countDeaths_wb
                each_date_df = each_date_df.append({"name":"Gaza Strip", "countConfirmed":countConfirmed_g, "countDeaths":countDeaths_g}, ignore_index=True)
            elif (world_map_country_name[c]=='Cook Islands'):
                each_date_df = each_date_df.append({"name":world_map_country_name[c], "countConfirmed":maxCountConfirmed, "countDeaths":maxCountDeaths}, ignore_index=True)
            else:
                each_date_df = each_date_df.append({"name":world_map_country_name[c], "countConfirmed":float("nan"), "countDeaths":float("nan")}, ignore_index=True)
            
    datewise_data[date[d]] = each_date_df
    print('Completed:', d,'/',len(date))
    

#%%
# dump datewise_data and world_map data using pickle
import pickle

with open('Data_Backup/datewise_data.pickle', 'wb') as f:
    pickle.dump(datewise_data, f)
    
with open('Data_Backup/world_map.pickle', 'wb') as f:
    pickle.dump(world_map, f)

with open('Data_Backup/date.pickle', 'wb') as f:
    pickle.dump(date, f)