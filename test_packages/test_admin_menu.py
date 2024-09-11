from ui_layer.admin_menu import admin_menu
from unittest.mock import MagicMock
from business_layer.user import User

class Test_admin_menu:
    def setup_method(self):
        self.mock_user=MagicMock()
        self.mock_user.show_all_user1=MagicMock(return_value=None)
        self.mock_user.show_all_users_expenses1=MagicMock(return_value=None)
        self.mock_user.delete_user1=MagicMock(return_value=None)

        self.mock_main_menu=MagicMock(return_value=1)
        self.mock_user_menu=MagicMock()
    def test_admin_menu_choice_1(self,monkeypatch):
        mock_input=MagicMock(side_effect=['1','3'])
        mock_myfun=MagicMock()
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('ui_layer.admin_menu.myfun',mock_myfun)
        admin_menu(self.mock_user,self.mock_main_menu,self.mock_user_menu)

        #assert
        self.mock_user_menu.assert_called_once_with(self.mock_user,mock_myfun)


    def test_admin_menu_choice_2_1(self,monkeypatch):
        mock_input=MagicMock(side_effect=['2','1','3','3'])
        mock_myfun=MagicMock()
        self.mock_user.username='User1'
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('ui_layer.admin_menu.myfun',mock_myfun)
        admin_menu(self.mock_user,self.mock_main_menu,self.mock_user_menu)

        #assert
        # self.mock_user_menu.assert_called_once_with(self.mock_user,mock_myfun)
        self.mock_user.show_all_user1.assert_called_once()
        self.mock_main_menu.assert_called_once()

    def test_admin_menu_choice_2_2(self,monkeypatch):
        mock_input=MagicMock(side_effect=['2','2','3','3'])
        mock_myfun=MagicMock()
        self.mock_user.username='User1'
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('ui_layer.admin_menu.myfun',mock_myfun)
        admin_menu(self.mock_user,self.mock_main_menu,self.mock_user_menu)

        #assert
        # self.mock_user_menu.assert_called_once_with(self.mock_user,mock_myfun)
        self.mock_main_menu.assert_called_once()
        self.mock_user.show_all_users_expenses1.assert_called_once()

    def test_admin_menu_choice_2_3(self,monkeypatch):
        mock_input=MagicMock(side_effect=['2','3','3'])
        mock_myfun=MagicMock()
        self.mock_user.username='User1'
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('ui_layer.admin_menu.myfun',mock_myfun)
        admin_menu(self.mock_user,self.mock_main_menu,self.mock_user_menu)

        #assert
        self.mock_main_menu.assert_called_once()

    def test_admin_menu_choice_2_4(self,monkeypatch):
        mock_input=MagicMock(side_effect=['2','4','3','3'])
        mock_myfun=MagicMock()
        self.mock_user.username='User1'
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('ui_layer.admin_menu.myfun',mock_myfun)
        admin_menu(self.mock_user,self.mock_main_menu,self.mock_user_menu)

        #assert
        self.mock_main_menu.assert_called_once()

    def test_admin_menu_choice_3(self,monkeypatch):
        mock_input = MagicMock(return_value='3')
        mock_myfun = MagicMock()
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.admin_menu.myfun', mock_myfun)
        admin_menu(self.mock_user, self.mock_main_menu, self.mock_user_menu)

        # assert
        self.mock_main_menu.assert_called_once()

    def test_admin_menu_choice_unknown(self,monkeypatch):
        mock_input = MagicMock(side_effect=['5','3'])
        mock_myfun = MagicMock()
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('ui_layer.admin_menu.myfun', mock_myfun)
        admin_menu(self.mock_user, self.mock_main_menu, self.mock_user_menu)

        # assert
        self.mock_main_menu.assert_called_once_with()
