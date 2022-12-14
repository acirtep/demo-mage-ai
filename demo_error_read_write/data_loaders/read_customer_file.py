from mage_ai.io.file import FileIO

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Template for loading data from filesystem.

    Docs: https://github.com/mage-ai/mage-ai/blob/master/docs/blocks/data_loading.md#fileio
    """
    filepath = f'/app/demo_error_read_write/data_setup/landing_zone/customers-{kwargs["cut_off_date"]}.csv'
    return FileIO().load(filepath, **{'sep': '\t'})
