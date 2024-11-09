import pandas as pd

def create_and_save_dataframe(updated_business_list, search_string, address):
    """
    Create DataFrame and save to Excel.
    
    Args:
    updated_business_list (list): List of dictionaries containing business information.
    search_string (str): The search query used to find businesses.
    address (str): The address around which the search was performed.
    
    Returns:
    None. Saves the DataFrame to an Excel file.
    """
    # Create DataFrame from the list of businesses
    df = pd.DataFrame(updated_business_list)
    
    # Add a URL column for easy access to Google Maps
    df['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df['place_id']
    
    # Generate a filename based on the search parameters
    output_filename = f"{search_string.replace(' ', '')}_{address.replace(' ', '')}.xlsx"
    
    # Save the DataFrame to an Excel file
    df.to_excel(output_filename, index=False)
    
    # Print a confirmation message
    print(f"Results saved to {output_filename}")
