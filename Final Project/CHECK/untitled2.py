import pandas as pd
import folium
import geopandas


# The URL we will read our data from
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_meat_consumption'
# read_html returns a list of tables from the URL
tables = pd.read_html(url)

# The data is in the first table - this changes from time to time - wikipedia is updated all the time.
table = tables[0]

# Read the geopandas dataset
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# Merge the two DataFrames together
table = world.merge(table, how="left", left_on=['name'], right_on=['Country'])

# Clean data: remove rows with no data
table = table.dropna(subset=['kg/person (2002)[9][note 1]'])

# Create a map
my_map = folium.Map(location=[42, 0], zoom_start=2.5)

# Add the data
folium.Choropleth(
    geo_data=table,
    name='choropleth',
    data=table,
    columns=['name','kg/person (2002)[9][note 1]'],
    key_on='feature.properties.Country',
    fill_color='OrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Meat consumption in kg/person',
    smooth_factor=0,
    Highlight= True,
    line_color = "#000000",
    #name = "Wills",
    show=False,
    overlay=True,
    nan_fill_color = "White"
).add_to(my_map)

'''
# Movable Legend
# We import the required library:
from branca.element import Template, MacroElement

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legend (draggable!)</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:white;opacity:0.7;'></span>Countries that have Null values.</li>
    

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

my_map.get_root().add_child(macro)
'''

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
    data = table,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['name','kg/person (2002)[9][note 1]'],
        aliases=['Country','Consumption'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
my_map.add_child(NIL)
my_map.keep_in_front(NIL)
#sample_map2

# Add dark and light mode. 
folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(my_map)
folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(my_map)

# We add a layer controller. 
folium.LayerControl(collapsed=False).add_to(my_map)


my_map.save('meat.html')