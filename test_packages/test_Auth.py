import pytest
from unittest.mock import MagicMock
from business_layer.Auth import Auth

class TestAuth:
    def setup_method(self):
        self.acnt_manager=MagicMock()
        self.db_manager=MagicMock()

    def test_login1_valid_credentials(self,monkeypatch):
        self.db_manager.fetch_data=MagicMock(return_value=[('username', 'password','user')])
        self.mock_bcrypt=MagicMock(return_value=True)

        monkeypatch.setattr('business_layer.Auth.database_manager',lambda : self.db_manager)
        monkeypatch.setattr('business_layer.Auth.Account_manager',lambda : self.acnt_manager)
        monkeypatch.setattr('bcrypt.checkpw',self.mock_bcrypt)

        auth_obj=Auth()
        result=auth_obj.login1('username','password')

        assert result==('username', 'password','user')


    def test_login1_valid_username_invalid_password(self,monkeypatch):
        self.db_manager.fetch_data=MagicMock(return_value=[('valid_username','valid_password','user')])
        self.mock_bcrypt=MagicMock(return_value=False)

        monkeypatch.setattr('business_layer.Auth.database_manager', lambda: self.db_manager)
        monkeypatch.setattr('business_layer.Auth.Account_manager', lambda: self.acnt_manager)
        monkeypatch.setattr('bcrypt.checkpw',self.mock_bcrypt)

        auth_obj=Auth()
        actual_result=auth_obj.login1('valid_username','invalid_password')
        assert actual_result==None

    def test_login1_invalid_username_valid_password(self,monkeypatch):
        self.db_manager.fetch_data = MagicMock(return_value=[])


        monkeypatch.setattr('business_layer.Auth.database_manager', lambda: self.db_manager)
        monkeypatch.setattr('business_layer.Auth.Account_manager', lambda: self.acnt_manager)

        auth_obj = Auth()
        actual_result = auth_obj.login1('invalid_username', 'valid_password')
        assert actual_result == None


    def test_sign_up1_username_exists(self,monkeypatch):
        self.db_manager.fetch_data=MagicMock(return_value=[('user_id','username','password','role')])
        monkeypatch.setattr('business_layer.Auth.database_manager',lambda : self.db_manager)

        auth_obj=Auth()
        result=auth_obj.sign_up1('username','password','role')

        assert result==False

    def test_sign_up1_username_not_exists_inserted(self,monkeypatch):
        self.db_manager.fetch_data = MagicMock(return_value=[])
        self.db_manager.insert_data=MagicMock(return_value=True)
        self.mock_bcrypt=MagicMock()
        monkeypatch.setattr('business_layer.Auth.database_manager', lambda: self.db_manager)
        monkeypatch.setattr('bcrypt.hashpw',self.mock_bcrypt)

        auth_obj = Auth()
        result = auth_obj.sign_up1('username', 'password', 'role')

        assert result == True

    def test_sign_up1_username_not_exists_not_inserted(self,monkeypatch):
        self.db_manager.fetch_data = MagicMock(return_value=[])
        self.db_manager.insert_data=MagicMock(return_value=False)
        self.mock_bcrypt=MagicMock()
        monkeypatch.setattr('business_layer.Auth.database_manager', lambda: self.db_manager)
        monkeypatch.setattr('bcrypt.hashpw',self.mock_bcrypt)

        auth_obj = Auth()
        result = auth_obj.sign_up1('username', 'password', 'role')

        assert result == False







