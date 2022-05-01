#%%
import pickle
#import folium
#from folium.plugins import StripePattern
#import streamlit as st
#from streamlit_folium import folium_static

#%%
with open('Data_Backup/datewise_data.pickle', 'rb') as handle:
    datewise_data = pickle.load(handle)


#%%    
with open('Data_Backup/world_map.pickle', 'rb') as handle:
    world_map = pickle.load(handle)


#%%    
#print(world_map['name'])
#print(datewise_data)

#Folium to make the map interactive
d = '3/29/2020'
merged_data = world_map.merge(datewise_data[d], on="name")
my_map = folium.Map(location=[42, 0], zoom_start=1)

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
folium.features.GeoJson(name="Unreported",data=gdf_nans, style_function=lambda x :{'fillPattern': sp},show=False).add_to(my_map)


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


#my_map.save('confirmed.html')
with c1:
    folium_static(my_map)
with c2:
    folium_static(my_map)
    
