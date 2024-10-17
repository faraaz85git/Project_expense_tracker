from unittest.mock import MagicMock
from custom_exception.custom_exception import SQLiteException,HTTPException
import pytest
from Router.expense import get_all_expense,create_expense
from request_response_models.ExpenseResponse import ExpenseResponse
class Test_expense:
    def setup_method(self):
        self.mock_user=MagicMock()
        self.mock_user.logger=MagicMock()
        self.mock_user.logger.log=MagicMock(return_value=1)
        self.mock_expense=MagicMock()


    @pytest.mark.asyncio
    async def test_get_all_expense_sucess(self,monkeypatch):
        #arrange
        self.mock_user.show_all_expense2=MagicMock(return_value=[(1,"2012-12-10","housing",120,"hello")])

        #act
        result= await get_all_expense(self.mock_user)

        #assert
        self.mock_user.show_all_expense2.assert_called_once()
        assert len(result) == 1
        assert result[0].exp_id == 1
        assert result[0].date == "2012-12-10"
        assert result[0].category == "housing"
        assert result[0].amount == 120.0
        assert result[0].description == "hello"

    @pytest.mark.asyncio
    async def test_get_all_expense_sqlite_exception(self,monkeypatch):
        # arrange
        self.mock_user.show_all_expense2 = MagicMock(side_effect=SQLiteException())

        # act
        with pytest.raises(HTTPException) as execption:
            await get_all_expense(self.mock_user)

        #assert
        self.mock_user.show_all_expense2.assert_called_once()
        assert execption.value.status_code==500
        assert execption.value.detail=="Internal server error."

    @pytest.mark.asyncio
    async def test_get_all_expense_general_exception(self, monkeypatch):
        # arrange
        self.mock_user.show_all_expense2 = MagicMock(side_effect=Exception())

        # act
        with pytest.raises(HTTPException) as execption:
            await get_all_expense(self.mock_user)

        #assert
        self.mock_user.show_all_expense2.assert_called_once()
        assert execption.value.status_code == 500
        assert execption.value.detail == "Internal server error."

    @pytest.mark.asyncio
    async def test_create_expenses_success(self, monkeypatch):
        # arrange
        self.mock_user.add_expense1 = MagicMock(return_value=True)

        # act
        result=await create_expense(self.mock_expense,self.mock_user)

        #assert
        self.mock_user.add_expense1.assert_called_once()
        assert type(result)==dict
        assert result.get("status") == "Expense created successfully."

    @pytest.mark.asyncio
    async def test_create_expenses_sqlite_exception(self, monkeypatch):
        # arrange
        self.mock_user.add_expense1 = MagicMock(side_effect=SQLiteException())

        # act
        with pytest.raises(HTTPException) as exception:
            await create_expense(self.mock_expense,self.mock_user)

        #assert
        self.mock_user.add_expense1.assert_called_once()
        assert exception.value.status_code == 500
        assert exception.value.detail == "Internal server error."

    @pytest.mark.asyncio
    async def test_create_expenses_general_exception(self, monkeypatch):
        # arrange
        self.mock_user.add_expense1 = MagicMock(side_effect=SQLiteException())

        # act
        with pytest.raises(HTTPException) as exception:
            await create_expense(self.mock_expense,self.mock_user)

        #assert
        self.mock_user.add_expense1.assert_called_once()
        assert exception.value.status_code == 500
        assert exception.value.detail == "Internal server error."
