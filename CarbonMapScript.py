import folium
import pandas as pd

# Create a folium map
map = folium.Map(location = [38.58,-99.09], zoom_start = 6, titles = "Stamen Terrain")

# Import city locations as a CSV
allCities = pd.read_csv("worldcities.csv")

cityCarbonTot = pd.read_csv("GGMCF_top500cities.txt", sep = '\t')

allCities = allCities[allCities.population > 100000].merge(cityCarbonTot, on = ["city_ascii", 'country'], how = 'right')

# Labels required: city, lat, lng, capital, population, country, Global ranking, Domestic ranking, (t CO2), (Mt CO2), Footprint/cap, Footprint

# Separate the cities by whether or not they are a capital
capitalCities = allCities.dropna()[['city', 'lat','lng','capital','population','country','Global ranking','Domestic ranking','Footprint/cap (t CO2)','Footprint (Mt CO2)','admin_name']]
majorCities = allCities[allCities['capital'].isna()]
majorCities = majorCities[['city', 'lat','lng','population','country','Global ranking','Domestic ranking','Footprint/cap (t CO2)','Footprint (Mt CO2)','admin_name']].dropna()

print(capitalCities)
print(majorCities)

# Create FeatureGroup
fg = folium.FeatureGroup(name = "My Map")

# Define the HTML the popup
htmlCapital = """
<b>City info:</b> <br>
Country: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Administration Area: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Name: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Type of Capital: %s <br>
Population: %s <br><br>

<b>Carbon Data:</b> <br>
Total Carbon Footprint (Mt of CO2): %s <br>
Carbon Footprint per Capita (t of CO2): %s <br>
Global Ranking: %s <br>
Domestic Ranking: %s
"""

htmlCity = """
<b>City Info:</b> <br>
Country: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Administration Area: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Name: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Population: %s <br><br>

<b>Carbon Data:</b> <br>
Total Carbon Footprint (Mt of CO2): %s <br>
Carbon Footprint per Capita (t of CO2): %s <br>
Global Ranking: %s <br>
Domestic Ranking: %s
"""

# Add all capitals to the map
index = 0
for lat, lon, name, capitalType, population, country, adminName, totFoot, footPerCap, gRank, dRank in zip(capitalCities['lat'], capitalCities['lng'], capitalCities['city'], capitalCities['capital'], capitalCities['population'], capitalCities['country'], capitalCities['admin_name'],
                                                                                                        capitalCities['Footprint (Mt CO2)'], capitalCities['Footprint/cap (t CO2)'], capitalCities['Global ranking'], capitalCities['Domestic ranking']):
    iframe = folium.IFrame(html = htmlCapital % (country, country, adminName, adminName, name, name, capitalType.title(), population, totFoot, footPerCap, gRank, dRank), width = 375, height = 250)
    popup = folium.Popup(iframe)
    if gRank <= 100:
        fg.add_child(folium.CircleMarker(location = [lat, lon], popup = popup, color = 'red', fill = True, fill_opacity = 0.7, radius = 6))
    elif 100 < gRank <= 300:
        fg.add_child(folium.CircleMarker(location = [lat, lon], popup = popup, color = 'orange', fill = True, fill_opacity = 0.7, radius = 6))
    else: 
        fg.add_child(folium.CircleMarker(location = [lat, lon], popup = popup, color = 'green', fill = True, fill_opacity = 0.7, radius = 6))

# Add all other cities
index = 0
for lat, lon, name, population, country, adminName, totFoot, footPerCap, gRank, dRank in zip(majorCities['lat'], majorCities['lng'], majorCities['city'], majorCities['population'], majorCities['country'], majorCities['admin_name'],
                                                                                            majorCities['Footprint (Mt CO2)'], majorCities['Footprint/cap (t CO2)'], majorCities['Global ranking'], majorCities['Domestic ranking']):
    iframe = folium.IFrame(html = htmlCity % (country, country, adminName, adminName, name, name, population, totFoot, footPerCap, gRank, dRank), width = 375, height = 220)
    popup = folium.Popup(iframe)
    if gRank <= 100:
        fg.add_child(folium.CircleMarker(location = [lat, lon], popup = popup, color = 'red', fill = True, fill_opacity = 0.7, radius = 6))
    elif 100 < gRank <= 300:
        fg.add_child(folium.CircleMarker(location = [lat, lon], popup = popup, color = 'orange', fill = True, fill_opacity = 0.7, radius = 6))
    else: 
        fg.add_child(folium.CircleMarker(location = [lat, lon], popup = popup, color = 'green', fill = True, fill_opacity = 0.7, radius = 6))

# # Add a GeoJson
# fg.add_child(folium.GeoJson(data = (open('countries.geo.json'))))

# Plot the points in the FeatureGroup
map.add_child(fg)

# Save map
map.save("CarbonMap.html")