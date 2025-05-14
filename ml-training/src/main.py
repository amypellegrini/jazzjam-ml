import requests

# Define the base URL of your API
base_url = "http://localhost:3000"  # Replace with your actual API URL

# Endpoint for fetching all walking bass harmonies
sequences_endpoint = "/walking-bass-sequences"
sequences_url = base_url + sequences_endpoint

try:
    # Send a GET request to the harmonies endpoint
    response = requests.get(sequences_url)

    # Check if the request was successful (status code 200 OK)
    if response.status_code == 200:
        # Parse the JSON response
        harmonies_data = response.json()
        print("Successfully fetched harmonies data:")
        # You can now work with the harmonies_data (which will be a list of dictionaries)
        # For example, you can print the first harmony:
        if harmonies_data:
            print(harmonies_data[0])
    else:
        print(f"Failed to fetch harmonies. Status code: {response.status_code}")
        if response.text:
            print(f"Response body: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")