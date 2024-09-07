from unittest.mock import MagicMock
from ui_layer.user_menu import user_menu



class Test_user_menu:

    def setup_method(self):
        self.mock_user=MagicMock()
        self.mock_main_menu=MagicMock()

    def test_role_user(self,monkeypatch):
        mock_input=MagicMock(return_value='9')
        self.mock_user.role='user'

        #act
        monkeypatch.setattr('builtins.input',mock_input)
        user_menu(self.mock_user,self.mock_main_menu)

        #assert
        self.mock_main_menu.assert_called_once()

    def test_role_admin(self,monkeypatch):
        mock_input = MagicMock(return_value='9')
        self.mock_user.role = 'admin'

        # act
        monkeypatch.setattr('builtins.input', mock_input)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_main_menu.assert_called_once()

    def test_choice_1_valid_amount(self,monkeypatch):
        mock_input = MagicMock(side_effect=['1','9.2',' ','9'])
        self.mock_user.role = 'user'
        self.mock_user.add_expense1=MagicMock(return_value=True)
        mock_get_date_input=MagicMock()
        mock_ask_category=MagicMock()

        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.get_date_input',mock_get_date_input)
        monkeypatch.setattr('ui_layer.user_menu.ask_category',mock_ask_category)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_user.add_expense1.assert_called_once()
        self.mock_main_menu.assert_called_once()

    def test_choice_1_invalid_amount(self,monkeypatch):
        mock_input = MagicMock(side_effect=['1','abc','9'])
        self.mock_user.role = 'user'
        self.mock_user.add_expense1=MagicMock(return_value=True)
        mock_get_date_input=MagicMock()
        mock_ask_category=MagicMock()

        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.get_date_input',mock_get_date_input)
        monkeypatch.setattr('ui_layer.user_menu.ask_category',mock_ask_category)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_user.add_expense1.assert_not_called()
        self.mock_main_menu.assert_called_once()


    def test_choice_1_invalid_amount_failed(self,monkeypatch):
        mock_input = MagicMock(side_effect=['1', '9.2', ' ', '9'])
        self.mock_user.role = 'user'
        self.mock_user.add_expense1 = MagicMock(return_value=False)
        mock_get_date_input = MagicMock()
        mock_ask_category = MagicMock()

        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.get_date_input', mock_get_date_input)
        monkeypatch.setattr('ui_layer.user_menu.ask_category', mock_ask_category)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_user.add_expense1.assert_called_once()
        self.mock_main_menu.assert_called_once()

    def test_choice_2_has_data(self,monkeypatch):
        mock_input = MagicMock(side_effect=['2','9'])
        self.mock_user.role = 'user'
        self.mock_user.show_all_expense2 = MagicMock(return_value=[('1','housing','2024-08-01','209','')])
        mock_display=MagicMock()
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.display',mock_display)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_user.show_all_expense2.assert_called_once()
        mock_display.assert_called_once_with([('1','housing','2024-08-01','209','')])
        self.mock_main_menu.assert_called_once()

    def test_choice_2_no_data(self,monkeypatch):
        mock_input = MagicMock(side_effect=['2','9'])
        self.mock_user.role = 'user'
        self.mock_user.show_all_expense2 = MagicMock(return_value=[])
        mock_display=MagicMock()
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.display',mock_display)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_user.show_all_expense2.assert_called_once()
        self.mock_main_menu.assert_called_once()

    def test_choice_3_has_data_invlid_id(self, monkeypatch):
        mock_input = MagicMock(side_effect=['3','a', '9'])
        self.mock_user.role = 'user'
        self.mock_user.show_all_expense2 = MagicMock(return_value=[('1','housing','2024-08-01','209','')])
        mock_display = MagicMock()
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.display', mock_display)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_user.show_all_expense2.assert_called_once()
        mock_display.assert_called_once_with([('1','housing','2024-08-01','209','')])
        self.mock_main_menu.assert_called_once()

    def test_choice_3_has_data_valid_id_sucess(self, monkeypatch):
        mock_input = MagicMock(side_effect=['3','1', '9'])
        self.mock_user.role = 'user'
        self.mock_user.show_all_expense2 = MagicMock(return_value=[('1','housing','2024-08-01','209','')])
        self.mock_user.update_expense2=MagicMock(return_value=True)
        mock_display = MagicMock()
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.display', mock_display)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_user.show_all_expense2.assert_called_once()
        mock_display.assert_called_once_with([('1','housing','2024-08-01','209','')])
        self.mock_user.update_expense2.assert_called_once_with(1)
        self.mock_main_menu.assert_called_once()

    def test_choice_3_has_data_valid_id_failed(self, monkeypatch):
        mock_input = MagicMock(side_effect=['3','2', '9'])
        self.mock_user.role = 'user'
        self.mock_user.show_all_expense2 = MagicMock(return_value=[('1','housing','2024-08-01','209','')])
        self.mock_user.update_expense2=MagicMock(return_value=False)
        mock_display = MagicMock()
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.display', mock_display)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_user.show_all_expense2.assert_called_once()
        mock_display.assert_called_once_with([('1','housing','2024-08-01','209','')])
        self.mock_user.update_expense2.assert_called_once_with(2)
        self.mock_main_menu.assert_called_once()

    def test_choice_3_no_data(self, monkeypatch):
        mock_input = MagicMock(side_effect=['3','9'])
        self.mock_user.role = 'user'
        self.mock_user.show_all_expense2 = MagicMock(return_value=[])
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_user.show_all_expense2.assert_called_once()
        self.mock_main_menu.assert_called_once()

    def test_choice_4_has_data_valid_id(self,monkeypatch):
        mock_input=MagicMock(side_effect=['4','1','9'])
        mock_display=MagicMock()
        self.mock_user.show_all_expense2=MagicMock(return_value=[('1','housing','2024-08-01','209','')])
        self.mock_user.delete_expense2=MagicMock()

        #act
        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('ui_layer.user_menu.display',mock_display)

        user_menu(self.mock_user,self.mock_main_menu)

        #assert
        self.mock_user.show_all_expense2.assert_called_once()
        mock_display.assert_called_once_with([('1','housing','2024-08-01','209','')])
        self.mock_user.delete_expense2.assert_called_once_with(1)
        self.mock_main_menu.assert_called_once()

    def test_choice_4_has_data_invalid_id(self,monkeypatch):
        mock_input=MagicMock(side_effect=['4','a','9'])
        mock_display=MagicMock()
        self.mock_user.show_all_expense2=MagicMock(return_value=[('1','housing','2024-08-01','209','')])
        self.mock_user.delete_expense2=MagicMock()

        #act
        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('ui_layer.user_menu.display',mock_display)

        user_menu(self.mock_user,self.mock_main_menu)

        #assert
        self.mock_user.show_all_expense2.assert_called_once()
        mock_display.assert_called_once_with([('1', 'housing', '2024-08-01', '209', '')])
        self.mock_main_menu.assert_called_once()

    def test_choice_4_no_data(self, monkeypatch):
        mock_input = MagicMock(side_effect=['4', '9'])
        mock_display = MagicMock()
        self.mock_user.show_all_expense2 = MagicMock(return_value=[])


        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.display', mock_display)

        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_main_menu.assert_called_once()

    def test_choice_5(self,monkeypatch):
        mock_input=MagicMock(side_effect=['5','y','n','y','n','n','9'])
        self.mock_user.show_expense_by_category2=MagicMock()

        #act
        monkeypatch.setattr('builtins.input',mock_input)
        user_menu(self.mock_user,self.mock_main_menu)

        #assert
        self.mock_user.show_expense_by_category2.assert_called_once_with({'transport':'y',
                                                                          'food':'y'})
        self.mock_main_menu.assert_called_once()


    def test_choice_6(self,monkeypatch):
        mock_input=MagicMock(side_effect=['6','9'])
        self.mock_user.set_budget_by_category2=MagicMock()

        #act
        monkeypatch.setattr('builtins.input',mock_input)
        user_menu(self.mock_user,self.mock_main_menu)
        #assert
        self.mock_user.set_budget_by_category2.assert_called_once()

        self.mock_main_menu.assert_called_once()

    def test_choice_7(self, monkeypatch):
        mock_input = MagicMock(side_effect=['7', '9'])
        self.mock_user.show_budget_status_by_category2 = MagicMock(return_value=[{},{}])
        mock_display_budget_status=MagicMock()
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.user_menu.display_budget_status', mock_display_budget_status)
        user_menu(self.mock_user, self.mock_main_menu)
        # assert
        self.mock_user.show_budget_status_by_category2.assert_called_once()
        mock_display_budget_status.assert_called_once_with({},{})
        self.mock_main_menu.assert_called_once()

    def test_choice_8(self,monkeypatch):
        mock_input = MagicMock(side_effect=['8', '9'])
        self.mock_user.plot_expense1= MagicMock()

        # act
        monkeypatch.setattr('builtins.input', mock_input)
        user_menu(self.mock_user, self.mock_main_menu)

        #assert
        self.mock_user.plot_expense1.assert_called_once()
        self.mock_main_menu.assert_called_once()

    def test_choice_9(self,monkeypatch):
        mock_input = MagicMock(side_effect=['9'])

        # act
        monkeypatch.setattr('builtins.input', mock_input)
        user_menu(self.mock_user, self.mock_main_menu)

        #assert
        self.mock_main_menu.assert_called_once()

    def test_choice_10(self, monkeypatch):
        mock_input = MagicMock(side_effect=['10','9'])

        # act
        monkeypatch.setattr('builtins.input', mock_input)
        user_menu(self.mock_user, self.mock_main_menu)

        # assert
        self.mock_main_menu.assert_called_once()