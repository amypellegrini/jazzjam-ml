import pandas as pd


def encodeSequence(sequence):
    sequence_df = pd.DataFrame(sequence)

    sequence_df = sequence_df.drop(columns=["_id"])

    return sequence_df
