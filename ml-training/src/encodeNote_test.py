from encodeNote import encodeNote
import pytest
import pandas as pd

BASE_NOTE = {
    "duration": 1,
    "pitchStep": "D",
    "pitchOctave": 3,
    "pitchAlter": 0,
    "rest": None,
    "chord": None,
}


@pytest.mark.parametrize(
    "pitch_step,expected_encoding",
    [
        ("A", [1, 0, 0, 0, 0, 0, 0, 0]),
        ("B", [0, 1, 0, 0, 0, 0, 0, 0]),
        ("C", [0, 0, 1, 0, 0, 0, 0, 0]),
        ("D", [0, 0, 0, 1, 0, 0, 0, 0]),
        ("E", [0, 0, 0, 0, 1, 0, 0, 0]),
        ("F", [0, 0, 0, 0, 0, 1, 0, 0]),
        ("G", [0, 0, 0, 0, 0, 0, 1, 0]),
        (None, [0, 0, 0, 0, 0, 0, 0, 1]),
    ],
)
def test_hot_encodes_pitch_step(pitch_step, expected_encoding):
    note = dict(BASE_NOTE, pitchStep=pitch_step)
    encoded_note_df = encodeNote(note)

    pitch_step_columns = [
        f"ohe_note_pitch_step__pitchStep_{step}"
        for step in ["A", "B", "C", "D", "E", "F", "G", "__MISSING__"]
    ]

    actual_encoding = encoded_note_df[pitch_step_columns].iloc[0].tolist()

    assert actual_encoding == expected_encoding


@pytest.mark.parametrize(
    "chord_value",
    [
        None,
        True,
        False,
    ],
)
def test_drops_unwanted_columns(chord_value):
    note = dict(BASE_NOTE, chord=chord_value)
    encoded_note_df = encodeNote(note)

    assert "chord" not in encoded_note_df.columns
    assert "remainder__chord" not in encoded_note_df.columns


@pytest.mark.parametrize(
    "rest_value,expected_encoding",
    [
        (None, 0),
        (True, 1),
        (False, 0),
    ],
)
def test_encodes_rest_correctly(rest_value, expected_encoding):
    note = dict(BASE_NOTE, rest=rest_value)
    encoded_note_df = encodeNote(note)

    assert encoded_note_df.iloc[0]["remainder__rest"] == expected_encoding


def test_encodes_note_as_dataframe(snapshot):
    encoded_note_df = encodeNote(BASE_NOTE)

    assert isinstance(encoded_note_df, pd.DataFrame)
    snapshot.assert_match(encoded_note_df.to_string(), "encoded_note_df.txt")
