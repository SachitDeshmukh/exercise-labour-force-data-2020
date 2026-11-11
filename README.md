# Exercise Data Preparation and Analysis Project

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

## Download from GitHub

You can get the project in either of these ways:

- **Clone with Git:** Open a terminal and run:

  ```bash
  git clone https://github.com/SachitDeshmukh/exercise-labour-force-data-2020.git
  cd exercise-labour-force-data-2020
  ```

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

## Run the Stata analysis

After the Python workflow completes:

1. Confirm that `working_dataset.dta` is in the project root.
2. Open Stata 15 or newer and set its working directory to the project root, where `working_dataset.dta` and `preliminary_analysis.do` are located. For example, in Stata's command window run:

   ```stata
   cd "C:\path\to\exercise-labour-force-data-2020"
   ```

   Replace the example path with the folder where you cloned or extracted the project.

3. Run the do-file in Stata's command window:

   ```stata
   do "preliminary_analysis.do"
   ```

   Alternatively, open `preliminary_analysis.do` in Stata's Do-file Editor and select **Do**.

4. When it completes, the analysis log is saved as `stata_review_output/preliminary_analysis.log` in the project folder.

## Important notes

- The scripts rely on relative file paths defined in `config.py`.
- The project expects the source files to remain in the same folder names and with the same names as currently set in `config.py`.
- If files are moved, renamed, or missing, the script will fail because it reads them directly.
- `prep_data.py` includes a custom label-fix step for a known incorrect entry in the second codebook. Do not remove it unless you are intentionally changing the data logic.
