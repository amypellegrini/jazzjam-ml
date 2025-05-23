import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


all_root_step_categories = ["A", "B", "C", "D", "E", "F", "G"]

all_bass_step_categories = ["A", "B", "C", "D", "E", "F", "G", "__MISSING__"]

all_harmony_kind_categories = [
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


def encodeHarmony(harmony):
    harmony_df = pd.DataFrame(harmony)

    harmony_df["bassStep"] = harmony_df["bassStep"].fillna("__MISSING__")
    harmony_df = harmony_df.drop(columns=["_id"])
    harmony_df = harmony_df.drop(columns=["sequenceId"])
    harmony_df = harmony_df.drop(columns=["style"])

    harmony_df["harmonyRootStep"] = pd.Categorical(
        harmony_df["harmonyRootStep"], categories=all_root_step_categories
    )

    harmony_df["targetPitchStep"] = pd.Categorical(
        harmony_df["targetPitchStep"], categories=all_root_step_categories
    )

    harmony_df["startPitchStep"] = pd.Categorical(
        harmony_df["startPitchStep"], categories=all_root_step_categories
    )

    harmony_df["harmonyKind"] = pd.Categorical(
        harmony_df["harmonyKind"], categories=all_harmony_kind_categories
    )

    harmony_df["bassStep"] = pd.Categorical(
        harmony_df["bassStep"], categories=all_bass_step_categories
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "ohe_harmony_root_step",
                OneHotEncoder(
                    categories=[all_root_step_categories],
                    sparse_output=False,
                    handle_unknown="error",
                ),
                ["harmonyRootStep"],
            ),
            (
                "ohe_harmony_target_step",
                OneHotEncoder(
                    categories=[all_root_step_categories],
                    sparse_output=False,
                    handle_unknown="error",
                ),
                ["targetPitchStep"],
            ),
            (
                "ohe_harmony_start_step",
                OneHotEncoder(
                    categories=[all_root_step_categories],
                    sparse_output=False,
                    handle_unknown="error",
                ),
                ["startPitchStep"],
            ),
            (
                "ohe_harmony_kind",
                OneHotEncoder(
                    categories=[all_harmony_kind_categories],
                    sparse_output=False,
                    handle_unknown="error",
                ),
                ["harmonyKind"],
            ),
            (
                "ohe_harmony_bass_step",
                OneHotEncoder(
                    categories=[all_bass_step_categories],
                    sparse_output=False,
                    handle_unknown="error",
                ),
                ["bassStep"],
            ),
        ],
        remainder="passthrough",
    )

    encoded_data_array = preprocessor.fit_transform(harmony_df)

    encoded_df = pd.DataFrame(
        encoded_data_array,
        columns=preprocessor.get_feature_names_out(),
        index=harmony_df.index,
    )

    return encoded_df
