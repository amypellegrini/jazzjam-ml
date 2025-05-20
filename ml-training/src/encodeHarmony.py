import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def encodeHarmony(harmony):
    harmony_df = pd.DataFrame(harmony)

    harmony_df = harmony_df.drop(columns=["_id"])
    harmony_df = harmony_df.drop(columns=["sequenceId"])
    harmony_df = harmony_df.drop(columns=["style"])

    all_root_step_categories = ["A", "B", "C", "D", "E", "F", "G"]

    encoder = OneHotEncoder(
        categories=[all_root_step_categories],
        sparse_output=False,
        handle_unknown="error",
    )

    harmony_df["harmonyRootStep"] = pd.Categorical(
        harmony_df["harmonyRootStep"], categories=all_root_step_categories
    )

    encoded_harmony_root_step = encoder.fit_transform(harmony_df[["harmonyRootStep"]])

    encoded_df = pd.DataFrame(
        encoded_harmony_root_step,
        columns=encoder.get_feature_names_out(["harmonyRootStep"]),
    )

    harmony_df = pd.concat([harmony_df, encoded_df], axis=1)
    harmony_df = harmony_df.drop(columns=["harmonyRootStep"])

    return harmony_df
