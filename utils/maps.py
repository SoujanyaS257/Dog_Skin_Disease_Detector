import folium
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two points on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371.0 # Radius of Earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def get_nearby_clinics(user_lat, user_lon):
    """
    Returns a DataFrame of mock vet clinics sorted by distance to the user.
    In a real app, this would query an API like Google Places.
    """
    # Expanded Mock Data covering major areas in Bengaluru
    vet_data = {
        'Name': [
            # --- NEW: RT Nagar (Near Hebbal) ---
            'Govt Veterinary Hospital (RT Nagar)',
            'Pet Life Clinic (RT Nagar)',

            # Hebbal & North Bangalore
            'Cessna Pet Hospital (Hebbal)', 
            'Bangalore Pet Hospital (Hebbal)',
            'Precise Pet Clinic (Sahakara Nagar)',
            'Hebbal Veterinary Clinic',

            # Indiranagar & East Bangalore
            'Cessna Pet Hospital (Domlur)',
            'Cartman Animal Hospital (Koramangala)',
            'V-Care Pet Polyclinic (Koramangala)',
            'Pet Zone Veterinary Clinic (Whitefield)',
            'The Pet Clinic (Indiranagar)',

            # South Bangalore (Jayanagar/JP Nagar)
            'Jayanagar Veterinary Hospital',
            'Marvelous Pet Clinic (JP Nagar)',
            'Sanchaya Pet Clinic (Banashankari)',

            # West Bangalore (Malleshwaram/Rajajinagar)
            'Malleshwaram Pet Clinic',
            'Rajajinagar Veterinary Hospital',
            'Canine Care Clinic (Vijayanagar)'
        ],
        'Latitude': [
            # --- RT Nagar Coords ---
            13.0245, 13.0198,

            # North
            13.0358, 13.0285, 13.0623, 13.0392,
            # East
            12.9645, 12.9345, 12.9312, 12.9716, 12.9784,
            # South
            12.9250, 12.9067, 12.9183,
            # West
            13.0031, 12.9815, 12.9724
        ],
        'Longitude': [
            # --- RT Nagar Coords ---
            77.5962, 77.5940,

            # North
            77.5970, 77.5895, 77.5906, 77.5932,
            # East
            77.6385, 77.6245, 77.6210, 77.7499, 77.6408,
            # South
            77.5938, 77.5856, 77.5732,
            # West
            77.5643, 77.5532, 77.5321
        ],
        'Info': [
            # --- RT Nagar Info ---
            'Affordable vaccinations & care',
            'General checkups & grooming',

            # North Info
            '24/7 Emergency & Critical Care',
            'General checkups & Surgery',
            'Specialized Dermatology Care',
            'Government Vet Clinic',
            # East Info
            'Full-service hospital',
            'Holistic pet care',
            'Skin & coat specialists',
            'Emergency services available',
            'Vaccinations & wellness',
            # South Info
            'Government hospital, affordable',
            'Advanced diagnostics',
            'General practice',
            # West Info
            'Surgery & X-Ray',
            'Government Vet Services',
            'Pet grooming & clinic'
        ]
    }
    df = pd.DataFrame(vet_data)
    
    # Calculate distance for each clinic
    df['Distance_km'] = df.apply(
        lambda row: haversine_distance(user_lat, user_lon, row['Latitude'], row['Longitude']), 
        axis=1
    )
    
    # Sort by nearest
    df = df.sort_values(by='Distance_km').reset_index(drop=True)
    return df

def create_vet_map(user_lat, user_lon):
    """
    Creates a Folium map centered on the user's location with nearby vet clinics.
    """
    # Zoom level 11 shows a wider area (increasing visible distance)
    m = folium.Map(location=[user_lat, user_lon], zoom_start=11, tiles="OpenStreetMap")

    # Add user location marker (Blue)
    folium.Marker(
        [user_lat, user_lon], 
        popup="<strong>You are Here</strong>", 
        icon=folium.Icon(color="blue", icon="user", prefix='fa')
    ).add_to(m)
    
    # Get nearby clinics
    nearby_clinics = get_nearby_clinics(user_lat, user_lon)

    # Add clinic markers (Red)
    for idx, row in nearby_clinics.iterrows():
        # Create a popup with info and distance
        popup_html = f"""
        <div style="width:200px">
            <strong>{row['Name']}</strong><br>
            {row['Info']}<br>
            <hr>
            <em>Distance: {row['Distance_km']:.2f} km</em>
        </div>
        """
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['Name']} ({row['Distance_km']:.1f} km)",
            icon=folium.Icon(color='red', icon='fa-solid fa-house-medical', prefix='fa')
        ).add_to(m)
        
    return m