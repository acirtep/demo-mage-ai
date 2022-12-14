from mage_ai.io.file import FileIO
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_file(**kwargs) -> DataFrame:
    """
    Template for loading data from filesystem.

    Docs: https://github.com/mage-ai/mage-ai/blob/master/docs/blocks/data_loading.md#fileio
    """
    filepath = 'path/to/your/file.csv'
    return FileIO().load(filepath)


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
