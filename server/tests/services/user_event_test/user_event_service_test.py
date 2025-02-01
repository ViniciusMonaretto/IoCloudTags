import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.database_conector.database_connector import DatabaseConnector
from src.Model.event_model import EventModel
from src.services.user_event_scheduler.user_event_scheduler import UserEventScheduler, prt

@pytest.fixture
def mock_database_connector():
    return AsyncMock(spec=DatabaseConnector)

@pytest.mark.asyncio
async def test_init_scheduler(mock_database_connector):
    user_event_scheduler = UserEventScheduler(mock_database_connector)
    mock_database_connector.find_info_from_table.return_value = [MagicMock(_id=1)]
    user_event_scheduler.check_event_for_user = AsyncMock(return_value=None)
    await user_event_scheduler.init_scheduler()
    user_event_scheduler.check_event_for_user.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_check_event_for_user_with_no_events(mock_database_connector):
    user_event_scheduler = UserEventScheduler(mock_database_connector)
    user_event_scheduler.add_user_event = AsyncMock(return_value=None)

    mock_database_connector.find_info_from_table.return_value = []
    await user_event_scheduler.check_event_for_user(1)
    user_event_scheduler.add_user_event.assert_not_called()

@pytest.mark.asyncio
async def test_check_event_for_user_with_events(mock_database_connector):
    user_event_scheduler = UserEventScheduler(mock_database_connector)
    mock_event = MagicMock(spec=EventModel, _begin_date=(datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'))

    user_event_scheduler.add_user_event = AsyncMock(return_value=None)

    mock_database_connector.find_info_from_table.return_value = [mock_event]
    await user_event_scheduler.check_event_for_user(1)
    user_event_scheduler.add_user_event.assert_called_once_with(1, datetime.strptime(mock_event._begin_date, "%Y-%m-%d %H:%M:%S"), prt)
    mock_database_connector.find_info_from_table.assert_called_once_with("EventModels", {"UserId": 1}, {"BeginDate": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, ["BeginDate"], 1)

@pytest.mark.asyncio
async def test_add_user_event():
    user_event_scheduler = UserEventScheduler(mock_database_connector)
    event_time = datetime.now() + timedelta(minutes=5)
    mock_event = MagicMock(spec=EventModel, _begin_date=event_time)
    await user_event_scheduler.add_user_event(1, mock_event, prt)
    assert 1 in user_event_scheduler.user_events

@pytest.mark.asyncio
async def test_add_user_event_past_event():
    user_event_scheduler = UserEventScheduler(mock_database_connector)
    event_time = datetime.now() - timedelta(minutes=5)
    mock_event = MagicMock(spec=EventModel, _begin_date=event_time)
    with pytest.raises(ValueError, match="Event time must be in the future."):
        await user_event_scheduler.add_user_event(1, mock_event, prt)

@pytest.mark.asyncio
async def test_cancel_user_events():
    user_event_scheduler = UserEventScheduler(mock_database_connector)
    event_time = datetime.now() + timedelta(minutes=5)
    mock_event = MagicMock(spec=EventModel, _begin_date=event_time)
    await user_event_scheduler.add_user_event(1, mock_event, prt)
    await user_event_scheduler.cancel_user_events(1)
    assert 1 not in user_event_scheduler.user_events

@pytest.mark.asyncio
async def test_execute_event():
    user_event_scheduler = UserEventScheduler(mock_database_connector)
    event_time = datetime.now() + timedelta(seconds=1)
    mock_event = MagicMock(spec=EventModel, _begin_date=event_time)
    await user_event_scheduler.add_user_event(1, mock_event, prt)
    await asyncio.sleep(2)  # Wait for the event to trigger
    assert 1 not in user_event_scheduler.user_events

@pytest.mark.asyncio
async def test_schedule_event():
    user_event_scheduler = UserEventScheduler(mock_database_connector)
    event_time = datetime.now() + timedelta(seconds=1)
    mock_event = MagicMock(spec=EventModel, _begin_date=event_time)
    await user_event_scheduler.add_user_event(1, mock_event, prt)
    await asyncio.sleep(2)  # Wait for the event to trigger
    assert 1 not in user_event_scheduler.user_events