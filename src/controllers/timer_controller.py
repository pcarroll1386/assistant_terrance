from datetime import datetime, timezone

class TimerController(object):
    """Timer controller class to manage timers."""
    def __init__(self):
        """Initialize the timer controller."""
        self.task_start_time = datetime.now(timezone.utc)
        self.daily_start_timer = None

    def set_task_start_time(self):
        """Set the start time for the current task."""
        self.task_start_time = datetime.now(timezone.utc)

    def set_daily_start_timer(self):
        """Set the daily start timer."""
        self.daily_start_timer = datetime.now(timezone.utc)
    
    def get_task_elapsed_time(self) -> str:
        """Get the elapsed time for the current task in HH:MM format."""
        if self.task_start_time:
            elapsed = datetime.now(timezone.utc) - self.task_start_time
            total_seconds = int(elapsed.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}"
        return "00:00"

    def get_daily_elapsed_time(self) -> str:
        """Get the elapsed time for the current day in HH:MM format."""
        if self.daily_start_timer:
            elapsed = datetime.now(timezone.utc) - self.daily_start_timer
            total_seconds = int(elapsed.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}"
        return "00:00"
