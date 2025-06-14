# Import necessary modules
from maps import *
from emails import *
from sheets import *

# Define search parameters
address = 'Madison Wisconsin, USA' # where to search
search_string = 'local restraunts' # what type of business to search for
radius_miles = 1 # will search in an x mile radius around the address
fields = ['place_id', 'name', 'formatted_address', 'rating', 'user_ratings_total', 'website', "formatted_phone_number"] # will put the following data fields into the spreadsheet

# Search for businesses based on parameters
business_list = search_businesses(address, search_string, radius_miles)

# Get additional information for each business
businesses_info = get_businesses_info(business_list, fields)

# Retrieve email addresses for businesses
# UNCOMMENT IF NEEDED
# businesses_list_with_emails = get_business_emails(businesses_info)

# Create and save the results to a dataframe with emails
# create_and_save_dataframe(businesses_list_with_emails, search_string, address)

# Create and save the results to a dataframe without emails
create_and_save_dataframe(businesses_info, search_string, address)