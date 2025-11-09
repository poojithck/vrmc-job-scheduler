# Job Priority Assignment System

A modular Python system for prioritizing jobs based on job type, due dates, and internal capability constraints.

## Features

- Filter jobs by reference date
- Assign priorities based on job type (HAZARD > REPAIRS > SURVEY)
- Consider due dates within same job type
- Handle internal capability constraints
- Flag jobs requiring capability checks
- Export results to Excel or CSV

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
.
├── main.py                    # Main execution script
├── config.py                  # Configuration and constants
├── data_loader.py            # Data loading functions
├── filter.py                 # Date filtering logic
├── capability_checker.py     # Capability validation
├── priority_assignment.py    # Priority calculation logic
├── output_handler.py         # Output generation and export
├── examples.py               # Usage examples
├── utils.py                  # Validation utilities
└── requirements.txt          # Python dependencies
```

## Usage

### Basic Usage

1. Update the file paths in `main.py`:

```python
JOBS_FILE = 'your_jobs_file.csv'
CAPABILITY_FILE = 'RM Codes Crew Capability.xlsx'
REFERENCE_DATE = '10/10/2024'
OUTPUT_FILE = 'prioritized_jobs_output.xlsx'
```

2. Run the script:

```bash
python main.py
```

### Custom Usage

```python
from main import process_job_priorities

result_df = process_job_priorities(
    jobs_file_path='jobs_data.csv',
    capability_file_path='RM Codes Crew Capability.xlsx',
    reference_date='10/10/2024',
    output_path='output.xlsx',
    capability_sheet_name='Sheet1 (2)'
)
```

## Input File Requirements

### Jobs File
Required columns:
- JobID
- Parent Job Type (values: HAZARD, REPAIRS, or SURVEY)
- Location
- Road
- Standard Job
- Due (format: dd/mm/yyyy hh:mm:ss AM/PM)

### Capability File
Required columns:
- Job Code (matches Standard Job in jobs file)
- Capability Internal

## Priority Rules

1. Jobs with "None" capability get priority -1 (Cannot Do flag)
2. Jobs with "<" or ">" in capability get "Check" flag but are still prioritized
3. Among doable jobs:
   - HAZARD (Priority 1)
   - REPAIRS (Priority 2)
   - SURVEY (Priority 3)
4. Within same job type, earlier due dates get higher priority
5. Same job type + same due date = same priority number

## Output

The system generates an Excel file with:
- Prioritized Jobs sheet with all job details
- Summary sheet with statistics
- Flags for jobs requiring attention:
  - Cannot_Do_Flag: Jobs we cannot do internally
  - Capability_Check_Flag: Jobs requiring capability verification

## Example Output Columns

- Priority
- JobID
- Parent Job Type
- Standard Job
- Location
- Road
- Due
- can_do_internally
- needs_capability_check
- Cannot_Do_Flag
- Capability_Check_Flag

## Notes

- Date format must be: dd/mm/yyyy hh:mm:ss AM/PM
- Jobs with due dates before the reference date are excluded
- Capability values with comparison operators (< or >) are flagged but still prioritized
- Jobs without matching capability data are treated as doable by default
