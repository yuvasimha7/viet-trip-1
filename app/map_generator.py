import folium
from math import atan2, degrees, radians, sin, cos



# Function to compute bearing between two points
'''def compute_bearing(coord1, coord2):
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)
    delta_lon = lon2 - lon1
    x = sin(delta_lon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon)
    bearing = atan2(x, y)
    return (degrees(bearing) + 360) % 360

# Function to compute midpoint between two coordinates
def midpoint(coord1, coord2):
    return [(coord1[0] + coord2[0]) / 2, (coord1[1] + coord2[1]) / 2]

# City coordinates
cities = {
    "Mumbai": [19.0760, 72.8777],
    "Hyderabad": [17.3850, 78.4867],
    "Kolkata": [22.5726, 88.3639],
    "Chennai": [13.0827, 80.2707],
    "Bangkok": [13.6849, 100.7449],
    "Pattaya": [12.9236, 100.8825],
    "Hanoi": [21.0278, 105.8342],
    "Sa Pa": [22.3371, 103.8448],
    "La Hang": [20.8609, 106.8190],
    "Ninh Binh": [20.2348, 105.9720]
}

# Adjusted Port Blair (150 km ≈ 1.35 degrees north)
port_blair_coords = [11.6234 + 1.35, 92.7265]  # ~150km north

# Compute map center
all_coords = list(cities.values()) + [port_blair_coords]
center_lat = sum(lat for lat, _ in all_coords) / len(all_coords)
center_lon = sum(lon for _, lon in all_coords) / len(all_coords)

# Create the map
m = folium.Map(location=[center_lat, center_lon], zoom_start=4, tiles='CartoDB positron')

# Add green 25 km circles with reduced opacity for layering clarity
for city, coords in cities.items():
    folium.Circle(
        location=coords,
        radius=25000,
        color='green',
        fill=True,
        fill_color='green',
        fill_opacity=0.1,  # Lower opacity for layering
        popup=city
    ).add_to(m)

# Add Leaflet.RotatedMarker plugin
rotated_marker_js = 'https://rawcdn.githack.com/bbecquet/Leaflet.RotatedMarker/master/leaflet.rotatedMarker.js'
m.get_root().html.add_child(folium.Element(f'<script src="{rotated_marker_js}"></script>'))

# Function to add a rotated airplane marker
def add_rotated_marker(map_obj, coord1, coord2):
    mid = midpoint(coord1, coord2)
    bearing = compute_bearing(coord1, coord2)
    # Adjust bearing if necessary, depending on the icon's default orientation
    adjusted_bearing = (bearing - 90) % 360
    icon = folium.Icon(icon='plane', prefix='fa', color='black')
    marker = folium.Marker(
        location=mid,
        icon=icon
    )
    # Add rotation angle to the marker's options
    marker.options = {**marker.options, 'rotationAngle': adjusted_bearing, 'rotationOrigin': 'center center'}
    map_obj.add_child(marker)

# Add red transparent dotted lines from Indian cities to Port Blair with rotated airplane markers
source_cities = ["Mumbai", "Hyderabad", "Kolkata", "Chennai"]
for city in source_cities:
    source = cities[city]
    folium.PolyLine(
        locations=[source, port_blair_coords],
        color='red',
        weight=3,
        opacity=0.4,
        dash_array='10, 10'
    ).add_to(m)
    add_rotated_marker(m, source, port_blair_coords)

# Port Blair to Bangkok (solid red line)
folium.PolyLine(
    locations=[port_blair_coords, cities["Bangkok"]],
    color='red',
    weight=3,
    opacity=0.4
).add_to(m)
add_rotated_marker(m, port_blair_coords, cities["Bangkok"])

# Bangkok to Hanoi (solid red line)
folium.PolyLine(
    locations=[cities["Bangkok"], cities["Hanoi"]],
    color='red',
    weight=3,
    opacity=0.4
).add_to(m)
add_rotated_marker(m, cities["Bangkok"], cities["Hanoi"])

# Save the map
m.save('static/map.html')'''

#use this when developing
def generate_map(output_path):
    # define everything inside this function
    def compute_bearing(coord1, coord2):
        lat1, lon1 = map(radians, coord1)
        lat2, lon2 = map(radians, coord2)
        delta_lon = lon2 - lon1
        x = sin(delta_lon) * cos(lat2)
        y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon)
        bearing = atan2(x, y)
        return (degrees(bearing) + 360) % 360

    def midpoint(coord1, coord2):
        return [(coord1[0] + coord2[0]) / 2, (coord1[1] + coord2[1]) / 2]

    cities = {
        "Mumbai": [19.0760, 72.8777],
        "Hyderabad": [17.3850, 78.4867],
        "Kolkata": [22.5726, 88.3639],
        "Chennai": [13.0827, 80.2707],
        "Bangkok": [13.6849, 100.7449],
        "Pattaya": [12.9236, 100.8825],
        "Hanoi": [21.0278, 105.8342],
        "Sa Pa": [22.3371, 103.8448],
        "La Hang": [20.8609, 106.8190],
        "Ninh Binh": [20.2348, 105.9720]
    }

    port_blair_coords = [11.6234 + 1.35, 92.7265]

    all_coords = list(cities.values()) + [port_blair_coords]
    center_lat = sum(lat for lat, _ in all_coords) / len(all_coords)
    center_lon = sum(lon for _, lon in all_coords) / len(all_coords)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4, tiles='CartoDB positron')

    for city, coords in cities.items():
        folium.Circle(
            location=coords,
            radius=25000,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.1,
            popup=city
        ).add_to(m)

    rotated_marker_js = 'https://rawcdn.githack.com/bbecquet/Leaflet.RotatedMarker/master/leaflet.rotatedMarker.js'
    m.get_root().html.add_child(folium.Element(f'<script src="{rotated_marker_js}"></script>'))

    def add_rotated_marker(map_obj, coord1, coord2):
        mid = midpoint(coord1, coord2)
        bearing = compute_bearing(coord1, coord2)
        adjusted_bearing = (bearing - 90) % 360
        icon = folium.Icon(icon='plane', prefix='fa', color='black')
        marker = folium.Marker(
            location=mid,
            icon=icon
        )
        marker.options = {**marker.options, 'rotationAngle': adjusted_bearing, 'rotationOrigin': 'center center'}
        map_obj.add_child(marker)

    source_cities = ["Mumbai", "Hyderabad", "Kolkata", "Chennai"]
    for city in source_cities:
        source = cities[city]
        folium.PolyLine(
            locations=[source, port_blair_coords],
            color='red',
            weight=3,
            opacity=0.4,
            dash_array='10, 10'
        ).add_to(m)
        add_rotated_marker(m, source, port_blair_coords)

    folium.PolyLine(
        locations=[port_blair_coords, cities["Bangkok"]],
        color='red',
        weight=3,
        opacity=0.4
    ).add_to(m)
    add_rotated_marker(m, port_blair_coords, cities["Bangkok"])

    folium.PolyLine(
        locations=[cities["Bangkok"], cities["Hanoi"]],
        color='red',
        weight=3,
        opacity=0.4
    ).add_to(m)
    add_rotated_marker(m, cities["Bangkok"], cities["Hanoi"])

    m.save(output_path)