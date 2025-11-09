"""
Configuration file for job priority assignment system.
"""

# Job type priority mapping (lower number = higher priority)
JOB_TYPE_PRIORITY = {
    'HAZARD': 1,
    'REPAIRS': 2,
    'SURVEY': 3
}

# Column names
JOBS_FILE_COLUMNS = {
    'job_id': 'JobID',
    'parent_job_type': 'Parent Job Type',
    'location': 'Location',
    'road': 'Road',
    'standard_job': 'Standard Job',
    'due': 'Due'
}

CAPABILITY_FILE_COLUMNS = {
    'job_code': 'Job Code',
    'capability_internal': 'Capability Internal'
}

# Priority for jobs that cannot be done internally
CANNOT_DO_PRIORITY = -1

# Date format (primary format, but multiple formats are supported)
DATE_FORMAT = '%d/%m/%Y %I:%M:%S %p'

# Supported date formats (handled automatically by parse_date function):
# - dd/mm/yyyy hh:mm:ss AM/PM (e.g., 01/07/2024 11:26:45 AM)
# - dd/mm/yyyy hh:mm AM/PM (e.g., 01/07/2024 11:26 AM)
# - dd/mm/yy hh:mm:ss AM/PM (e.g., 01/07/24 11:26:45 AM)
# - dd/mm/yy hh:mm AM/PM (e.g., 01/07/24 11:26 AM)
# - dd/mm/yyyy (e.g., 01/07/2024)
# - dd/mm/yy (e.g., 01/07/24)
# - yyyy-mm-dd hh:mm:ss (e.g., 2024-07-01 11:26:45)
# - yyyy-mm-dd hh:mm (e.g., 2024-07-01 11:26)
# - yyyy-mm-dd (e.g., 2024-07-01)