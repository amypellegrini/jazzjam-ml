import requests


def fetchData():
    base_url = "http://localhost:3000"
    sequences_url = base_url + "/walking-bass-sequences"
    harmonies_url = base_url + "/walking-bass-harmonies"

    try:
        sequences_data = requests.get(sequences_url)
        harmonies_data = requests.get(harmonies_url)

        if sequences_data.status_code == 200 and harmonies_data.status_code == 200:
            return sequences_data.json(), harmonies_data.json()
        else:
            return f"Error: Sequences status {sequences_data.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Request error: {str(e)}"
