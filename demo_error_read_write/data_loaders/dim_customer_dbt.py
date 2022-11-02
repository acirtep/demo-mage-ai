import subprocess
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything
    """
    # Specify your data loading logic here

    subprocess.run("cd /app/demo_error_read_write/dbt/demo && dbt snapshot", shell=True, executable='/bin/bash', check=True)
