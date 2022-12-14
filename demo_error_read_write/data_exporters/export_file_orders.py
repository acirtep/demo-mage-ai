from mage_ai.io.file import FileIO
from pandas import DataFrame
import os
from datetime import datetime

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_file(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to filesystem.

    Docs: https://github.com/mage-ai/mage-ai/blob/master/docs/blocks/data_loading.md#fileio
    """
    filepath = os.getenv('DATA_OUTPUT_LANDING_ZONE')
    filepath = f"{filepath}/orders-{datetime.today().strftime('%Y-%m-%d')}.csv"
    FileIO().export(df, filepath, 'csv', **{'sep': '\t', 'index': False})
