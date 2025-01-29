import asyncio
from datetime import datetime, timedelta

class UserEventScheduler:
    def __init__(self):
        self.user_events = {}  # Dictionary to store events for each user
        self.loop = asyncio.get_event_loop()

    def add_user_event(self, user_id, event_time, callback, *args, **kwargs):
        now = datetime.now()
        delay = (event_time - now).total_seconds()

        if delay <= 0:
            raise ValueError("Event time must be in the future.")

        if user_id in self.user_events:
            existing_task = self.user_events[user_id]
            existing_task.cancel()

        task = self.loop.call_later(delay, self._execute_event, user_id, callback, *args, **kwargs)
        self.user_events[user_id] = task

    def _execute_event(self, user_id, callback, *args, **kwargs):
        callback(*args, **kwargs)
        if user_id in self.user_events:
            del self.user_events[user_id]

    def cancel_user_events(self, user_id):
        if user_id in self.user_events:
            self.user_events[user_id].cancel()
            del self.user_events[user_id]
