from encodeSequence import encodeSequence

BASE_SEQUENCE = (
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
)


def test_drops_id_from_sequence():
    encoded_sequence_df = encodeSequence(BASE_SEQUENCE)
    assert "_id" not in encoded_sequence_df.columns
