from db_layer.database_manager import database_manager
from unittest.mock import MagicMock

class Testdatabase_manager:
    def setup_method(self):
        self.mock_connection=MagicMock()

    def test_create_table_sucess(self,monkeypatch):
        mock_execute=MagicMock()
        mock_execute.execute=MagicMock(return_value=True)
        self.mock_connection.cursor=MagicMock(return_value=mock_execute)
        self.mock_connection.commit=MagicMock()

        monkeypatch.setattr('db_layer.database_manager.get_connection',lambda : self.mock_connection)

        db_obj=database_manager()
        db_obj.create_table('expense','schema')


        self.mock_connection.cursor.assert_called_once()
        mock_execute.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()

    def test_create_table_failed(self,monkeypatch):
        mock_cursor=MagicMock()
        mock_cursor.execute=MagicMock()
        self.mock_connection.cursor=MagicMock(return_value=mock_cursor)
        self.mock_connection.commit=MagicMock(side_effect=Exception('error occured'))
        mock_print=MagicMock()

        monkeypatch.setattr('db_layer.database_manager.get_connection',lambda : self.mock_connection)
        monkeypatch.setattr('builtins.print',mock_print)
        db_obj=database_manager()
        db_obj.create_table('expense','schema')

        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()
        mock_print.assert_called_once()

    def test_fetch_data_sucess(self,monkeypatch):
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock()
        mock_cursor.fetchall=MagicMock(return_value=[('username','expesne')])
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)

        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)

        db_obj=database_manager()
        data=db_obj.fetch_data(table_name='expense')

        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()

        assert data==[('username','expesne')]

    def test_fetch_data_success_where_clause(self, monkeypatch):
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock()
        mock_cursor.fetchall = MagicMock(return_value=[('username', 'expesne')])
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)

        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)

        db_obj = database_manager()
        data = db_obj.fetch_data(table_name='expense',where_clause=['username=?'],parameters=['username'])

        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()

        assert data == [('username', 'expesne')]

    def test_fetch_data_failed(self,monkeypatch):
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('error occured'))
        mock_cursor.fetchall = MagicMock(return_value=[('username', 'expesne')])
        mock_print=MagicMock()
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)

        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        monkeypatch.setattr('builtins.print',mock_print)
        db_obj = database_manager()
        data = db_obj.fetch_data(table_name='expense', where_clause=['username=?'], parameters=['username'])

        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_print.assert_called_once()

        assert data == None

    def test_insert_data_row_count_1(self,monkeypatch):
        #arrange
        mock_cursor=MagicMock()
        mock_cursor.execute=MagicMock()
        mock_cursor.rowcount=1
        self.mock_connection.cursor=MagicMock(return_value=mock_cursor)
        self.mock_connection.commit=MagicMock()

        #act
        monkeypatch.setattr('db_layer.database_manager.get_connection',lambda : self.mock_connection)
        db_obj=database_manager()
        result=db_obj.insert_data('users', ['name', 'age'], ['Alice', 30])

        #assert
        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()
        assert result==True
    def test_insert_data_row_count_0(self,monkeypatch):
        # arrange
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock()
        mock_cursor.rowcount = 0
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()

        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        db_obj = database_manager()
        result = db_obj.insert_data('users', ['name', 'age'], ['Alice', 30])

        # assert
        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()
        assert result == False

    def test_insert_data_failed_no_table(self,monkeypatch):
        # arrange
        mock_print=MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('No table name'))
        mock_cursor.rowcount = 0
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()

        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        monkeypatch.setattr('builtins.print',mock_print)
        db_obj = database_manager()
        result = db_obj.insert_data(None, 'columns', [])

        # assert
        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_print.assert_called_once()
        assert result == False

    def test_insert_data_failed_no_columns(self,monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('No column'))
        mock_cursor.rowcount = 0
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()

        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        monkeypatch.setattr('builtins.print', mock_print)
        db_obj = database_manager()
        result = db_obj.insert_data('expense', [], ['Alice', 30])

        # assert
        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_print.assert_called_once()
        assert result == False

    def test_insert_data_no_values(self,monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('No values to insert'))
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()

        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        monkeypatch.setattr('builtins.print', mock_print)
        db_obj = database_manager()
        result = db_obj.insert_data('expense', ['name', 'age'], [])

        # assert
        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_print.assert_called_once()
        assert result == False

    def test_insert_data_sql_exception(self,monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('No values to insert'))
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()

        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        monkeypatch.setattr('builtins.print', mock_print)
        db_obj = database_manager()
        result = db_obj.insert_data('expense', ['name', 'age'], [])

        # assert
        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_print.assert_called_once()
        assert result == False

    def test_update_data_no_table_name(self,monkeypatch):
        #arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('No table name'))
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()


        #act
        monkeypatch.setattr('db_layer.database_manager.get_connection',lambda : self.mock_connection)
        db_obj = database_manager()
        result=db_obj.update_data(table_name=None,
                           updates={
                               'username': 'username',
                               'role': 'user'
                           }, conditions=['username=?'],
                           parameters=['username'])

        #assert
        self.mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        assert result==False

    def test_update_data_no_updates(self, monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('No table name'))
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()

        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        db_obj = database_manager()
        result = db_obj.update_data(table_name='user',
                                    updates={},
                                    conditions=['username=?'],
                                    parameters=['username'])

        # assert
        assert result == False


    def test_update_data_no_values(self, monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('No values are given'))
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()

        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        db_obj = database_manager()
        result = db_obj.update_data(table_name='user',
                                    updates={
                                    'username': 'username',
                                    'role': 'user'},
                                    conditions=['username=?'],
                                    parameters=[])

        # assert
        assert result == False

    def test_update_data_row_count_0(self, monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock()
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()
        mock_cursor.rowcount=0
        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        db_obj = database_manager()
        result = db_obj.update_data(table_name='user',
                                    updates={
                                        'username': 'username',
                                        'role': 'user'},
                                    conditions=['username=?'],
                                    parameters=['username'])

        # assert
        assert result == False


    def test_update_data_row_count_1(self, monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock()
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()
        mock_cursor.rowcount=1
        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        db_obj = database_manager()
        result = db_obj.update_data(table_name='user',
                                    updates={
                                        'username': 'username',
                                        'role': 'user'},
                                    conditions=['username=?'],
                                    parameters=['username'])

        # assert
        assert result == True

    def test_delete_data_no_table_name(self,monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('An error has occured'))
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()
        mock_cursor.rowcount = 1
        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        db_obj = database_manager()
        result = db_obj.delete_data(table_name=None,
                                    conditions=['username=?'],
                                    parameters=['username'])

        # assert
        assert result == False

    def test_delete_data_no_parameter(self, monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock(side_effect=Exception('An error has occured'))
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()
        mock_cursor.rowcount = 1
        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        db_obj = database_manager()
        result = db_obj.delete_data(table_name=None,
                                    conditions=['username=?'],
                                    parameters=[])

        # assert
        assert result == False


    def test_delete_data_successfull(self,monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock()
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()
        mock_cursor.rowcount = 1
        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        db_obj = database_manager()
        result = db_obj.delete_data(table_name='user',
                                    conditions=['username=?'],
                                    parameters=['username'])

        # assert
        assert result == True


    def test_delete_data_unsuccessfull(self,monkeypatch):
        # arrange
        mock_print = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute = MagicMock()
        self.mock_connection.cursor = MagicMock(return_value=mock_cursor)
        self.mock_connection.commit = MagicMock()
        mock_cursor.rowcount = 0
        # act
        monkeypatch.setattr('db_layer.database_manager.get_connection', lambda: self.mock_connection)
        db_obj = database_manager()
        result = db_obj.delete_data(table_name='user',
                                    conditions=['username=?'],
                                    parameters=['username'])

        # assert
        assert result == False









