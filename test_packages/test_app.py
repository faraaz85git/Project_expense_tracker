import pytest
from unittest.mock import MagicMock
from ui_layer.app import main_menu,handle_login,handle_signup


'''---------------Test fucntion for main_menu-------------'''


def test_main_menu_choice_1(monkeypatch):
  mock_print=MagicMock(return_value=None)
  mock_input=MagicMock(return_value='1')
  mock_handle_login=MagicMock(return_value=None)
  mock_handle_signup=MagicMock(return_value=None)
  mock_close_connection=MagicMock(return_value=None)
  mock_main_menu=MagicMock(return_value=None)
  mock_exit=MagicMock(return_value=None)

  monkeypatch.setattr('builtins.print',mock_print)
  monkeypatch.setattr('builtins.input',mock_input)
  monkeypatch.setattr('ui_layer.app.handle_login',mock_handle_login)
  monkeypatch.setattr('ui_layer.app.handle_signup',mock_handle_signup)
  monkeypatch.setattr('ui_layer.app.close_connection',mock_close_connection)
  monkeypatch.setattr('builtins.exit',mock_exit)
  monkeypatch.setattr('ui_layer.app.main_menu',mock_main_menu)



  main_menu()

  mock_print.assert_called()
  mock_input.assert_called_once_with('Your choice: ')
  mock_handle_login.assert_called_once()
  mock_handle_signup.assert_not_called()
  mock_close_connection.assert_not_called()
  mock_exit.assert_not_called()
  mock_main_menu.assert_not_called()



def test_main_menu_choice_2(monkeypatch):
  mock_print = MagicMock()
  mock_input = MagicMock(return_value='2')
  mock_handle_signup = MagicMock()

  monkeypatch.setattr('builtins.print',mock_print)
  monkeypatch.setattr('builtins.input',mock_input)
  monkeypatch.setattr('ui_layer.app.handle_signup',mock_handle_signup)

  main_menu()

  mock_handle_signup.assert_called_once()


def test_main_menu_choice_3(monkeypatch):
  mock_print = MagicMock()
  mock_input = MagicMock(return_value='3')
  mock_close_connection = MagicMock()
  mock_exit=MagicMock()

  monkeypatch.setattr('builtins.print',mock_print)
  monkeypatch.setattr('builtins.input',mock_input)
  monkeypatch.setattr('ui_layer.app.close_connection',mock_close_connection)
  monkeypatch.setattr('builtins.exit',mock_exit)

  main_menu()

  mock_close_connection.assert_called_once()

'''------------------------------------------------------'''

'''---------------------test function for handle_login-------------------'''

def test_handle_login_missing_input(monkeypatch):
    mock_input = MagicMock(side_effect=['', ''])
    mock_print = MagicMock()
    mock_main_menu = MagicMock()
    monkeypatch.setattr('builtins.input', mock_input)
    monkeypatch.setattr('builtins.print', mock_print)
    monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)

    handle_login()

    mock_main_menu.assert_called_once()


def test_handle_login_valid_input_user(monkeypatch):
  mock_input = MagicMock(side_effect=['Valid_user', 'valid_password'])


  mock_auth = MagicMock()
  mock_auth.login1=MagicMock(return_value=('valid_user', 'valid_password', 'user'))

  mock_print = MagicMock()
  mock_User = MagicMock()

  mock_Admin = MagicMock()
  mock_user_menu = MagicMock()
  mock_admin_menu = MagicMock()
  mock_main_menu = MagicMock()

  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('builtins.print', mock_print)
  monkeypatch.setattr('ui_layer.app.Auth', lambda: mock_auth)
  monkeypatch.setattr('ui_layer.app.User', lambda *args: mock_User)
  monkeypatch.setattr('ui_layer.app.Admin', lambda *args: mock_Admin)
  monkeypatch.setattr('ui_layer.app.user_menu', mock_user_menu)
  monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)


  handle_login()

  mock_auth.login1.assert_called_once()
  mock_user_menu.assert_called_once_with(mock_User,mock_main_menu)

def test_handle_login_valid_input_admin(monkeypatch):
  mock_input = MagicMock(side_effect=['Valid_user', 'valid_password'])


  mock_auth = MagicMock()
  mock_auth.login1=MagicMock(return_value=('valid_user', 'valid_password', 'admin'))

  mock_print = MagicMock()
  mock_User = MagicMock()

  mock_Admin = MagicMock()
  mock_user_menu = MagicMock()
  mock_admin_menu = MagicMock()
  mock_main_menu = MagicMock()

  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('builtins.print', mock_print)
  monkeypatch.setattr('ui_layer.app.Auth', lambda: mock_auth)
  monkeypatch.setattr('ui_layer.app.User', lambda *args: mock_User)
  monkeypatch.setattr('ui_layer.app.Admin', lambda *args: mock_Admin)
  monkeypatch.setattr('ui_layer.app.admin_menu', mock_admin_menu)
  monkeypatch.setattr('ui_layer.app.user_menu',mock_user_menu)
  monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)


  handle_login()

  mock_auth.login1.assert_called_once()
  mock_admin_menu.assert_called_once_with(mock_Admin,mock_main_menu,mock_user_menu)



def test_handle_login_invalid_input(monkeypatch):
  mock_input = MagicMock(side_effect=['invalid_user', 'invalid_password'])
  mock_auth = MagicMock()

  mock_auth.login1 = MagicMock(return_value=None)
  mock_print = MagicMock()

  mock_main_menu = MagicMock()

  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('ui_layer.app.Auth', lambda: mock_auth)
  monkeypatch.setattr('builtins.print', mock_print)
  monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)

  handle_login()


  mock_auth.login1.assert_called_once_with('invalid_user', 'invalid_password')

  mock_main_menu.assert_called_once()

'''-----------------------------------------------------'''

"""------------------------test function for handle_signup-------------------"""

def test_handle_signup_missing_input(monkeypatch):

    mock_input=MagicMock(side_effect=['','',''])
    mock_print=MagicMock()
    mock_main_menu=MagicMock()


    monkeypatch.setattr('builtins.input',mock_input)
    monkeypatch.setattr('builtins.print',mock_print)
    monkeypatch.setattr('ui_layer.app.main_menu',mock_main_menu)

    handle_signup()

    mock_main_menu.assert_called_once()

def test_handle_signup_input_role_1(monkeypatch):
  mock_input=MagicMock(side_effect=['valid_user','valid_password','1'])
  mock_auth=MagicMock()
  mock_auth.sign_up1=MagicMock(return_value=True)
  mock_print=MagicMock()
  mock_main_menu=MagicMock()

  monkeypatch.setattr('builtins.input',mock_input)
  monkeypatch.setattr('ui_layer.app.Auth',lambda :mock_auth)
  monkeypatch.setattr('builtins.print',mock_print)
  monkeypatch.setattr('ui_layer.app.main_menu',mock_main_menu)

  handle_signup()


  mock_auth.sign_up1.assert_called_once_with('valid_user','valid_password','user')
  mock_main_menu.assert_called_once()



def test_handle_signup_input_role_2(monkeypatch):
  mock_input=MagicMock(side_effect=['valid_user','valid_password','2'])
  mock_auth=MagicMock()
  mock_auth.sign_up1=MagicMock(return_value=True)
  mock_print=MagicMock()
  mock_main_menu=MagicMock()

  monkeypatch.setattr('builtins.input',mock_input)
  monkeypatch.setattr('ui_layer.app.Auth',lambda :mock_auth)
  monkeypatch.setattr('builtins.print',mock_print)
  monkeypatch.setattr('ui_layer.app.main_menu',mock_main_menu)

  handle_signup()


  mock_auth.sign_up1.assert_called_once_with('valid_user','valid_password','admin')
  mock_main_menu.assert_called_once()

def test_handle_signup_input_role_2_failed(monkeypatch):
  mock_input=MagicMock(side_effect=['valid_user','valid_password','2'])
  mock_auth=MagicMock()
  mock_auth.sign_up1=MagicMock(return_value=False)
  mock_print=MagicMock()
  mock_main_menu=MagicMock()

  monkeypatch.setattr('builtins.input',mock_input)
  monkeypatch.setattr('ui_layer.app.Auth',lambda :mock_auth)
  monkeypatch.setattr('builtins.print',mock_print)
  monkeypatch.setattr('ui_layer.app.main_menu',mock_main_menu)

  handle_signup()

  mock_print.assert_any_call('username exists')
  mock_auth.sign_up1.assert_called_once_with('valid_user','valid_password','admin')
  mock_main_menu.assert_called_once()
