import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


all_pitch_step_categories = ["A", "B", "C", "D", "E", "F", "G", "__MISSING__"]


def encodeNote(note):
    note_df = pd.DataFrame([note])
    note_df = note_df.drop(columns=["chord"])

    note_df["pitchStep"] = note_df["pitchStep"].fillna("__MISSING__")

    note_df["pitchStep"] = pd.Categorical(
        note_df["pitchStep"], categories=all_pitch_step_categories
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "ohe_note_pitch_step",
                OneHotEncoder(
                    categories=[all_pitch_step_categories],
                    sparse_output=False,
                    handle_unknown="error",
                ),
                ["pitchStep"],
            ),
        ],
        remainder="passthrough",
    )

    encoded_data_array = preprocessor.fit_transform(note_df)

    encoded_df = pd.DataFrame(
        encoded_data_array,
        columns=preprocessor.get_feature_names_out(),
        index=note_df.index,
    )

    return encoded_df
