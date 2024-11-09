import time
import googlemaps
import pandas as pd
from bs4 import BeautifulSoup

"""Initialize Google Maps client."""
map_client = googlemaps.Client('AIzaSyAWiOY-X7t0I6uQ9tGF0t3D5KR0NpUAzJg')

def miles_to_meters(miles):
    """Convert miles to meters."""
    try:
        return miles * 1_609.344
    except TypeError:
        return 0

def get_coordinates(address):
    """Get coordinates for the address."""
    geocode = map_client.geocode(address=address)
    return geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng']

def search_businesses(address, search_string, distance):
    """Search for businesses."""
    print("searching for businesses")
    distance = miles_to_meters(distance)
    lat, lng = get_coordinates(address)
    business_list = []
    next_page_token = None

    while True:
        response = map_client.places(
            location=(lat, lng),
            query=search_string,
            radius=distance,
            page_token=next_page_token
        )
        
        business_list.extend(response.get('results', []))
        next_page_token = response.get('next_page_token')
        
        if not next_page_token:
            break
        
        time.sleep(2)  # Delay to respect API rate limits

    print(f"Total businesses found: {len(business_list)}")
    return business_list

def get_businesses_info(business_list, fields):
    """Get additional details for each business."""
    print("getting business info")
    updated_business_list = []
    for business in business_list:
        place_details = map_client.place(place_id=business['place_id'], fields=fields)
        temp_business = place_details['result']
        updated_business_list.append(temp_business)

    return updated_business_list