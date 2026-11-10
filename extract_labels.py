import pprint

import pandas as pd

from config import CODEBOOK_1, CODEBOOK_2

# Creating copies of the original dataframes
code_1_df = CODEBOOK_1.copy(deep=True)
code_2_df = CODEBOOK_2.copy(deep=True)


# Define function to extract value labels as dict from codebooks
def extract_labels(dataframe: pd.DataFrame) -> dict:
    """
    Extracts answer code and answer values and returns as dict type.
    """

    # Forwardfill variable name, value, and type columns
    for column in ["Variable Name", "Variable Label", "Variable Type"]:
        dataframe[column] = dataframe[column].ffill()

    # Drop NaN values from the dataframe
    dataframe = dataframe.dropna(subset=["Answer Label", "Answer Code"])

    # Create key values pairs of answer code and labels for each variable
    label_dict = (
        dataframe.groupby("Variable Name")
        .apply(lambda x: dict(zip(x["Answer Code"].astype(int), x["Answer Label"])))
        .to_dict()
    )

    return label_dict


if __name__ == "__main__":
    # Extract values using defined function
    labels_1 = extract_labels(code_1_df)
    pprint.pp(labels_1)

    labels_2 = extract_labels(code_2_df)
    pprint.pp(labels_2)
