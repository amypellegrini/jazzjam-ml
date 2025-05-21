from encodeHarmony import encodeHarmony
import pytest

# Base harmony object that can be reused across tests
BASE_HARMONY = {
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
}


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
    # Create a copy of the base harmony and set the root step
    harmony = (dict(BASE_HARMONY, harmonyRootStep=root_step),)
    encoded_harmony_df = encodeHarmony(harmony)

    # --- Assertion Part ---
    # Define the possible root step values in the order they are encoded
    root_step_columns = [
        f"ohe_harmony_root_step__harmonyRootStep_{step}"
        for step in ["A", "B", "C", "D", "E", "F", "G"]
    ]

    # Select the one-hot encoded columns for the first (and only) row
    # The .iloc[0] gets the first row, .tolist() converts it to a list
    actual_encoding = encoded_harmony_df[root_step_columns].iloc[0].tolist()

    assert (
        actual_encoding == expected_encoding
    ), f"Encoding mismatch for root_step '{root_step}'"


@pytest.mark.parametrize(
    "harmony_kind",
    [
        "augmented",
        "augmented-seventh",
        "diminished",
        "diminished-seventh",
        "dominant",
        "dominant-11th",
        "dominant-13th",
        "dominant-ninth",
        "half-diminished",
        "major",
        "major-11th",
        "major-13th",
        "major-minor",
        "major-ninth",
        "major-seventh",
        "major-sixth",
        "minor",
        "minor-11th",
        "minor-13th",
        "minor-ninth",
        "minor-seventh",
        "minor-sixth",
        "none",
        "suspended-fourth",
        "suspended-second",
    ],
)
def test_harmony_kind_one_hot_encoding(harmony_kind):
    harmony = (dict(BASE_HARMONY, harmonyKind=harmony_kind),)
    encoded_harmony_df = encodeHarmony(harmony)

    harmony_kind_columns = [
        f"ohe_harmony_kind__harmonyKind_{kind}"
        for kind in [
            "augmented",
            "augmented-seventh",
            "diminished",
            "diminished-seventh",
            "dominant",
            "dominant-11th",
            "dominant-13th",
            "dominant-ninth",
            "half-diminished",
            "major",
            "major-11th",
            "major-13th",
            "major-minor",
            "major-ninth",
            "major-seventh",
            "major-sixth",
            "minor",
            "minor-11th",
            "minor-13th",
            "minor-ninth",
            "minor-seventh",
            "minor-sixth",
            "none",
            "suspended-fourth",
            "suspended-second",
        ]
    ]

    actual_encoding = encoded_harmony_df[harmony_kind_columns].iloc[0].tolist()
    expected_encoding = [0.0] * len(harmony_kind_columns)
    expected_encoding[
        harmony_kind_columns.index(f"ohe_harmony_kind__harmonyKind_{harmony_kind}")
    ] = 1.0

    assert actual_encoding == expected_encoding


def test_drops_unwanted_columns_from_harmony():
    encoded_harmony_df = encodeHarmony([BASE_HARMONY])

    assert "_id" not in encoded_harmony_df.columns
    assert "sequenceId" not in encoded_harmony_df.columns
    assert "style" not in encoded_harmony_df.columns
