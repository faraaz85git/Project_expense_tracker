from unittest.mock import MagicMock
import db_layer.myutils as mu



class Test_myutils:

    def test_get_float_input_valid_input(self,monkeypatch):
        #arrange
        mock_input=MagicMock(return_value='1')
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        #assert
        result=mu.get_float_input('Enter value')
        assert result==1

    def test_get_float_input_invalid_input(self,monkeypatch):
        #arrange
        mock_input=MagicMock(side_effect=['a','1'])
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        #assert
        result=mu.get_float_input('Enter value')
        assert result==1

    def test_get_date_input(self,monkeypatch):
        mock_input=MagicMock(return_value='')
        mock_datetime=MagicMock()
        mock_date=MagicMock()
        mock_date.strftime=MagicMock(return_value='2024-09-01')
        mock_datetime.now=MagicMock(return_value=mock_date)

        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('db_layer.myutils.datetime',mock_datetime)

        result=mu.get_date_input('enter date')

        assert result=='2024-09-01'


    def test_get_date_input_valid_date(self,monkeypatch):
        #arrange
        mock_input=MagicMock(return_value='2024-09-01')
        mock_date_obj=MagicMock()
        mock_datetime=MagicMock()
        mock_datetime.strptime=MagicMock(return_value=mock_date_obj)
        mock_date_obj.strftime=MagicMock(return_value='2024-09-01')

        #act
        monkeypatch.setattr('builtins.input',mock_input)
        monkeypatch.setattr('db_layer.myutils.datetime',mock_datetime)
        date=mu.get_date_input('enter date')

        #assert
        mock_datetime.strptime.assert_called_once()
        mock_date_obj.strftime.assert_called_once()
        assert date=='2024-09-01'

    def test_get_date_input_invalid_date(self, monkeypatch):
        # arrange
        mock_input = MagicMock(side_effect=['abcd','2024-09-02'])
        mock_datetime = MagicMock()
        mock_date_obj=MagicMock()
        mock_date_obj.strftime=MagicMock(return_value='2024-09-02')
        mock_datetime.strptime = MagicMock(side_effect=[ValueError("invalid date"),mock_date_obj])

        # act
        monkeypatch.setattr('builtins.input', mock_input)
        monkeypatch.setattr('db_layer.myutils.datetime', mock_datetime)
        date = mu.get_date_input('enter date')

        # assert
        mock_datetime.strptime.assert_any_call('abcd','%Y-%m-%d')
        mock_datetime.strptime.assert_any_call('2024-09-02','%Y-%m-%d')
        mock_date_obj.strftime.assert_called_once()
        assert date == '2024-09-02'

    def test_ask_category_choice_1(self, monkeypatch):
        # arrange
        mock_input = MagicMock(return_value='1')
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        category = mu.ask_category()
        # assert
        assert category == 'housing'

    def test_ask_category_choice_2(self, monkeypatch):
        # arrange
        mock_input = MagicMock(return_value='2')
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        category = mu.ask_category()
        # assert
        assert category == 'transport'

    def test_ask_category_choice_3(self, monkeypatch):
        # arrange
        mock_input = MagicMock(return_value='3')
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        category = mu.ask_category()
        # assert
        assert category == 'food'

    def test_ask_category_choice_4(self, monkeypatch):
        # arrange
        mock_input = MagicMock(return_value='4')
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        category = mu.ask_category()
        # assert
        assert category == 'clothing'

    def test_ask_category_choice_5(self, monkeypatch):
        # arrange
        mock_input = MagicMock(return_value='5')
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        category = mu.ask_category()
        # assert
        assert category == 'other'

    def test_update_category_1(self,monkeypatch):
        #arrange
        mock_input=MagicMock(return_value='1')
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        category=mu.update_category()
        #assert
        assert category=='housing'

    def test_update_category_2(self,monkeypatch):
        #arrange
        mock_input=MagicMock(return_value='2')
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        category=mu.update_category()
        #assert
        assert category=='transport'

    def test_update_category_3(self,monkeypatch):
        #arrange
        mock_input=MagicMock(return_value='3')
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        category=mu.update_category()
        #assert
        assert category=='food'

    def test_update_category_4(self,monkeypatch):
        #arrange
        mock_input=MagicMock(return_value='4')
        #act
        monkeypatch.setattr('builtins.input',mock_input)
        category=mu.update_category()
        #assert
        assert category=='clothing'

    def test_update_category_5(self, monkeypatch):
        # arrange
        mock_input = MagicMock(return_value='5')
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        category = mu.update_category()
        # assert
        assert category == 'other'

    def test_update_category_6(self, monkeypatch):
        # arrange
        mock_input = MagicMock(return_value='6')
        # act
        monkeypatch.setattr('builtins.input', mock_input)
        category = mu.update_category()
        # assert
        assert category == ''

    def test_curr_date_str(self,monkeypatch):
        #arrange
        mock_date_obj=MagicMock()
        mock_date_obj.strftime=MagicMock(return_value='2024-09-09')
        mock_datetime=MagicMock(return_value=mock_date_obj)
        mock_datetime.now=MagicMock(return_value=mock_date_obj)

        #act
        monkeypatch.setattr('db_layer.myutils.datetime',mock_datetime)
        date=mu.curr_date_str()
        #assert
        mock_datetime.now.assert_called_once()
        mock_date_obj.strftime.assert_called_once()
        assert date=='2024-09-09'

    def test_get_int_input_valid_int(self,monkeypatch):
        #arrange
        mock_input=MagicMock(return_value='1')

        #act
        monkeypatch.setattr('builtins.input',mock_input)
        value=mu.get_int_input('Enter an integer')
        #assert
        assert value==1

    def test_get_int_input_invalid_int(self,monkeypatch):
        #arrange
        mock_input=MagicMock(side_effect=['a','2'])

        #act
        monkeypatch.setattr('builtins.input',mock_input)
        value=mu.get_int_input('Enter an integer')
        #assert
        assert value==None
