from encodeHarmony import encodeHarmony
import pytest


@pytest.mark.parametrize(
    "root_step,expected_encoding",
    [
        ("A", [1, 0, 0, 0, 0, 0, 0]),
        ("B", [0, 1, 0, 0, 0, 0, 0]),
        ("C", [0, 0, 1, 0, 0, 0, 0]),
        ("D", [0, 0, 0, 1, 0, 0, 0]),
        ("E", [0, 0, 0, 0, 1, 0, 0]),
        ("F", [0, 0, 0, 0, 0, 1, 0]),
        ("G", [0, 0, 0, 0, 0, 0, 1]),
    ],
)
def test_root_step_one_hot_encoding(root_step, expected_encoding):
    harmony = (
        {
            "_id": 0,
            "keyFifths": 0,
            "beats": 4,
            "beatsType": 4,
            "harmonyRootStep": root_step,
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
    )
    encoded_harmony_df = encodeHarmony(harmony)

    # --- Assertion Part ---
    # Define the possible root step values in the order they are encoded
    root_step_columns = [
        f"harmonyRootStep_{step}" for step in ["A", "B", "C", "D", "E", "F", "G"]
    ]

    # Select the one-hot encoded columns for the first (and only) row
    # The .iloc[0] gets the first row, .tolist() converts it to a list
    actual_encoding = encoded_harmony_df[root_step_columns].iloc[0].tolist()

    print(f"Input root_step: {root_step}")
    print(f"Actual encoding: {actual_encoding}")
    print(f"Expected encoding: {expected_encoding}")

    assert (
        actual_encoding == expected_encoding
    ), f"Encoding mismatch for root_step '{root_step}'"
