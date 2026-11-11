import pandas as pd

# Load datasets
DATASET_1 = pd.read_csv(r"Data Files/Labour1_use.csv")
print(f"The shape of the original dataset 1 is {DATASET_1.shape}")

DATASET_2 = pd.read_excel(r"Data Files/Labour2_use.xlsx", header=3)
print(f"The shape of the original dataset 2 is {DATASET_2.shape}")

QUICK_ACCESS_DF = pd.read_csv(r"clean_dataset.csv")

# Load codebooks
CODEBOOK_1 = pd.read_excel(r"Supporting Documents\Labour1_Codebook.xlsx")
CODEBOOK_2 = pd.read_excel(r"Supporting Documents\Labour2_Codebook.xlsx")

# ID COLUMNS
ID_COLS = {
    "state": 2,
    "hh_code": 6,
    "person_code": 6,
}  # variable name: string characters to fill to for ID

# EMPLOYMENT CATEGORIES
EMPLOY_CATEGORIES = {
    "self_employed": [11, 12, 21],
    "salaried": [31],
    "casual_labour": [41, 42, 51],
    "unemployeed": [81],
    "not_part": [91, 92, 93, 94, 95, 97],
}

# URBAN VERSUS RURAL EMPLOYMENT
EMPLOY_LOCATION = {
    "urban": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    "rural": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    "none": [99],
}
