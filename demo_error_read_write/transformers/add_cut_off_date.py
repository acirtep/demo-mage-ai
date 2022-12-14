from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform_df(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        df (DataFrame): Data frame from parent block.

    Returns:
        DataFrame: Transformed data frame
    """
    # Specify your transformation logic here
    df["cut_off_date"] = kwargs["cut_off_date"]

    return df


@test
def validate_(df) -> None:
    """
    Validate 
    """
    from pandas.api.types import is_integer_dtype
    assert df is not None, 'The output is undefined'
    assert is_integer_dtype(df.id)
    assert df.id.is_unique

