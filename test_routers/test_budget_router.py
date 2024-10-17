from unittest.mock import MagicMock
from fastapi import HTTPException
import pytest
from custom_exception.custom_exception import SQLiteException,BudgetNotSetException
from Router.Budget import get_active_budget,set_budget
from request_response_models.BudgetResponse import BudgetResponse

active_budget=[(1000.0,1000.0,1000.0,1000.0,1000.0,"2024-10-16",
"2024-10-16")
]
start_date="2024-12-12"
end_date="2024-12-20"
budget_amount={
        "housing": 1000.0,
        "transport": 1000.0,
        "food": 1000.0,
        "clothing": 1000.0,
        "other": 1000.0
    }
amount_spend={
        "housing": 0,
        "transport": 3000.0,
        "food": 0,
        "clothing": 1000.0,
        "other": 0
    }
budget_status={
        "housing": 1000.0,
        "transport": -2000.0,
        "food": 1000.0,
        "clothing": 0.0,
        "other": 1000.0
    }
# status={
# "start_date":budget_status[3],
#                 "end_date":budget_status[4],
#                 "budget_amount":budget_status[0],
#                 "amount_spend":budget_status[1],
#                 "budget_status":budget_status[2]
# }
class Test_budget:
    def setup_method(self):
        self.mock_user = MagicMock()
        self.mock_user.logger = MagicMock()
        self.mock_user.logger.log = MagicMock(return_value=1)
        self.mock_request=MagicMock()
    @pytest.mark.asyncio
    async def test_get_active_budget_success(self,monkeypatch):
        #arrange
        mock_budget=MagicMock()
        mock_budget.active_budget=MagicMock(return_value=active_budget)

        #act
        monkeypatch.setattr("Router.Budget.Budget",lambda **arg: mock_budget)
        result= get_active_budget(self.mock_user,self.mock_request)

        #assert
        assert self.mock_user.logger.log.call_count == 2
        assert result.housing == 1000
        assert result.transport == 1000
        assert result.food == 1000
        assert result.clothing == 1000
        assert result.other == 1000
        assert result.start_date == "2024-10-16"
        assert result.end_date == "2024-10-16"

    @pytest.mark.asyncio
    async def test_get_active_budget_no_active_budget(self, monkeypatch):
        # arrange
        mock_budget = MagicMock()
        mock_budget.active_budget = MagicMock(return_value=[])

        # act
        monkeypatch.setattr("Router.Budget.Budget", lambda **arg: mock_budget)
        # assert
        with pytest.raises(HTTPException) as exe:
            get_active_budget(self.mock_user, self.mock_request)

        assert self.mock_user.logger.log.call_count == 2
        assert exe.value.status_code == 404
        assert exe.value.detail == "No active budget is found."

    @pytest.mark.asyncio
    async def test_get_active_budget_sqlite_exception(self, monkeypatch):
        # arrange
        mock_budget = MagicMock()
        mock_budget.active_budget = MagicMock(side_effect=SQLiteException())

        # act
        monkeypatch.setattr("Router.Budget.Budget", lambda **arg: mock_budget)
        # assert
        with pytest.raises(HTTPException) as exe:
            get_active_budget(self.mock_user, self.mock_request)

        assert self.mock_user.logger.log.call_count == 1
        assert exe.value.status_code == 500
        assert exe.value.detail == "Internal server error."

    @pytest.mark.asyncio
    async def test_get_active_budget_general_exception(self, monkeypatch):
        # arrange
        mock_budget = MagicMock()
        mock_budget.active_budget = MagicMock(side_effect=Exception())

        # act
        monkeypatch.setattr("Router.Budget.Budget", lambda **arg: mock_budget)
        # assert
        with pytest.raises(HTTPException) as exe:
            get_active_budget(self.mock_user, self.mock_request)

        assert self.mock_user.logger.log.call_count == 2
        assert exe.value.status_code == 500
        assert exe.value.detail == "Internal server error."

    @pytest.mark.asyncio
    async def test_create_budget_success(self, monkeypatch):
        # arrange
        mock_validate_budget_date = MagicMock(return_value=True)
        self.mock_user.set_budget_by_category2 = MagicMock()
        self.mock_user.username="user"
        mock_budget_create=MagicMock()
        mock_budget_create.start_date=MagicMock()
        mock_budget_create.end_date=MagicMock()
        mock_budget_create.model_dump=MagicMock(return_value={})

        # act
        monkeypatch.setattr("Router.Budget.validate_budget_date", mock_validate_budget_date)
        result = await set_budget(self.mock_user, mock_budget_create)

        # assert
        mock_validate_budget_date.assert_called_once_with(mock_budget_create.start_date,mock_budget_create.end_date)
        mock_budget_create.model_dump.assert_called_once()
        self.mock_user.set_budget_by_category2.assert_called_once_with(new_budget={"username":"user"})
        assert result.get("created")=="success"

    @pytest.mark.asyncio
    async def test_create_budget_end_date_smaller_than_start_date(self, monkeypatch):
        # arrange
        mock_budget_create = MagicMock()
        mock_budget_create.start_date = "2024-10-10"
        mock_budget_create.end_date = "2024-10-09"

        # act
        with pytest.raises(HTTPException) as exc:
            await set_budget(self.mock_user, mock_budget_create)

        #assert
        assert exc.value.status_code==400
        assert exc.value.detail == 'Invalid budget start date 2024-10-10 should be smaller than or equal to end data 2024-10-09.'

    @pytest.mark.asyncio
    async def test_create_budget_not_set_exception(self, monkeypatch):
        # arrange
        mock_validate_budget_date=MagicMock(return_value=True)
        self.mock_user.set_budget_by_category2 = MagicMock(side_effect=BudgetNotSetException())
        self.mock_user.username = "user"
        mock_budget_create = MagicMock()
        mock_budget_create.start_date = MagicMock()
        mock_budget_create.end_date = MagicMock()
        mock_budget_create.model_dump = MagicMock(return_value={})

        # act
        monkeypatch.setattr("Router.Budget.validate_budget_date", mock_validate_budget_date)
        with pytest.raises(HTTPException) as exc:
            await set_budget(self.mock_user, mock_budget_create)

        # assert
        mock_validate_budget_date.assert_called_once_with(mock_budget_create.start_date, mock_budget_create.end_date)
        mock_budget_create.model_dump.assert_called_once()
        self.mock_user.set_budget_by_category2.assert_called_once_with(new_budget={"username": "user"})
        assert exc.value.status_code == 400
        assert exc.value.detail=="Budget is not set."

    @pytest.mark.asyncio
    async def test_create_budget_not_general_exception(self, monkeypatch):
        # arrange
        mock_validate_budget_date = MagicMock(return_value=True)
        self.mock_user.set_budget_by_category2 = MagicMock(side_effect=Exception())
        self.mock_user.username = "user"
        mock_budget_create = MagicMock()
        mock_budget_create.start_date = MagicMock()
        mock_budget_create.end_date = MagicMock()
        mock_budget_create.model_dump = MagicMock(return_value={})

        # act
        monkeypatch.setattr("Router.Budget.validate_budget_date", mock_validate_budget_date)
        with pytest.raises(HTTPException) as exc:
            await set_budget(self.mock_user, mock_budget_create)

        # assert
        mock_validate_budget_date.assert_called_once_with(mock_budget_create.start_date, mock_budget_create.end_date)
        mock_budget_create.model_dump.assert_called_once()
        self.mock_user.set_budget_by_category2.assert_called_once_with(new_budget={"username": "user"})
        assert exc.value.status_code == 500
        assert exc.value.detail == "Internal server error."