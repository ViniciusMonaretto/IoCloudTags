import asyncio
from datetime import datetime, timedelta
from ..database_conector.database_connector import DatabaseConnector
from Model.event_model import EventModel

def prt(user_id = 1, message = ""):
    print(f"Event triggered for user {user_id}: {message}")

class UserEventScheduler:
    def __init__(self, database_conector: DatabaseConnector):
        self.user_events = {}  
        self.loop = asyncio.get_event_loop()
        self._database_conector = database_conector
        self._lock = asyncio.Lock()

    async def init_scheduler(self):
        users = await self._database_conector.find_info_from_table("Users")
        for user in users:
            await self.check_event_for_user(user._id)

    async def check_event_for_user(self, user_id):
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        event_list = await self._database_conector.find_info_from_table("EventModels", {"UserId": user_id}, {"BeginDate": current_date}, ["BeginDate"], 1)
        if(len(event_list) == 0):
            return
        
        event: EventModel = event_list[0]
        await self.add_user_event(user_id, datetime.strptime(event._begin_date, "%Y-%m-%d %H:%M:%S"), prt)

    async def add_user_event(self, user_id, event_time, callback, *args, **kwargs):
        now = datetime.now()
        delay = (event_time - now).total_seconds()

        if delay <= 0:
            raise ValueError("Event time must be in the future.")

        async with self._lock:
            if user_id in self.user_events:
                existing_task, existing_event_time = self.user_events[user_id]

                if event_time < existing_event_time:
                    existing_task.cancel()
                    print(f"Canceling existing event for user {user_id} (scheduled at {existing_event_time})")
                else:
                    print(f"Keeping existing event for user {user_id} (scheduled at {existing_event_time})")
                    return

            # Schedule the new event
            task = asyncio.create_task(self._schedule_event(user_id, delay, callback, *args, **kwargs))
            self.user_events[user_id] = (task, event_time)
            print(f"Scheduled new event for user {user_id} at {event_time}") 

    async def _schedule_event(self, user_id, delay, callback, *args, **kwargs):
        await asyncio.sleep(delay)  # Wait for the delay
        await self._execute_event(user_id, callback, *args, **kwargs)  # Execute the event             

    async def _execute_event(self, user_id, callback, *args, **kwargs):

        async with self._lock:  # Ensure thread-safe access
            if asyncio.iscoroutinefunction(callback):
                await callback(*args, **kwargs)  # Await if the callback is a coroutine
            else:
                callback(*args, **kwargs)  # Call directly if it's a regular function

            # Remove the event after execution
            if user_id in self.user_events:
                del self.user_events[user_id]
        
        await self.check_event_for_user(user_id)

    async def cancel_user_events(self, user_id):
        async with self._lock:
            if user_id in self.user_events:
                existing_task, _ = self.user_events[user_id]
                existing_task.cancel()
                del self.user_events[user_id]
                print(f"Canceled event for user {user_id}")