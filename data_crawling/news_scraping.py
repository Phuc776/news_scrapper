import requests
import json

# Define your API Key here
API_KEY = 'shNAPcBAj0HYRJ62u7gXFh26f98W4hZN9gbaFQT4iV8'

# Set the API endpoint and headers
url = "https://api.newscatcherapi.com/v2/search"

# You can customize the query parameter (e.g., "technology" or "sports")
querystring = {"q":"technology", "lang":"en", "sort_by":"relevancy", "page":"1"}

headers = {
    'x-api-key': API_KEY
}

# Make the request to the Newscatcher API
response = requests.get(url, headers=headers, params=querystring)

# Check if the response is successful
if response.status_code == 200:
    news_data = response.json()
    # Pretty-print the result to see the structure
    print(json.dumps(news_data, indent=4))
    
    # Save the results to a file
    with open('news_results.json', 'w') as f:
        json.dump(news_data, f, indent=4)
else:
    print(f"Error: {response.status_code}, {response.text}")

