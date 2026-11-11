import numpy as np
import pandas as pd

from config import DATASET_1, DATASET_2, ID_COLS


def clean_data(df_1: pd.DataFrame, df_2: pd.DataFrame) -> pd.DataFrame:
    # Dropping columns with all null values
    df_1 = df_1.drop(columns=["j", "k", "l"])
    df_2 = df_2.drop(columns=["d"])

    # Dropping duplicates and NaN
    df_1 = df_1.dropna(subset=["person_code"])
    print(
        f"The shape of the dataset 1 after dropping NaN person codes is {df_1.shape}."
    )
    df_2 = df_2.dropna(subset=["person_code"])
    print(
        f"The shape of the dataset 2 after dropping NaN person codes is {df_2.shape}."
    )
    df_2 = df_2.drop_duplicates(subset="person_code")
    print(f"The shape of the dataset 2 after dropping duplicates is {df_2.shape}.")

    # Merging the two data sets
    merged_df = pd.merge(df_1, df_2, on="person_code", sort=True)
    print(f"The shape of the merged dataset is {merged_df.shape}.")

    # Clean NaN values
    merged_df["socialsecurity"] = (
        merged_df["socialsecurity"].replace({"Missing", np.nan}, 9).astype(int)
    )
    merged_df["earn_l30d"] = merged_df["earn_l30d"].replace("Nil", 0).astype(float)

    #  Clean data types
    merged_df[["earn_lmonth", "earn_l30d"]] = merged_df[
        ["earn_lmonth", "earn_l30d"]
    ].astype(float)

    merged_df["location"] = merged_df["location"].astype("Int64")

    # Drop outliers
    clean_df = merged_df[merged_df["earn_l30d"] >= float(0)]

    clean_df = clean_df[clean_df["age"] >= float(15)]
    age_q1 = clean_df["age"].quantile(0.25)
    age_q3 = clean_df["age"].quantile(0.75)
    age_iqr = age_q3 - age_q1
    age_lower_bound = age_q1 - 1.5 * age_iqr
    age_upper_bound = age_q3 + 1.5 * age_iqr

    clean_df = clean_df[clean_df["age"] >= age_lower_bound]
    clean_df = clean_df[clean_df["age"] <= age_upper_bound]
    print(f"The shape of the cleaned dataset is {clean_df.shape}.")

    return clean_df


# Assign new unique IDs
def assign_new_id(df: pd.DataFrame, id_cols: dict) -> pd.DataFrame:
    id_cols_new = []

    for col, cap in id_cols.items():
        df[col] = df[col].astype(int)
        col_new = col + "_id"
        id_cols_new.append(col_new)
        df[col_new] = df[col].astype(str).str.zfill(cap)

    df["assigned_unique_id"] = df[id_cols_new].astype(str).agg("_".join, axis=1)

    df = df.drop(columns=id_cols_new)

    return df


if __name__ == "__main__":
    data_1_df = DATASET_1.copy(deep=True)
    data_2_df = DATASET_2.copy(deep=True)
    clean_df = clean_data(data_1_df, data_2_df)
    clean_df = assign_new_id(clean_df, ID_COLS)
    clean_df.to_csv(r"clean_dataset.csv", index=False)
