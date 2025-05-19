from fetchData import fetchData
import responses


@responses.activate
def test_it_fetches_and_returns_data(snapshot):
    responses.add(
        responses.GET,
        "http://localhost:3000/walking-bass-sequences",
        json=[
            {
                "_id": "95f250d2-e85c-485e-b666-df55fa845257",
                "sequence": [
                    {
                        "duration": 1,
                        "pitchStep": "D",
                        "pitchOctave": 3,
                        "pitchAlter": 0,
                        "rest": None,
                        "chord": None,
                    },
                    {
                        "duration": 1,
                        "pitchStep": "F",
                        "pitchOctave": 3,
                        "pitchAlter": 0,
                        "rest": None,
                        "chord": None,
                    },
                ],
            },
        ],
    )

    data = str(fetchData())
    snapshot.assert_match(data, "data.txt")
