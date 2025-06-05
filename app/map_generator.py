import folium
from math import atan2, degrees, radians, sin, cos
import os


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

    # Add road route waypoints for more realistic routing
    def add_road_route(map_obj, start_coords, end_coords, waypoints=None, color='blue', weight=4, opacity=0.7, dash_array=None):
        """Add a road route line with optional waypoints"""
        if waypoints:
            route_coords = [start_coords] + waypoints + [end_coords]
        else:
            route_coords = [start_coords, end_coords]
        
        folium.PolyLine(
            locations=route_coords,
            color=color,
            weight=weight,
            opacity=opacity,
            dash_array=dash_array,
            popup=f"Road Route"
        ).add_to(map_obj)
        
        


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
        "Ninh Binh": [20.2470, 105.9836]
    }

    # Add specific locations for better routing
    specific_locations = {
        "Suvarnabhumi Airport": [13.6900, 100.7501],  # BKK Airport
        "Pattaya Train Station": [12.9300, 100.8850]   # Approximate location
    }

    # Sublocation data
    sublocations = {
        "sapa": {
            "fansipan_mountain": [22.3322, 103.8354],
            "cat_cat_village": [22.3300, 103.8327],
            "ta_phin_village": [22.3913, 103.8399],
            "moana_sapa": [22.3272, 103.8459],
            "alpine_coaster": [22.3223, 103.8666]
        },
        "ninh_binh": {
            "tam_coc": [20.2184, 105.9179],
            "hang_mua_cave": [20.2304, 105.9371],
            "bai_dinh_pagoda": [20.2774, 105.8648],
            "bich_dong_pagoda": [20.2175, 105.9157],
            "bird_park": [20.2164, 105.9017]
        },
        "hanoi": {
            "old_quarter": [21.0339, 105.8505],
            "night_street": [21.0314, 105.8531],
            "temple_of_literature": [21.0279, 105.8357],
            "prison_museum": [21.0251, 105.8464],
            "mausoleum": [21.03667, 105.8349]
        },
        "pattaya": {
            "sanctuary_of_truth": [12.9274, 100.8892],
            "walking_street": [12.9262, 100.8729],
            "ko_lan": [12.9142, 100.7829]
        }
    }

    port_blair_coords = [11.6234 + 1.35, 92.7265]

    all_coords = list(cities.values()) + [port_blair_coords] + list(specific_locations.values())
    center_lat = sum(lat for lat, _ in all_coords) / len(all_coords)
    center_lon = sum(lon for _, lon in all_coords) / len(all_coords)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    # Add circles for cities with special handling for Bangkok
    for city, coords in cities.items():
        if city == "Bangkok":
            # Special popup for Bangkok with airport information
            bangkok_popup = folium.Popup(
                html="""
                <div style="font-family: Arial, sans-serif; width: 250px;">
                    <h3 style="margin: 0; color: #2c3e50;"><b>Bangkok</b></h3>
                    <hr style="margin: 5px 0;">
                    <h4 style="margin: 5px 0; color: #34495e;">Suvarnabhumi Airport (BKK)</h4>
                    <p style="margin: 5px 0; font-size: 12px;">
                        <b>IATA Code:</b> BKK<br>
                        <b>ICAO Code:</b> VTBS<br>
                        <b>Location:</b> Racha Thewa, Bang Phli District<br>
                        <b>Elevation:</b> 5 ft (1.5 m)<br>
                        <b>Opened:</b> September 28, 2006<br>
                        <b>Hub for:</b> Thai Airways, Bangkok Airways<br>
                        <b>Passengers/year:</b> ~65 million (pre-2020)<br>
                        <b>Runways:</b> 2 (3,700m and 4,000m)
                    </p>
                </div>
                """,
                max_width=300
            )
            
            # Custom tooltip for Bangkok
            bangkok_tooltip = """
            <div style="font-family: Arial, sans-serif; text-align: center;">
                <div style="font-weight: bold; font-size: 14px;">Bangkok</div>
                <div style="font-size: 11px; color: #666;">Click for more information</div>
            </div>
            """
            
            # Reduced Bangkok circle radius to 15km
            folium.Circle(
                location=coords,
                radius=15000,
                color='green',
                fill=True,
                fill_color='green',
                fill_opacity=0.1,
                popup=bangkok_popup,
                tooltip=folium.Tooltip(bangkok_tooltip, permanent=False)
            ).add_to(m)
        else:
            folium.Circle(
                location=coords,
                radius=25000,
                color='green',
                fill=True,
                fill_color='green',
                fill_opacity=0.1,
                popup=city
            ).add_to(m)

    # Add markers for specific locations
    '''for location_name, coords in specific_locations.items():
        icon_color = 'red' if 'Airport' in location_name else 'blue' if 'Bus' in location_name else 'orange'
        icon_name = 'plane' if 'Airport' in location_name else 'bus' if 'Bus' in location_name else 'train'
        
        folium.Marker(
            location=coords,
            popup=location_name,
            tooltip=location_name,
            icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa')
        ).add_to(m)'''

    # Add sublocation circles (1km radius, violet color)
    for location_group, places in sublocations.items():
        for place_name, coords in places.items():
            # Format place name for display
            display_name = place_name.replace('_', ' ').title()
            
            folium.Circle(
                location=coords,
                radius=1000,  # 1km radius
                color='violet',
                fill=True,
                fill_color='violet',
                fill_opacity=0.2,
                popup=f"{display_name} ({location_group.title()})",
                tooltip=display_name
            ).add_to(m)

    # Add Font Awesome for icons
    font_awesome_css = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'
    m.get_root().html.add_child(folium.Element(font_awesome_css))
    
    rotated_marker_js = 'https://rawcdn.githack.com/bbecquet/Leaflet.RotatedMarker/master/leaflet.rotatedMarker.js'
    m.get_root().html.add_child(folium.Element(f'<script src="{rotated_marker_js}"></script>'))

    def add_rotated_marker(map_obj, coord1, coord2, icon_type="plane"):
        mid = midpoint(coord1, coord2)
        bearing = compute_bearing(coord1, coord2)
        adjusted_bearing = (bearing - 90) % 360
        
        # Create icon based on type
        if icon_type == "plane":
            icon_class = "fa-plane"
            color = "black"
        elif icon_type == "car":
            icon_class = "fa-car"
            color = "black"
        elif icon_type == "bus":
            icon_class = "fa-bus"
            color = "blue"
        elif icon_type == "train":
            icon_class = "fa-train"
            color = "orange"
        else:
            icon_class = "fa-plane"
            color = "black"
        
        # Create rotated icon
        plane_html = f'''
        <div style="
            width: 20px; 
            height: 20px; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            transform: rotate({adjusted_bearing}deg);
            transform-origin: center center;
        ">
            <i class="fa {icon_class}" style="
                font-size: 16px; 
                color: {color};
            "></i>
        </div>
        '''
        
        icon = folium.DivIcon(
            html=plane_html,
            icon_size=(20, 20),
            icon_anchor=(10, 10)
        )
        
        marker = folium.Marker(
            location=mid,
            icon=icon
        )
        map_obj.add_child(marker)

    # Original flight routes
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
        add_rotated_marker(m, source, port_blair_coords, "plane")

    folium.PolyLine(
        locations=[port_blair_coords, cities["Bangkok"]],
        color='red',
        weight=3,
        opacity=0.4
    ).add_to(m)
    add_rotated_marker(m, port_blair_coords, cities["Bangkok"], "plane")

    folium.PolyLine(
        locations=[cities["Bangkok"], cities["Hanoi"]],
        color='red',
        weight=3,
        opacity=0.4
    ).add_to(m)
    add_rotated_marker(m, cities["Bangkok"], cities["Hanoi"], "plane")

    # NEW: Add road route from Suvarnabhumi Airport to Pattaya Train Station
    # Please provide your coordinates - using placeholder coordinates for now
    road_waypoints = [
        [13.7313, 100.8051],  # Replace with your coordinates
        [13.7342, 100.8056],  # Replace with your coordinates  
        [13.6728, 100.8394],   # Replace with your coordinates
        [13.5930,100.9638],
        [13.4955,101.0464],
        [13.3922,101.0464],
        [13.2987,100.9945],
        [13.2576,100.9903],
        [13.2145,101.0056],
        [13.1523,100.9866],
        [13.0038,100.9934],
        [12.9592,100.9739],
        [12.9447,100.9047],
        [12.9183,100.8969]
    ]
    
    add_road_route(
        m, 
        specific_locations["Suvarnabhumi Airport"], 
        specific_locations["Pattaya Train Station"],
        waypoints=road_waypoints,
        color='blue',
        weight=4,
        opacity=0.8
    )
    
    # Add black car symbol on the road route
    #car_position = midpoint(specific_locations["Suvarnabhumi Airport"], specific_locations["Pattaya Train Station"])
    #add_rotated_marker(m, specific_locations["Suvarnabhumi Airport"], specific_locations["Pattaya Train Station"], "car")

    
    #m.get_root().html.add_child(folium.Element(legend_html))

    m.save(output_path)


def generate_sublocation_maps(base_output_dir):
    """Generate individual maps for each sublocation"""
    
    # Sublocation data
    sublocations = {
        "sapa": {
            "center": [22.3371, 103.8448],  # Use original Sa Pa coordinates as center
            "places": {
                "fansipan_mountain": [22.3322, 103.8354],
                "cat_cat_village": [22.3300, 103.8327],
                "ta_phin_village": [22.3913, 103.8399],
                "moana_sapa": [22.3272, 103.8459],
                "alpine_coaster": [22.3223, 103.8666]
            }
        },
        "ninh_binh": {
            "center": [20.2470, 105.9836],  # Use original Ninh Binh coordinates as center
            "places": {
                "tam_coc": [20.2184, 105.9179],
                "hang_mua_cave": [20.2304, 105.9371],
                "bai_dinh_pagoda": [20.2774, 105.8648],
                "bich_dong_pagoda": [20.2175, 105.9157],
                "bird_park": [20.2164, 105.9017]
            }
        },
        "hanoi": {
            "center": [21.0278, 105.8342],  # Use original Hanoi coordinates as center
            "places": {
                "old_quarter": [21.0339, 105.8505],
                "night_street": [21.0314, 105.8531],
                "temple_of_literature": [21.0279, 105.8357],
                "prison_museum": [21.0251, 105.8464],
                "mausoleum": [21.03667, 105.8349]
            }
        },
        "pattaya": {
            "center": [12.9236, 100.8825],  # Use original Pattaya coordinates as center
            "places": {
                "sanctuary_of_truth": [12.9274, 100.8892],
                "walking_street": [12.9262, 100.8729],
                "ko_lan": [12.9142, 100.7829]
            }
        }
    }
    
    # Create sublocation directory if it doesn't exist
    sublocation_dir = os.path.join(base_output_dir, "sublocation")
    os.makedirs(sublocation_dir, exist_ok=True)
    
    for location_name, location_data in sublocations.items():
        # Create individual location directory
        location_dir = os.path.join(sublocation_dir, location_name)
        os.makedirs(location_dir, exist_ok=True)
        
        # Create map centered on the location
        center_coords = location_data["center"]
        m = folium.Map(location=center_coords, zoom_start=12)
        
        # Add violet circles for each place (1km radius)
        for place_name, coords in location_data["places"].items():
            display_name = place_name.replace('_', ' ').title()
            
            folium.Circle(
                location=coords,
                radius=1000,  # 1km radius
                color='violet',
                fill=True,
                fill_color='violet',
                fill_opacity=0.2,
                popup=f"{display_name}",
                tooltip=display_name
            ).add_to(m)
            
            # Add a marker for better visibility
            folium.Marker(
                location=coords,
                popup=display_name,
                tooltip=display_name,
                icon=folium.Icon(color='purple', icon='info-sign')
            ).add_to(m)
        
        # Save the map
        output_file = os.path.join(location_dir, f"{location_name}_map.html")
        m.save(output_file)
        print(f"Generated map for {location_name}: {output_file}")


# Example usage:
if __name__ == "__main__":
    # Generate main map
    generate_map("main_map.html")
    
    # Generate sublocation maps
    generate_sublocation_maps("maps")