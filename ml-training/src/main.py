import requests

# Define the base URL of your API
base_url = "http://localhost:3000"  # Replace with your actual API URL

# Endpoint for fetching all walking bass harmonies
sequences_endpoint = "/walking-bass-sequences"
harmonies_endpoint = "/walking-bass-harmonies"

sequences_url = base_url + sequences_endpoint
harmonies_url = base_url + harmonies_endpoint

try:
    # Send a GET request to the harmonies endpoint
    sequences_data = requests.get(sequences_url)
    harmonies_data = requests.get(harmonies_url)

    # Check if the request was successful (status code 200 OK)
    if sequences_data.status_code == 200:
        # Parse the JSON response
        sequences_data = sequences_data.json()
        print("Successfully fetched sequences data:")
        # You can now work with the harmonies_data (which will be a list of dictionaries)
        # For example, you can print the first harmony:
        if sequences_data:
            print(sequences_data[0])
    else:
        print(f"Failed to fetch sequences. Status code: {sequences_data.status_code}")
        if sequences_data.text:
            print(f"Response body: {sequences_data.text}")

    if harmonies_data.status_code == 200:
        harmonies_data = harmonies_data.json()
        print("Successfully fetched harmonies data:")
        if harmonies_data:
            print(harmonies_data[0])
    else:
        print(f"Failed to fetch harmonies. Status code: {harmonies_data.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")

sequence_map = {}

for sequence in sequences_data:
    sequence_map[sequence["_id"]] = sequence["sequence"]

print(sequence_map)
