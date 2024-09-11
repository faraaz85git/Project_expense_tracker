from unittest.mock import MagicMock
from business_layer.Budget import Budget

class Test_Budget:

    def setup_method(self):
        self.mock_db_manager=MagicMock()

    def test_active_budget_username_None(self,monkeypatch):
        #arrange
        mock_curr_date_str=MagicMock(return_value='2024-09-01')
        self.mock_db_manager.fetch_data=MagicMock(return_value=[])
        #act
        monkeypatch.setattr('business_layer.Budget.database_manager',lambda : self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.curr_date_str',mock_curr_date_str)
        budget=Budget()
        result=budget.active_budget(None)

        #assert
        mock_curr_date_str.assert_called_once()
        self.mock_db_manager.fetch_data.assert_called_once()
        assert result==[]

    def test_active_budget_valid_username_no_budget(self, monkeypatch):
        # arrange
        mock_curr_date_str = MagicMock(return_value='2024-09-01')
        self.mock_db_manager.fetch_data = MagicMock(return_value=[])
        # act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.curr_date_str', mock_curr_date_str)
        budget = Budget()
        result = budget.active_budget('raj')

        # assert
        mock_curr_date_str.assert_called_once()
        self.mock_db_manager.fetch_data.assert_called_once()
        assert result == []

    def test_active_budget_valid_username_has_budget(self, monkeypatch):
        # arrange
        mock_curr_date_str = MagicMock(return_value='2024-09-01')
        self.mock_db_manager.fetch_data = MagicMock(return_value=[(2000,2000,2000,1000,1200,'2024-08-20','2024-09-10')])
        # act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.curr_date_str', mock_curr_date_str)
        budget = Budget()
        result = budget.active_budget('raj')

        # assert
        mock_curr_date_str.assert_called_once()
        self.mock_db_manager.fetch_data.assert_called_once()
        assert result == [(2000,2000,2000,1000,1200,'2024-08-20','2024-09-10')]

    def test_latest_budget_None_username(self,monkeypatch):
        #arrange
        self.mock_db_manager.fetch_data = MagicMock(return_value=[])

        #act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        budget = Budget()
        result = budget.latest_budget(None)

        #assert
        self.mock_db_manager.fetch_data.assert_called_once()
        assert result==None

    def test_latest_budget_valid_username_has_budget(self,monkeypatch):
        #arrange
        self.mock_db_manager.fetch_data = MagicMock(return_value=[(2000,2000,2000,1000,1200,'2024-08-20','2024-08-30')])

        #act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        budget = Budget()
        result = budget.latest_budget('raj')

        #assert
        self.mock_db_manager.fetch_data.assert_called_once()
        assert result==(2000,2000,2000,1000,1200,'2024-08-20','2024-08-30')

    def test_latest_budget_valid_username_no_budget(self,monkeypatch):
        #arrange
        self.mock_db_manager.fetch_data = MagicMock(return_value=[])

        #act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        budget = Budget()
        result = budget.latest_budget('raj')

        #assert
        self.mock_db_manager.fetch_data.assert_called_once()
        assert result==None

    def test_latest_budget_invalid_username(self, monkeypatch):
        # arrange
        self.mock_db_manager.fetch_data = MagicMock(return_value=[])

        # act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        budget = Budget()
        result = budget.latest_budget('invalid')

        # assert
        self.mock_db_manager.fetch_data.assert_called_once()
        assert result == None


    def test_set_budget_no_username_no_prev_budget_end_date_greater(self,monkeypatch):
        # arrange
        self.mock_db_manager.insert_data = MagicMock(return_value=False)
        mock_get_float_input=MagicMock(side_effect=[200.0,200.0,100.0,100.1,100.0])
        mock_get_date_input=MagicMock(side_effect=['2024-09-09','2024-09-09'])

        #act
        monkeypatch.setattr('business_layer.Budget.database_manager',lambda : self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.get_float_input',mock_get_float_input)
        monkeypatch.setattr('business_layer.Budget.get_date_input',mock_get_date_input)
        budget=Budget()
        budget.set_budget(None,None)

        #assert
        mock_get_float_input.assert_any_call('Enter budget for housing category: ')
        mock_get_float_input.assert_any_call('Enter budget for transport category: ')
        mock_get_float_input.assert_any_call('Enter budget for food category: ')
        mock_get_float_input.assert_any_call('Enter budget for clothing category: ')
        mock_get_float_input.assert_any_call('Enter budget for other category: ')
        mock_get_date_input.assert_any_call('Enter start date(yyyy-mm--dd) for budget: ')
        mock_get_date_input.assert_any_call('Enter end date(yyyy-mm--dd) for budget: ')

    def test_set_budget_no_username_no_prev_budget_end_date_smaller_start_date(self,monkeypatch):
        # arrange
        self.mock_db_manager.insert_data = MagicMock(return_value=False)
        mock_get_float_input=MagicMock(side_effect=[200.0,200.0,100.0,100.1,100.0])
        mock_get_date_input=MagicMock(side_effect=['2024-09-09','2024-08-09','2024-09-09'])

        #act
        monkeypatch.setattr('business_layer.Budget.database_manager',lambda : self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.get_float_input',mock_get_float_input)
        monkeypatch.setattr('business_layer.Budget.get_date_input',mock_get_date_input)
        budget=Budget()
        budget.set_budget(None,None)

        #assert
        mock_get_float_input.assert_any_call('Enter budget for housing category: ')
        mock_get_float_input.assert_any_call('Enter budget for transport category: ')
        mock_get_float_input.assert_any_call('Enter budget for food category: ')
        mock_get_float_input.assert_any_call('Enter budget for clothing category: ')
        mock_get_float_input.assert_any_call('Enter budget for other category: ')
        mock_get_date_input.assert_any_call('Enter start date(yyyy-mm--dd) for budget: ')
        mock_get_date_input.assert_any_call('Enter end date(yyyy-mm--dd) for budget: ')

    def test_set_budget_valid_username_no_prev_budget_end_date_greater_start_date(self, monkeypatch):
        # arrange
        self.mock_db_manager.insert_data = MagicMock(return_value=True)
        mock_get_float_input = MagicMock(side_effect=[200.0, 200.0, 100.0, 100.1, 100.0])
        mock_get_date_input = MagicMock(side_effect=['2024-09-09', '2024-09-09'])

        # act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.get_float_input', mock_get_float_input)
        monkeypatch.setattr('business_layer.Budget.get_date_input', mock_get_date_input)
        budget = Budget()
        budget.set_budget('raj', None)

        # assert
        mock_get_float_input.assert_any_call('Enter budget for housing category: ')
        mock_get_float_input.assert_any_call('Enter budget for transport category: ')
        mock_get_float_input.assert_any_call('Enter budget for food category: ')
        mock_get_float_input.assert_any_call('Enter budget for clothing category: ')
        mock_get_float_input.assert_any_call('Enter budget for other category: ')
        mock_get_date_input.assert_any_call('Enter start date(yyyy-mm--dd) for budget: ')
        mock_get_date_input.assert_any_call('Enter end date(yyyy-mm--dd) for budget: ')

    def test_set_budget_valid_username_no_prev_budget_end_date_smaller_start_date(self, monkeypatch):
        # arrange
        self.mock_db_manager.insert_data = MagicMock(return_value=True)
        mock_get_float_input = MagicMock(side_effect=[200.0, 200.0, 100.0, 100.1, 100.0])
        mock_get_date_input = MagicMock(side_effect=['2024-09-09', '2024-08-09','2024-09-10'])

        # act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.get_float_input', mock_get_float_input)
        monkeypatch.setattr('business_layer.Budget.get_date_input', mock_get_date_input)
        budget = Budget()
        budget.set_budget('raj', None)

        # assert
        mock_get_float_input.assert_any_call('Enter budget for housing category: ')
        mock_get_float_input.assert_any_call('Enter budget for transport category: ')
        mock_get_float_input.assert_any_call('Enter budget for food category: ')
        mock_get_float_input.assert_any_call('Enter budget for clothing category: ')
        mock_get_float_input.assert_any_call('Enter budget for other category: ')
        mock_get_date_input.assert_any_call('Enter start date(yyyy-mm--dd) for budget: ')
        mock_get_date_input.assert_any_call('Enter end date(yyyy-mm--dd) for budget: ')

    def test_set_budget_valid_username_has_prev_budget_start_date_greater_prev_end_date(self, monkeypatch):
        # arrange
        self.mock_db_manager.insert_data = MagicMock(return_value=True)
        mock_get_float_input = MagicMock(side_effect=[200.0, 200.0, 100.0, 100.1, 100.0])
        mock_get_date_input = MagicMock(side_effect=['2024-09-09','2024-09-10'])

        # act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.get_float_input', mock_get_float_input)
        monkeypatch.setattr('business_layer.Budget.get_date_input', mock_get_date_input)
        budget = Budget()
        budget.set_budget('raj', '2024-08-10')

        # assert
        mock_get_float_input.assert_any_call('Enter budget for housing category: ')
        mock_get_float_input.assert_any_call('Enter budget for transport category: ')
        mock_get_float_input.assert_any_call('Enter budget for food category: ')
        mock_get_float_input.assert_any_call('Enter budget for clothing category: ')
        mock_get_float_input.assert_any_call('Enter budget for other category: ')
        mock_get_date_input.assert_any_call('Enter start date(yyyy-mm--dd) for budget: ')
        mock_get_date_input.assert_any_call('Enter end date(yyyy-mm--dd) for budget: ')

    def test_set_budget_valid_username_has_prev_budget_start_date_smaller_prev_end_date(self, monkeypatch):
        # arrange
        self.mock_db_manager.insert_data = MagicMock(return_value=True)
        mock_get_float_input = MagicMock(side_effect=[200.0, 200.0, 100.0, 100.1, 100.0])
        mock_get_date_input = MagicMock(side_effect=['2024-08-09','2024-09-10','2024-08-11'])

        # act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.get_float_input', mock_get_float_input)
        monkeypatch.setattr('business_layer.Budget.get_date_input', mock_get_date_input)
        budget = Budget()
        budget.set_budget('raj', '2024-08-10')

        # assert
        mock_get_float_input.assert_any_call('Enter budget for housing category: ')
        mock_get_float_input.assert_any_call('Enter budget for transport category: ')
        mock_get_float_input.assert_any_call('Enter budget for food category: ')
        mock_get_float_input.assert_any_call('Enter budget for clothing category: ')
        mock_get_float_input.assert_any_call('Enter budget for other category: ')
        mock_get_date_input.assert_any_call('Enter start date(yyyy-mm--dd) for budget: ')
        mock_get_date_input.assert_any_call('Enter end date(yyyy-mm--dd) for budget: ')

    def test_set_budget_valid_username_has_prev_budget_start_date_greater_end_date(self, monkeypatch):
        # arrange
        self.mock_db_manager.insert_data = MagicMock(return_value=True)
        mock_get_float_input = MagicMock(side_effect=[200.0, 200.0, 100.0, 100.1, 100.0])
        mock_get_date_input = MagicMock(side_effect=['2024-09-09','2024-08-20','2024-09-20'])

        # act
        monkeypatch.setattr('business_layer.Budget.database_manager', lambda: self.mock_db_manager)
        monkeypatch.setattr('business_layer.Budget.get_float_input', mock_get_float_input)
        monkeypatch.setattr('business_layer.Budget.get_date_input', mock_get_date_input)
        budget = Budget()
        budget.set_budget('raj', '2024-08-10')

        # assert
        mock_get_float_input.assert_any_call('Enter budget for housing category: ')
        mock_get_float_input.assert_any_call('Enter budget for transport category: ')
        mock_get_float_input.assert_any_call('Enter budget for food category: ')
        mock_get_float_input.assert_any_call('Enter budget for clothing category: ')
        mock_get_float_input.assert_any_call('Enter budget for other category: ')
        mock_get_date_input.assert_any_call('Enter start date(yyyy-mm--dd) for budget: ')
        mock_get_date_input.assert_any_call('Enter end date(yyyy-mm--dd) for budget: ')

