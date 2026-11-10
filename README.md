# CEGIS Data Preparation Project

The workflow is designed to:

- load the raw data files from the `Data Files` folder
- load the codebooks from the `Supporting Documents` folder
- merge and clean the datasets
- create standardized identifiers
- label categorical values using the survey codebooks
- export the final cleaned dataset as `working_dataset.dta`

## Requirements

Before running the project, make sure you have:

- Python 3.13 or newer (as specified in `pyproject.toml`)
- `uv` installed
- access to the files listed above in the project directory

## Recommended setup with uv

1. Open a terminal in the project folder.
2. Create the project environment and install dependencies:

```bash
uv sync
```

## Run the project

From the project root, run:

```bash
uv run prep_data.py
```

This script will:

- activate venv and install all necessary libraries
- read raw datasets from the configured file paths
- clean and merge the records
- assign working identifiers
- label categorical responses from the codebooks
- generate the output file `working_dataset.dta`

## Expected output

The final dataset is exported as:

```text
working_dataset.dta
```

This file is created in the project root when the script completes successfully.

## Important notes

- The scripts rely on relative file paths defined in `config.py`.
- The project expects the source files to remain in the same folder names and with the same names as currently set in `config.py`.
- If files are moved, renamed, or missing, the script will fail because it reads them directly.
- `prep_data.py` includes a custom label-fix step for a known incorrect entry in the second codebook. Do not remove it unless you are intentionally changing the data logic.
