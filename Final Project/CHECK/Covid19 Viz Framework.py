#%%
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from folium.plugins import StripePattern
import streamlit as st
from streamlit_folium import folium_static

page = st.radio(
    "Select map type", ["Single map", "Dual map", "Branca figure"], index = 0
)

#%%
# Reading Shapefile
world_map = gpd.read_file("D:/GitHub/kavak_lab/Twitter Project outside GitHub/world-administrative-boundaries/world-administrative-boundaries.shp")

#%%
# Reading Covid Data
covid_data = pd.read_csv ('D:\GitHub\kavak_lab\Twitter Project outside GitHub\COVID-19 Cases.csv')
# We have covid data from one source and the shapefile from another.
# Between these sources, we need country names to join them before we can generate geo-plots.
# However, these two sources have some mismatch that we are handling manually so that we can join them.
#covid_data.iloc[85017]['Country_Region'] = 'United States of America'
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
# An helper section to ID the max values for confirmed cases and deaths during the entire timeframe
date = np.unique(np.array(list(covid_data['Date'])))
#country = np.unique(np.array(list(covid_data['Country_Region'])))
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
            if(world_map_country_name[c]=='West Bank and Gaza'):
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
                countConfirmed_wb = int(countConfirmed/5*3)
                countDeaths_wb = int(countDeaths/5*3)
                each_date_df = each_date_df.append({"name":"West Bank", "countConfirmed":countConfirmed_wb, "countDeaths":countDeaths_wb}, ignore_index=True)
                countConfirmed_g = countConfirmed - countConfirmed_wb
                countDeaths_g = countDeaths - countDeaths_wb
                each_date_df = each_date_df.append({"name":"Gaza Strip", "countConfirmed":countConfirmed_g, "countDeaths":countDeaths_g}, ignore_index=True)
            else:
                each_date_df = each_date_df.append({"name":world_map_country_name[c], "countConfirmed":0, "countDeaths":0}, ignore_index=True)

    datewise_data[date[d]] = each_date_df
    print('Completed:', d,'/',len(date))

#%%
# Finding out max of confirmed and death cases per day for the entire period
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
#Using 'Cook Islands' to uniform color in between diff. days.
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
#Folium to make the map interactive
d = '3/29/2020'
merged_data = world_map.merge(datewise_data[d], on="name")
my_map = folium.Map(location=[42, 0], zoom_start=2.5)

folium.Choropleth(
    geo_data = merged_data,
    name = 'COVID 19 Spread',
    data = merged_data,
    columns = ['name', 'countConfirmed'],
    key_on = 'feature.properties.name',
    fill_color = 'Oranges',
    fill_opacity = 0.7,
    line_opacity = 0.2,
    legend_name = '# of Patients',
    smooth_factor=0,
    Highlight= True,
    line_color = "#000000",
    show=True,
    overlay=True,
    nan_fill_color = "White"
).add_to(my_map)

################
# Here we add cross-hatching (crossing lines) to display the Null values.
nans = merged_data[merged_data["countConfirmed"].isnull()]['name'].values
gdf_nans = merged_data[merged_data['name'].isin(nans)]
sp = StripePattern(angle=45, color='black', space_color='black', line_color = "black", weight = 2, space_weight = 2, line_weight = 0, space_opacity = 0.75, line_opacity = 0.75)
sp.add_to(my_map)
folium.features.GeoJson(name="Unreported",data=gdf_nans, style_function=lambda x :{'fillPattern': sp},show=True).add_to(my_map)


#Hover
# Add hover functionality.
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
NIL = folium.features.GeoJson(
    data = merged_data,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['name','countConfirmed', 'countDeaths'],
        aliases=['Country','Confirmed Cases', 'Deaths'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
my_map.add_child(NIL)
my_map.keep_in_front(NIL)
#sample_map2

loc = 'Distribution of COVID-19 Daily Confirmed Cases '+'('+d+')'
title_html = '''
             <h3 align="center" style="font-size:32px"><b>{}</b></h3>
             '''.format(loc)
my_map.get_root().html.add_child(folium.Element(title_html))



# Add dark and light mode. 
folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(my_map)
folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(my_map)




# We add a layer controller. 
folium.LayerControl(collapsed=False).add_to(my_map)
################


my_map.save('confirmed.html')
folium_static(my_map)

#%%
import pickle

with open('datewise_data.pickle', 'wb') as f:
    pickle.dump(datewise_data, f)
    
with open('world_map.pickle', 'wb') as f:
    pickle.dump(world_map, f)

#%%
with open('datewise_data.pickle', 'rb') as handle:
    b = pickle.load(handle)
    
with open('world_map.pickle', 'rb') as handle:
    c = pickle.load(handle)
    
print(c)























