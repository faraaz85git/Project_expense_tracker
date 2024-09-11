
import pytest
from unittest.mock import MagicMock
from business_layer.user import User

class TestUser():
    def setup_method(self):
        self.expense=MagicMock()
        self.db_manager=MagicMock()

    def test_add_expense1_invalid_username(self,monkeypatch):
        #arrange
        self.expense.add_expense=MagicMock(return_value=False)

        #act
        monkeypatch.setattr('business_layer.user.Expense',lambda : self.expense)
        user_obj=User('invalid_username','valid_password','valid_role')
        result=user_obj.add_expense1('2024-08-01','housing',1200,'no description')

        #assert
        assert result==False

    # def test_add_expense1_invalid_amount(self, monkeypatch):
    #
    #     mock_get_date_input = MagicMock(return_value='2024-08-01')
    #     mock_ask_category = MagicMock(return_value='housing')
    #     mock_input = MagicMock(side_effect=['ab', ''])
    #
    #
    #     monkeypatch.setattr('business_layer.user.get_date_input', mock_get_date_input)
    #     monkeypatch.setattr('business_layer.user.ask_category', mock_ask_category)
    #     monkeypatch.setattr('builtins.input', mock_input)
    #
    #     user_obj = User('username', 'password', 'role')
    #     result = user_obj.add_expense1()
    #
    #     assert result == None
    #
    # def test_show_all_expense1_has_data(self,monkeypatch):
    #     self.db_manager.fetch_data=MagicMock(return_value=[('expense_id','date','category','amount','description')])
    #     mock_print=MagicMock()
    #
    #     monkeypatch.setattr('business_layer.user.database_manager',lambda : self.db_manager)
    #     monkeypatch.setattr('builtins.print',mock_print)
    #
    #     user_obj=User('username','password','role')
    #     result=user_obj.show_all_expense1()
    #
    #     assert result==[('expense_id','date','category','amount','description')]
    #
    # def test_show_all_expense1_no_data(self,monkeypatch):
    #     self.db_manager.fetch_data = MagicMock(return_value=[])
    #     mock_print = MagicMock()
    #
    #     monkeypatch.setattr('business_layer.user.database_manager', lambda: self.db_manager)
    #     monkeypatch.setattr('builtins.print', mock_print)
    #
    #     user_obj = User('username', 'password', 'role')
    #     result = user_obj.show_all_expense1()
    #
    #     assert result == None
    #
    # def test_update_expense1_no_data(self,monkeypatch):
    #
    #     mock_print = MagicMock()
    #     mock_show_all_expense1=MagicMock(return_value=None)
    #     monkeypatch.setattr('builtins.print', mock_print)
    #     monkeypatch.setattr('business_layer.user.User.show_all_expense1',mock_show_all_expense1)
    #
    #     user_obj = User('username', 'password', 'role')
    #     result = user_obj.update_expense1()
    #
    #     assert result == None
    #
    # def test_update_expense1_has_data_invalid_id(self,monkeypatch):
    #     mock_print = MagicMock()
    #     mock_show_all_expense1 = MagicMock(return_value=[('1','2024-08-01','housing',122,'description')])
    #     mock_input=MagicMock(return_value='abc')
    #     monkeypatch.setattr('builtins.print', mock_print)
    #     monkeypatch.setattr('business_layer.user.User.show_all_expense1', mock_show_all_expense1)
    #     monkeypatch.setattr('builtins.input',mock_input)
    #
    #     user_obj = User('username', 'password', 'role')
    #     result = user_obj.update_expense1()
    #
    #     assert result == None
    #
    # def test_update_expense1_has_data_valid_id(self,monkeypatch):
    #     self.db_manager.update_data=MagicMock(return_value=True)
    #     mock_print = MagicMock()
    #     mock_update_category=MagicMock(return_value='')
    #     mock_show_all_expense1 = MagicMock(return_value=[('1','2024-08-01','housing',122,'description')])
    #     mock_input=MagicMock(side_effect=['1','2024-08-01','1.2','description'])
    #
    #     monkeypatch.setattr('builtins.print', mock_print)
    #     monkeypatch.setattr('business_layer.user.User.show_all_expense1', mock_show_all_expense1)
    #     monkeypatch.setattr('builtins.input',mock_input)
    #     monkeypatch.setattr('business_layer.user.update_category',mock_update_category)
    #     monkeypatch.setattr('business_layer.user.database_manager',lambda : self.db_manager)
    #
    #     user_obj = User('username', 'password', 'role')
    #     result = user_obj.update_expense1()
    #
    #     assert result == None
    #     # cd..
    #





