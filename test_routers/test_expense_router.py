from unittest.mock import MagicMock
from custom_exception.custom_exception import SQLiteException, HTTPException
import pytest
from Router.expense import get_expense_by_category, create_expense


class Test_expense:
    def setup_method(self):
        self.mock_user = MagicMock()
        self.mock_user.logger = MagicMock()
        self.mock_user.logger.log = MagicMock(return_value=1)
        self.mock_expense = MagicMock()

    @pytest.mark.asyncio
    async def test_get_all_expense_by_category_no_category_specify_return_all_expense(self, monkeypatch):
        # arrange
        self.mock_user.show_all_expense = MagicMock(
            return_value=[(1, "2012-12-10", "housing", 120, "hello")]
        )

        # act
        result = await get_expense_by_category(self.mock_user,[])

        # assert
        self.mock_user.show_all_expense.assert_called_once()
        assert len(result) == 1
        assert result[0].exp_id == 1
        assert result[0].date == "2012-12-10"
        assert result[0].category == "housing"
        assert result[0].amount == 120.0
        assert result[0].description == "hello"

    @pytest.mark.asyncio
    async def test_get_all_expense_by_category_valid_category_return_specified_category(self, monkeypatch):
        # arrange
        self.mock_user.show_expense_by_category = MagicMock(return_value=[(1, "2012-12-10", "food", 120, "hello")])

        # act
        result = await get_expense_by_category(self.mock_user, ["food"])

        # assert
        assert self.mock_user.logger.log.call_count==2
        self.mock_user.show_expense_by_category.assert_called_once()
        assert len(result) == 1
        assert result[0].exp_id == 1
        assert result[0].date == "2012-12-10"
        assert result[0].category == "food"
        assert result[0].amount == 120.0
        assert result[0].description == "hello"
    @pytest.mark.asyncio
    async def test_get_all_expense_by_category_invalid_category_bad_request(self, monkeypatch):
        # arrange

        # act
        with pytest.raises(HTTPException) as execption:
            await get_expense_by_category(self.mock_user,["invalid_category"])

        # assert
        assert execption.value.status_code == 400
        assert execption.value.detail == f"No valid category is provided.It must be one of housing,transport,food,clothing,other"
    @pytest.mark.asyncio
    async def test_get_all_expense_by_category_sqlite_exception(self, monkeypatch):
        # arrange
        self.mock_user.show_expense_by_category = MagicMock(side_effect=SQLiteException())

        # act
        with pytest.raises(HTTPException) as execption:
            await get_expense_by_category(self.mock_user,["food"])

        # assert
        self.mock_user.show_expense_by_category.assert_called_once()
        assert execption.value.status_code == 500
        assert execption.value.detail == "Sqlite Error."

    @pytest.mark.asyncio
    async def test_get_all_expense_by_category_internal_server_error(self, monkeypatch):
        # arrange
        self.mock_user.show_expense_by_category = MagicMock(side_effect=Exception())

        # act
        with pytest.raises(HTTPException) as execption:
            await get_expense_by_category(self.mock_user, ["food"])

        # assert
        self.mock_user.show_expense_by_category.assert_called_once()
        assert execption.value.status_code == 500
        assert execption.value.detail == "Internal server error."
    @pytest.mark.asyncio
    async def test_create_expenses_created_success(self, monkeypatch):
        # arrange
        self.mock_user.add_expense = MagicMock(return_value=True)

        # act
        result = await create_expense(self.mock_expense, self.mock_user)

        # assert
        self.mock_user.add_expense.assert_called_once()
        assert type(result) == dict
        assert result.get("status") == "Expense created successfully."

    @pytest.mark.asyncio
    async def test_create_expenses_sqlite_exception(self, monkeypatch):
        # arrange
        self.mock_user.add_expense = MagicMock(side_effect=SQLiteException())

        # act
        with pytest.raises(HTTPException) as exception:
            await create_expense(self.mock_expense, self.mock_user)

        # assert
        self.mock_user.add_expense.assert_called_once()
        assert exception.value.status_code == 500
        assert exception.value.detail == "Internal server error."

    @pytest.mark.asyncio
    async def test_create_expenses_general_exception(self, monkeypatch):
        # arrange
        self.mock_user.add_expense = MagicMock(side_effect=SQLiteException())

        # act
        with pytest.raises(HTTPException) as exception:
            await create_expense(self.mock_expense, self.mock_user)

        # assert
        self.mock_user.add_expense.assert_called_once()
        assert exception.value.status_code == 500
        assert exception.value.detail == "Internal server error."
