## Standard Library Imports
import sys
import time

## Local Imports
from src.physical_interface.mockLCD import CharLCD1602 as LCD  # Adjusted import
from src.services.jobs_service import JobsService
from src.services.job_task_service import JobTaskService
from src.controllers.timer_controller import TimerController
from src.controllers.input_controller import InputController
from src.controllers.job_controller import JobController
from src.schemas.job_schemas import JobsContainer, Job, Task


class Controller(object):
    """Controller class to manage the appication logic."""
    def __init__(self):
        """Initialize the controller."""
        self.job_service = JobsService()
        self.job_tasks = JobTaskService()
        self.job_controller= JobController()
        self.lcd = LCD()
        self.timer = TimerController()
        self.input_controller = InputController()


    def shutdown(self):
        """Shutdown the controller."""
        self.lcd.write(0, 0, "\rExiting...")
        self.lcd.write(0, 1, "\rGoodbye!")
        self.lcd.destroy()
        # Restore terminal settings
        self.input_controller._restore_terminal()
        sys.exit()


    def check_input(self):
        """Check for keyboard input without blocking."""
        return self.input_controller.check_input()
  
    def loop(self):
        self.lcd.write(0, 0, "\rGood morning")
        time.sleep(.3)
        self.lcd.write(0, 1, "Ma'am:")
        time.sleep(1)

        if not self.job_controller.jobs:
            self.lcd.write(0, 0, "\rNo active jobs")
            self.lcd.write(0, 1, "\rPlease check later")
            self.shutdown()

        self._display_controls()
        
        # Setup navigation callbacks. This will need to be looked at it is very clunky. but for now it is kind of working
        navigation_callbacks = {
            'scroll_job': self.job_controller.scroll_job,
            'scroll_task': self.job_controller.scroll_task,
            'quit': self.shutdown
        }
        
        try:
            while True:
                # Check for key input and process
                key = self.input_controller.check_input()
                if key:
                    print(f"\r[DEBUG] Key pressed: '{key}' (ord: {ord(key)})")
                    result = self.input_controller.process_navigation_input(key, navigation_callbacks)
                    if result:
                        print(f"\r[DEBUG] Navigation action processed for key '{key}'")
                
                # Display current status
                self._display_current_status()
                
                time.sleep(0.1)  # Reduced sleep for more responsive input
                
        except KeyboardInterrupt:
            self.shutdown()

    def _display_controls(self):
        """Display control instructions."""
        help_text = self.input_controller.get_control_help_text()
        self.lcd.write(0, 0, help_text['line1'])
        self.lcd.write(0, 1, help_text['line2'])
        time.sleep(2)

    def _display_current_status(self):
        """Display current job and task status."""
        if self.job_controller.current_job and self.job_controller.current_job_task:
            self.lcd.write(0, 0, f"\r{self.job_controller.current_job.short_name} {self.job_controller.current_job_task.short_name}")
            self.lcd.write(0, 1, f"\r{self.timer.get_daily_elapsed_time()} {self.timer.get_task_elapsed_time()}")