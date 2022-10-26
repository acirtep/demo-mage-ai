from pandas import DataFrame
from demo_error_read_write.data_setup.generate_fake_data import generate_random_customer

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(**kwargs) -> DataFrame:
    """
    Template code for loading data from any source.

    Returns:
        DataFrame: Returned pandas data frame.
    """
    # Specify your data loading logic here

    return generate_random_customer(corrupted=True)


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'