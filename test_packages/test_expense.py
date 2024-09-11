
from unittest.mock import MagicMock
from business_layer.Expense import Expense


class Test_Expense:

    def setup_method(self):
        self.db_manager=MagicMock()

    def test_add_expense_no_username(self,monkeypatch):
        #arrange
        self.db_manager.insert_data=MagicMock(return_value=False)

        #act
        monkeypatch.setattr('business_layer.Expense.database_manager',lambda : self.db_manager)
        expense=Expense()
        result=expense.add_expense(None,'2024-08-10','housing',1200,'')

        #assert
        self.db_manager.insert_data.assert_called_once()
        assert result==False

    def test_add_expense_no_date(self,monkeypatch):
        #arrange
        self.db_manager.insert_data=MagicMock(return_value=False)

        #act
        monkeypatch.setattr('business_layer.Expense.database_manager',lambda : self.db_manager)
        expense=Expense()
        result=expense.add_expense('raj',None,'housing',1200,'')

        #assert
        self.db_manager.insert_data.assert_called_once()
        assert result==False

    def test_add_expense_no_category(self,monkeypatch):
        #arrange
        self.db_manager.insert_data=MagicMock(return_value=False)

        #act
        monkeypatch.setattr('business_layer.Expense.database_manager',lambda : self.db_manager)
        expense=Expense()
        result=expense.add_expense('raj','2024-08-01',None,1200,'')

        #assert
        self.db_manager.insert_data.assert_called_once()
        assert result==False

    def test_add_expense_no_amount(self, monkeypatch):
        # arrange
        self.db_manager.insert_data = MagicMock(return_value=False)

        # act
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.add_expense('raj', '2024-08-01', 'food', None, '')

        # assert
        self.db_manager.insert_data.assert_called_once()
        assert result == False

    def test_add_expense_no_description(self, monkeypatch):
        # arrange
        self.db_manager.insert_data = MagicMock(return_value=True)

        # act
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.add_expense('raj', '2024-08-01', 'food', 120, '')

        # assert
        self.db_manager.insert_data.assert_called_once()
        assert result == True

    def test_get_expense_no_username(self,monkeypatch):
        #arrange
        self.db_manager.fetch_data=MagicMock(return_value=[])

        #acgt
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.get_expense(None)

        #assert
        self.db_manager.fetch_data.assert_called_once()
        assert result==[]

    def test_get_expense_valid_username_no_expense(self,monkeypatch):
        #arrange
        self.db_manager.fetch_data=MagicMock(return_value=[])

        #acgt
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.get_expense('raj')

        #assert
        self.db_manager.fetch_data.assert_called_once()
        assert result==[]


    def test_get_expense_valid_username_has_expense(self,monkeypatch):
        #arrange
        self.db_manager.fetch_data=MagicMock(return_value=[(1,'2024-08-01','housing',122,'')])

        #acgt
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.get_expense('raj')

        #assert
        self.db_manager.fetch_data.assert_called_once()
        assert result==[(1,'2024-08-01','housing',122,'')]

    def test_update_expense_no_username(self, monkeypatch):
        # arrange
        self.db_manager.update_data = MagicMock(return_value=False)

        # acgt
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.update_expense(None,{'amount':'1200'},1)

        # assert
        self.db_manager.update_data.assert_called_once()
        assert result == False

    def test_update_expense_valid_username_no_filters(self, monkeypatch):
        # arrange
        self.db_manager.update_data = MagicMock(return_value=False)

        # acgt
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.update_expense('raj',{},1)

        # assert
        assert result == False

    def test_update_expense_valid_username_invalid_amount(self, monkeypatch):
        # arrange
        self.db_manager.update_data = MagicMock(return_value=False)

        # acgt
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.update_expense('raj',{'amount':'abc'},1)

        # assert
        assert result == False

    def test_update_expense_valid_username_validd_amount(self, monkeypatch):
        # arrange
        self.db_manager.update_data = MagicMock(return_value=True)

        # acgt
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.update_expense('raj', {'amount': '100'}, 1)

        # assert
        assert result == True

    def test_update_expense_valid_username_invalid_expense_id(self, monkeypatch):
        # arrange
        self.db_manager.update_data = MagicMock(return_value=False)

        # acgt
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.update_expense('raj', {'amount': '100'}, 'abc')

        # assert
        assert result == False

    def test_update_expense_valid_username_valid_filter_valid_expense_id(self, monkeypatch):
        # arrange
        self.db_manager.update_data = MagicMock(return_value=True)

        # acgt
        monkeypatch.setattr('business_layer.Expense.database_manager', lambda: self.db_manager)
        expense = Expense()
        result = expense.update_expense('raj', {'amount': '100'}, 1)

        # assert
        assert result == True


    def test_delete_expense_invalid_username(self,monkeypatch):
        #arrange
        self.db_manager.delete_data=MagicMock(return_value=False)

        #act
        monkeypatch.setattr('business_layer.Expense.database_manager',lambda : self.db_manager)
        expense = Expense()
        result = expense.delete_expense('invalid_username', 1)

        #assert
        self.db_manager.delete_data.assert_called_once()
        assert result==None

    def test_delete_expense_invalid_expense_id(self,monkeypatch):
        #arrange
        self.db_manager.delete_data=MagicMock(return_value=False)

        #act
        monkeypatch.setattr('business_layer.Expense.database_manager',lambda : self.db_manager)
        expense = Expense()
        result = expense.delete_expense('valid_username', 'abc')

        #assert
        self.db_manager.delete_data.assert_called_once()
        assert result==None

    def test_delete_expense_valid_username_valid_expense_id(self,monkeypatch):
        #arrange
        self.db_manager.delete_data=MagicMock(return_value=True)

        #act
        monkeypatch.setattr('business_layer.Expense.database_manager',lambda : self.db_manager)
        expense = Expense()
        result = expense.delete_expense('valid_username', 1)

        #assert
        self.db_manager.delete_data.assert_called_once()
        assert result==None


