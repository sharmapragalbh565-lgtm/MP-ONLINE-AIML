import requests
import os

print("Fetching data from NASA Exoplanet Archive TAP service...")
# Using TAP (Table Access Protocol) to query the Planetary Systems (ps) table
# default_flag=1 ensures we get the single best default parameter set for each planet
query = """
select pl_name, hostname, discoverymethod, disc_year, pl_bmasse, pl_rade, pl_orbper, pl_eqt, st_teff, st_mass, sy_dist 
from ps 
where default_flag=1
"""
url = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query={requests.utils.quote(query)}&format=csv"

response = requests.get(url)
if response.status_code == 200:
    print("Data fetched successfully. Saving to CSV...")
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save raw data directly
    csv_path = 'data/exoplanets.csv'
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
        
    print(f"Dataset saved to {csv_path}.")
    print("Done! You can now use data/exoplanets.csv in your RAG system.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print(response.text)
