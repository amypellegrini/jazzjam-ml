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

    responses.add(
        responses.GET,
        "http://localhost:3000/walking-bass-harmonies",
        json=[
            {
                "_id": 0,
                "keyFifths": 0,
                "beats": 4,
                "beatsType": 4,
                "harmonyRootStep": "D",
                "divisions": 1,
                "harmonyRootAlter": 0,
                "harmonyKind": "minor-seventh",
                "harmonyDuration": 2,
                "sequenceId": "95f250d2-e85c-485e-b666-df55fa845257",
                "startPitchStep": "D",
                "startPitchOctave": 3,
                "startPitchAlter": 0,
                "targetPitchStep": "G",
                "targetPitchOctave": 3,
                "targetPitchAlter": 0,
                "bassStep": None,
                "bassAlter": 0,
                "style": "swing",
            },
        ],
    )

    sequences, harmonies = fetchData()
    snapshot.assert_match(str(sequences), "sequences.txt")
    snapshot.assert_match(str(harmonies), "harmonies.txt")
