import requests

# Your N2YO API key
api_key = 'L9NPLA-JM7B6C-DG46RL-5GE8'  # Replace with your actual API key

# The satellite ID for NOAA 19
sat_id = '33591'  # Example for NOAA 19

# Observer's latitide in decimal degrees
lat = '38.716753'

# Observer's longitude in decimal degrees
lon = '-9.133368'

# Observer's altitude above sea level in meters
alt = '100'

# Number of satellite positions to return 
#(each position for each further second with limit 300 seconds)
count = '2' # return positions for current time, and current time + 1 second

# Make the API request
response = requests.get(url = ("https://api.n2yo.com/rest/v1/satellite/positions/" + sat_id+ '/' + lat + '/' + lon + '/' + alt + '/' + count + '/' + "&apiKey=" + api_key))

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    
    # Print the response data (satellite position and other details)
    print(data)
else:
    print(f'Error: {response.status_code}')
