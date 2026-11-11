import pandas as pd

from clean import assign_new_id, clean_data
from config import (
    CODEBOOK_1,
    CODEBOOK_2,
    DATASET_1,
    DATASET_2,
    EMPLOY_CATEGORIES,
    EMPLOY_LOCATION,
    ID_COLS,
)
from extract_labels import extract_labels


def label_one_variable(
    variable: str, code_value_dict: dict, df: pd.DataFrame
) -> pd.DataFrame:
    categorical_col = variable
    value_col = variable + "_labeled"
    code_value_order = [code_value_dict[key] for key in sorted(code_value_dict.keys())]

    df[value_col] = (
        df[categorical_col]
        .map(code_value_dict)
        .astype(pd.CategoricalDtype(categories=code_value_order, ordered=True))
    )

    df[value_col] = df[value_col].replace(
        {"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-"}, regex=True
    )

    return df


def assign_values(df: pd.DataFrame, code_values_all: dict) -> pd.DataFrame:
    for key, values in code_values_all.items():
        df = label_one_variable(variable=key, code_value_dict=values, df=df)

    return df


def categorize_employment(df: pd.DataFrame, category_dict: dict) -> pd.DataFrame:
    for category, value_codes in category_dict.items():
        df.loc[df["status"].isin(value_codes), "employment_nature"] = category

    return df


def categorize_location(df: pd.DataFrame, category_dict: dict) -> pd.DataFrame:
    for category, value_codes in category_dict.items():
        df.loc[df["location"].isin(value_codes), "employment_location"] = category

    return df


def main() -> None:
    data_1_df = DATASET_1.copy(deep=True)
    data_2_df = DATASET_2.copy(deep=True)
    code_1_df = CODEBOOK_1.copy(deep=True)
    code_2_df = CODEBOOK_2.copy(deep=True)

    clean_df = clean_data(data_1_df, data_2_df)
    clean_df = assign_new_id(clean_df, ID_COLS)
    labels_1 = extract_labels(code_1_df)
    labels_2 = extract_labels(code_2_df)

    labels_2["location"][20] = "Workplace in urban areas and located in own dwelling"
    labels_2["usa_location"][20] = (
        "Workplace in urban areas and located in own dwelling"
    )

    clean_df = assign_values(df=clean_df, code_values_all=labels_1)
    clean_df = assign_values(df=clean_df, code_values_all=labels_2)
    clean_df = categorize_employment(df=clean_df, category_dict=EMPLOY_CATEGORIES)
    clean_df = categorize_location(df=clean_df, category_dict=EMPLOY_LOCATION)

    clean_df.to_stata("working_dataset.dta", version=118, write_index=False)


if __name__ == "__main__":
    main()
