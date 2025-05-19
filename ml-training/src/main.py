from fetchData import fetchData

sequences_data, harmonies_data = fetchData()

root_step_categories = ["A", "B", "C", "D", "E", "F", "G"]
root_step_mapping = {step: i for i, step in enumerate(root_step_categories)}

harmony_kind_categories = [
    "augmented" "augmented,-seventh",
    "diminished" "diminished,-seventh",
    "dominant" "dominant,-11th",
    "dominant-13th",
    "dominant-ninth",
    "half-diminished",
    "major" "major,-11th",
    "major-13th",
    "major-minor",
    "major-ninth",
    "major-seventh",
    "major-sixth",
    "minor" "minor,-11th",
    "minor-13th",
    "minor-ninth",
    "minor-seventh",
    "minor-sixth",
    "none" "suspended,-fourth",
    "suspended-second",
]

harmony_kind_mapping = {kind: i for i, kind in enumerate(harmony_kind_categories)}

start_pitch_step_categories = ["A", "B", "C", "D", "E", "F", "G"]
start_pitch_step_mapping = {
    step: i for i, step in enumerate(start_pitch_step_categories)
}

target_pitch_step_categories = ["A", "B", "C", "D", "E", "F", "G"]
target_pitch_step_mapping = {
    step: i for i, step in enumerate(target_pitch_step_categories)
}


def one_hot_encode(category, mapping):
    vector = [0] * len(mapping)
    if category in mapping:
        index = mapping[category]
        vector[index] = 1
    return vector


encoded_harmonies = []

for harmony in harmonies_data:

    print(harmony)

    encoded_harmony = {
        "keyFifths": harmony["keyFifths"],
        "beats": harmony["beats"],
        "beatsType": harmony["beatsType"],
        "harmonyRootStep": one_hot_encode(
            harmony["harmonyRootStep"], root_step_mapping
        ),
        "harmonyRootAlter": harmony["harmonyRootAlter"],
        "harmonyKind": one_hot_encode(harmony["harmonyKind"], harmony_kind_mapping),
        "divisions": harmony["divisions"],
        "startPitchStep": one_hot_encode(
            harmony["startPitchStep"], start_pitch_step_mapping
        ),
        "startPitchOctave": harmony["startPitchOctave"],
        "startPitchAlter": harmony["startPitchAlter"],
        "targetPitchStep": one_hot_encode(
            harmony["targetPitchStep"], target_pitch_step_mapping
        ),
        "targetPitchOctave": harmony["targetPitchOctave"],
        "targetPitchAlter": harmony["targetPitchAlter"],
        "harmonyDuration": harmony["harmonyDuration"],
        "sequenceId": harmony["sequenceId"],
    }
    encoded_harmonies.append(encoded_harmony)


def encode_note(note):
    print("Note: ")
    print(note)

    encoded = {}
    encoded["duration"] = note["duration"]
    encoded["rest"] = (
        1 if note.get("rest", False) else 0
    )  # Default to False if 'rest' is missing
    encoded["chord"] = (
        1 if note.get("chord", False) else 0
    )  # Default to False if 'chord' is missing
    encoded["step"] = one_hot_encode(note["pitchStep"], root_step_mapping)
    encoded["octave"] = note["pitchOctave"]
    encoded["alter"] = note["pitchAlter"]

    return encoded


encoded_sequences = []

for sequence_data in sequences_data:
    encoded_sequence = [encode_note(note) for note in sequence_data["sequence"]]
    encoded_sequences.append(
        {"_id": sequence_data["_id"], "encoded_sequence": encoded_sequence}
    )

print(encoded_sequences[0])
print(encoded_harmonies[0])

sequence_map = {}

for sequence in encoded_sequences:
    sequence_map[sequence["_id"]] = sequence["encoded_sequence"]

training_pairs = []

for harmony in encoded_harmonies:

    sequence_id = harmony["sequenceId"]

    if sequence_id not in sequence_map:
        print(f"Sequence {sequence_id} not found in sequence map")
        continue

    sequence = sequence_map[sequence_id]

    training_pairs.append({"sequence": sequence, "harmony": harmony})

print("")
print(training_pairs[0])
