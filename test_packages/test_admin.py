from unittest.mock import MagicMock
from business_layer.Admin import Admin


class TestAdmin:

    def setup_method(self):
        self.mock_expense=MagicMock()
        self.mock_db_manager=MagicMock()

    def test_show_all_user1_has_user(self,monkeypatch):
        self.mock_db_manager.fetch_data=MagicMock(return_value=[('1','user1','user')])

        #act
        monkeypatch.setattr('business_layer.user.database_manager',lambda :self.mock_db_manager)
        monkeypatch.setattr('business_layer.user.Expense',lambda : self.mock_expense)
        admin=Admin('Raj','sddsa','admin')
        admin.show_all_user1()

        #assert
        self.mock_db_manager.fetch_data.assert_called_once()

    def test_show_all_user1_no_user(self,monkeypatch):
        #arrange
        self.mock_db_manager.fetch_data=MagicMock(return_value=[])

        #act
        monkeypatch.setattr('business_layer.user.database_manager',lambda :self.mock_db_manager)
        monkeypatch.setattr('business_layer.user.Expense',lambda : self.mock_expense)
        admin=Admin('Raj','sddsa','admin')
        admin.show_all_user1()

        #assert
        self.mock_db_manager.fetch_data.assert_called_once()

    def test_delete_user1_valid_id_deleted(self,monkeypatch):
        #arrange
        self.mock_db_manager.fetch_data = MagicMock(return_value=[])
        mock_show_all_user1=MagicMock()
        mock_input=MagicMock(return_value='1')
        self.mock_db_manager.delete_data=MagicMock(return_value=True)
        # act
        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('business_layer.user.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.user.Expense', lambda: self.mock_expense)
        monkeypatch.setattr('business_layer.Admin.Admin.show_all_user1',mock_show_all_user1)
        admin = Admin('Raj', 'sddsa', 'admin')
        admin.delete_user1()

        # assert
        mock_show_all_user1.assert_called_once()
        self.mock_db_manager.delete_data.assert_called_once()

    def test_delete_user1_valid_id_not_deleted(self, monkeypatch):
        # arrange
        self.mock_db_manager.fetch_data = MagicMock(return_value=[])
        mock_show_all_user1 = MagicMock()
        mock_input = MagicMock(return_value='1')
        self.mock_db_manager.delete_data = MagicMock(return_value=False)
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('business_layer.user.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.user.Expense', lambda: self.mock_expense)
        monkeypatch.setattr('business_layer.Admin.Admin.show_all_user1', mock_show_all_user1)
        admin = Admin('Raj', 'sddsa', 'admin')
        admin.delete_user1()

        # assert
        mock_show_all_user1.assert_called_once()
        self.mock_db_manager.delete_data.assert_called_once()

    def test_delete_user1_invalid_id(self, monkeypatch):
        # arrange
        self.mock_db_manager.fetch_data = MagicMock(return_value=[])
        mock_show_all_user1 = MagicMock()
        mock_input = MagicMock(return_value='a')

        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('business_layer.user.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.user.Expense', lambda: self.mock_expense)
        monkeypatch.setattr('business_layer.Admin.Admin.show_all_user1', mock_show_all_user1)
        admin = Admin('Raj', 'sddsa', 'admin')
        result=admin.delete_user1()

        # assert
        mock_show_all_user1.assert_called_once()
        assert result==False

    def test_show_all_user_expenses1_has_data(self,monkeypatch):
        # arrange
        self.mock_db_manager.fetch_data = MagicMock(return_value=[('1','user1','2024-08-01','housing',1222,'')])

        # act
        monkeypatch.setattr('business_layer.user.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.user.Expense', lambda: self.mock_expense)
        admin = Admin('Raj', 'sddsa', 'admin')
        result = admin.show_all_users_expenses1()

        # assert
        self.mock_db_manager.fetch_data.assert_called_once()
        assert result == [('1','user1','2024-08-01','housing',1222,'')]

    def test_show_all_user_expenses1_no_data(self, monkeypatch):
        # arrange
        self.mock_db_manager.fetch_data = MagicMock(return_value=[])

        # act
        monkeypatch.setattr('business_layer.user.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.user.Expense', lambda: self.mock_expense)
        admin = Admin('Raj', 'sddsa', 'admin')
        result = admin.show_all_users_expenses1()

        # assert
        self.mock_db_manager.fetch_data.assert_called_once()
        assert result == None
