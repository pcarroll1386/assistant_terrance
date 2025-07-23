from datetime import datetime

class TimerController(object):
    """Timer controller class to manage timers."""
    def __init__(self):
        """Initialize the timer controller."""
        self.task_start_time = datetime.now()
        self.daily_start_timer = None

    def set_task_start_time(self):
        """Set the start time for the current task."""
        self.task_start_time = datetime.now()

    def set_daily_start_timer(self):
        """Set the daily start timer."""
        self.daily_start_timer = datetime.now()
