from unittest.mock import MagicMock
from app import main_menu,handle_login,handle_signup


'''---------------Test fucntion for main_menu-------------'''


def test_main_menu_choice_1(monkeypatch):
  #arrange
  mock_print=MagicMock()
  mock_input=MagicMock(return_value='1')
  mock_handle_login=MagicMock()

  #act
  monkeypatch.setattr('builtins.print',mock_print)
  monkeypatch.setattr('builtins.input',mock_input)
  monkeypatch.setattr('ui_layer.app.handle_login',mock_handle_login)
  main_menu()
  #assert
  mock_handle_login.assert_called_once()




def test_main_menu_choice_2(monkeypatch):
  # arrange
  mock_print = MagicMock()
  mock_input = MagicMock(return_value='2')
  mock_handle_signup = MagicMock()

  # act
  monkeypatch.setattr('builtins.print', mock_print)
  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('ui_layer.app.handle_signup', mock_handle_signup)
  main_menu()
  # assert

  mock_handle_signup.assert_called_once()


def test_main_menu_choice_3(monkeypatch):
  # arrange
  mock_print = MagicMock()
  mock_input = MagicMock(return_value='3')
  mock_close_connection = MagicMock()
  mock_exit=MagicMock()

  # act
  monkeypatch.setattr('builtins.print', mock_print)
  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('ui_layer.app.close_connection', mock_close_connection)
  monkeypatch.setattr('builtins.exit',mock_exit)
  main_menu()
  # assert
  mock_close_connection.assert_called_once()
  mock_exit.assert_called_once()


def test_main_menu_choice_4(monkeypatch):
  # arrange
  mock_print = MagicMock()
  mock_input = MagicMock(side_effect=['4','3'])
  mock_close_connection = MagicMock()
  mock_exit=MagicMock()

  # act
  monkeypatch.setattr('builtins.print', mock_print)
  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('ui_layer.app.close_connection', mock_close_connection)
  monkeypatch.setattr('builtins.exit',mock_exit)
  main_menu()
  # assert
  mock_close_connection.assert_called_once()
  mock_exit.assert_called_once()

'''------------------------------------------------------'''

'''---------------------test function for handle_login-------------------'''

def test_handle_login_missing_input(monkeypatch):
    #arrange
    mock_input = MagicMock(side_effect=['', ''])
    mock_print = MagicMock()
    mock_main_menu = MagicMock()
    #act
    monkeypatch.setattr('builtins.input', mock_input)
    monkeypatch.setattr('builtins.print', mock_print)
    monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)

    handle_login()
    #assert
    mock_main_menu.assert_called_once()


def test_handle_login_valid_input_user(monkeypatch):
  #arrange
  mock_input = MagicMock(side_effect=['Valid_user', 'valid_password'])
  mock_auth = MagicMock()
  mock_auth.login1=MagicMock(return_value=('valid_user', 'valid_password', 'user'))
  mock_User = MagicMock()
  mock_user_menu = MagicMock()
  mock_main_menu = MagicMock()
  #act
  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('ui_layer.app.Auth', lambda: mock_auth)
  monkeypatch.setattr('ui_layer.app.User', lambda *args: mock_User)
  monkeypatch.setattr('ui_layer.app.user_menu', mock_user_menu)
  monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)
  handle_login()
  #assert
  mock_auth.login1.assert_called_once()
  mock_user_menu.assert_called_once_with(mock_User,mock_main_menu)

def test_handle_login_valid_input_admin(monkeypatch):
  mock_input = MagicMock(side_effect=['Valid_user', 'valid_password'])
  mock_auth = MagicMock()
  mock_auth.login1=MagicMock(return_value=('valid_user', 'valid_password', 'admin'))
  mock_Admin = MagicMock()
  mock_user_menu = MagicMock()
  mock_admin_menu = MagicMock()
  mock_main_menu = MagicMock()

  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('ui_layer.app.Auth', lambda: mock_auth)
  monkeypatch.setattr('ui_layer.app.Admin', lambda *args: mock_Admin)
  monkeypatch.setattr('ui_layer.app.admin_menu', mock_admin_menu)
  monkeypatch.setattr('ui_layer.app.user_menu',mock_user_menu)
  monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)


  handle_login()

  mock_auth.login1.assert_called_once()
  mock_admin_menu.assert_called_once_with(mock_Admin,mock_main_menu,mock_user_menu)



def test_handle_login_invalid_input(monkeypatch):
  #arrange
  mock_input = MagicMock(side_effect=['invalid_user', 'invalid_password'])
  mock_auth = MagicMock()
  mock_auth.login1 = MagicMock(return_value=None)
  mock_print = MagicMock()
  mock_main_menu = MagicMock()
  #act
  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('ui_layer.app.Auth', lambda: mock_auth)
  monkeypatch.setattr('builtins.print', mock_print)
  monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)
  handle_login()

  #assert
  mock_auth.login1.assert_called_once_with('invalid_user', 'invalid_password')

  mock_main_menu.assert_called_once()

'''-----------------------------------------------------'''

"""------------------------test function for handle_signup-------------------"""

def test_handle_signup_invalid_username_invalid_password(monkeypatch):
    #arrange
    mock_input=MagicMock(side_effect=['invlaid_username','invalid_password'])
    mock_print=MagicMock()
    mock_main_menu=MagicMock()
    mock_validate_username=MagicMock(return_value=False)
    mock_validate_password=MagicMock(return_value=False)


    #act
    monkeypatch.setattr('builtins.input',mock_input)
    monkeypatch.setattr('builtins.print',mock_print)
    monkeypatch.setattr('ui_layer.app.validate_username',mock_validate_username)
    monkeypatch.setattr('ui_layer.app.validate_password',mock_validate_password)
    monkeypatch.setattr('ui_layer.app.main_menu',mock_main_menu)

    handle_signup()
    #assert
    mock_validate_username.assert_called_once_with('invlaid_username')
    mock_main_menu.assert_called_once()

def test_handle_signup_valid_username_invalid_passowrd(monkeypatch):
  # arrange
  mock_input = MagicMock(side_effect=['user12', '12'])
  mock_print = MagicMock()
  mock_main_menu = MagicMock()
  mock_validate_username = MagicMock(return_value=True)
  mock_validate_password = MagicMock(return_value=False)

  # act
  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('builtins.print', mock_print)
  monkeypatch.setattr('ui_layer.app.validate_username', mock_validate_username)
  monkeypatch.setattr('ui_layer.app.validate_password', mock_validate_password)
  monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)

  handle_signup()
  # assert
  mock_validate_username.assert_called_once_with('user12')
  mock_validate_password.assert_called_once_with('12')
  mock_main_menu.assert_called_once()


def test_handle_signup_invalid_username_valid_passowrd(monkeypatch):
  # arrange
  mock_input = MagicMock(side_effect=['user', '12345678'])
  mock_print = MagicMock()
  mock_main_menu = MagicMock()
  mock_validate_username = MagicMock(return_value=False)
  mock_validate_password = MagicMock(return_value=True)

  # act
  monkeypatch.setattr('builtins.input', mock_input)
  monkeypatch.setattr('builtins.print', mock_print)
  monkeypatch.setattr('ui_layer.app.validate_username', mock_validate_username)
  monkeypatch.setattr('ui_layer.app.validate_password', mock_validate_password)
  monkeypatch.setattr('ui_layer.app.main_menu', mock_main_menu)

  handle_signup()
  # assert
  mock_validate_username.assert_called_once_with('user')
  mock_main_menu.assert_called_once()


def test_handle_signup_valid_username_valid_password_username_not_exist(monkeypatch):
  mock_input=MagicMock(side_effect=['user12','12222111'])
  mock_auth=MagicMock()
  mock_auth.sign_up1=MagicMock(return_value=True)
  mock_print=MagicMock()
  mock_main_menu=MagicMock()
  mock_validate_username = MagicMock(return_value=True)
  mock_validate_password = MagicMock(return_value=True)

  monkeypatch.setattr('builtins.input',mock_input)
  monkeypatch.setattr('ui_layer.app.Auth',lambda :mock_auth)
  monkeypatch.setattr('builtins.print',mock_print)
  monkeypatch.setattr('ui_layer.app.main_menu',mock_main_menu)
  monkeypatch.setattr('ui_layer.app.validate_username', mock_validate_username)
  monkeypatch.setattr('ui_layer.app.validate_password', mock_validate_password)

  handle_signup()


  mock_auth.sign_up1.assert_called_once_with('user12','12222111','user')
  mock_main_menu.assert_called_once()
  mock_validate_username.assert_called_once_with('user12')
  mock_validate_password.assert_called_once_with('12222111')


def test_handle_signup_valid_username_valid_password_username_exist(monkeypatch):
  mock_input=MagicMock(side_effect=['user12','12222111'])
  mock_auth=MagicMock()
  mock_auth.sign_up1=MagicMock(return_value=False)
  mock_print=MagicMock()
  mock_main_menu=MagicMock()
  mock_validate_username = MagicMock(return_value=True)
  mock_validate_password = MagicMock(return_value=True)

  monkeypatch.setattr('builtins.input',mock_input)
  monkeypatch.setattr('ui_layer.app.Auth',lambda :mock_auth)
  monkeypatch.setattr('builtins.print',mock_print)
  monkeypatch.setattr('ui_layer.app.main_menu',mock_main_menu)
  monkeypatch.setattr('ui_layer.app.validate_username', mock_validate_username)
  monkeypatch.setattr('ui_layer.app.validate_password', mock_validate_password)

  handle_signup()


  mock_auth.sign_up1.assert_called_once_with('user12','12222111','user')
  mock_main_menu.assert_called_once()
  mock_validate_username.assert_called_once_with('user12')
  mock_validate_password.assert_called_once_with('12222111')
