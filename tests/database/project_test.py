from unittest import mock

@mock.patch('database.setup.db_connect')
def setUp():
    pass
    # mock_db = patch('database.setup.db_connect').start()

